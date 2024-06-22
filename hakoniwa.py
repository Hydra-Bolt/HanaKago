import json

# My own DBMS named Hakoniwa(Box Garden)


class Hakoniwa:
    """
    A class representing a database management system (DBMS) named Hakoniwa.
    """

    def __init__(self, filename):
        """
        Initialize the Hakoniwa object with the provided filename.

        Parameters:
            filename (str): The name of the file to be initialized.
        """
        self.filename = filename
        self.__data_records = self._parse_json()

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

    def insert(self, dict_insert):
        """
        Insert a new record into the database file.

        Parameters:
            dict_insert (dict): The dictionary containing the key-value pairs to insert into the database.
        """
        self.__data_records.append(dict_insert)
        self._update_db()

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

    @property
    def data_records(self):
        return self.__data_records
    
    def __str__(self) -> str:
        return json.dumps(self.__data_records, indent=2)
