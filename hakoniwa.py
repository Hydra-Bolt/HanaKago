import json
import secrets
# My own DBMS named Hakoniwa(Box Garden)


class Hakoniwa:
    """
    A class representing a database management system (DBMS) named Hakoniwa.
    """

    def __init__(self, filename, is_identity=False):
        """
        Initialize the Hakoniwa object with the provided filename.

        Parameters:
            filename (str): The name of the file to be initialized.
            is_identity (bool): If True, generate sequential IDs.
                               If False, generate random IDs.
        """

        self.filename = filename
        self.__data_records = self._parse_json()
        self.current_id = self.loadCurrentID()


        # Set the method to generate IDs
        if is_identity:
            # Generate sequential IDs
            self.gen_id = self.genSequentialId
        else:
            # Generate random IDs
            self.gen_id = self.genRandomId

    def loadCurrentID(self):
        with open("TABLES/id.cache", "r") as f:
            lines = f.readlines()
            if len(lines) == 0:
                return 0
            else:
                for line in lines:
                    if line.startswith(self.filename):
                        return int(line.split("=")[1])

    def saveCurrentID(self):
        with open("TABLES/id.cache", "r+") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if lines[i].startswith(self.filename):
                    lines[i] = f"{self.filename}={self.current_id}\n"
                    break
            f.seek(0)
            f.writelines(lines)

    def genSequentialId(self):
        self.current_id += 1
        self.saveCurrentID()
        return self.current_id

    def genRandomId(self, length=16):
        """Generate a random ID composed of numbers with a specified length."""
        return int(''.join(secrets.choice('0123456789') for _ in range(length)))

    def _parse_json(self):
        """
        Parse the JSON data from the file associated with this object.

        Returns:
            list[dict]: The parsed JSON data.
        """
        with open(self.filename) as file:
            return json.load(file)

    def find(self, dict_find):
        """
        Finds and returns a list of dictionaries from the `__data_records` list that match the given `dict_find` dictionary.

        Parameters:
            dict_find (dict): The dictionary containing the key-value pairs to search for in the `__data_records` list.

        Returns:
            list[dict]: A list of dictionaries from the `__data_records` list that match the given `dict_find` dictionary.
        """
        return [record for record in self.__data_records if all(record.get(key) == value for key, value in dict_find.items())]

    def insert(self, record, add_id : str | None =None):
        """
        Insert a new record into the database file.

        Parameters:
            record (dict): The dictionary containing the key-value pairs to insert into the database.
        """
        if add_id is not None:
            record[add_id] = self.gen_id()
        self.__data_records.append(record)

    def update(self, dict_find, dict_update):
        """
        Updates a record in the database based on the provided `dict_find` and `dict_update` dictionaries.

        Parameters:
            dict_find (dict): A dictionary containing the key-value pairs to search for in the database.
            dict_update (dict): A dictionary containing the key-value pairs to update in the database.
        """
        for record in self.__data_records:
            if all(record.get(key) == value for key, value in dict_find.items()):
                record.update(dict_update)
                return

    def _update_db(self):
        """
        Update the database file with the current data records.
        """
        with open(self.filename, "w") as file:
            json.dump(self.__data_records, file, indent=2)

    def delete(self, dict_find):
        """
        Deletes a record from the database based on the provided `dict_find` dictionary.

        Parameters:
            dict_find (dict): The dictionary containing the key-value pairs to search for in the database.
        """
        self.__data_records = [record for record in self.__data_records if not all(record.get(key) == value for key, value in dict_find.items())]
    @property
    def data_records(self):
        return self.__data_records

    def __str__(self) -> str:
        return json.dumps(self.__data_records, indent=2)
    