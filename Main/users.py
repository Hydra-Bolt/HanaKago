from abc import abstractmethod, abstractproperty


class Person:

    def __init__(self, first_name,last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.age} years old"


class User(Person):
    def __init__(self, first_name, last_name, age, username, password):
        super().__init__(first_name, last_name, age)
        self.__username = username
        self.__password = password

    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.age} years old and is identified by {self.username}"


    @property
    @abstractmethod
    def get_username(self):
        pass
    
    @property
    @abstractmethod
    def get_password(self):
        pass
    

class Admin(User):
    def __init__(self, first_name, last_name, age, username, password):
        super().__init__(first_name, last_name, age, username, password)

    @property
    def get_username(self):
        return self.__username

    @property
    def get_password(self):
        return self.__password
    
class Customer(User):
    def __init__(self, first_name, last_name, age, username, password):
        super().__init__(first_name, last_name, age, username, password)

    @property
    def get_username(self):
        return self.__username

    @property
    def get_password(self):
        return self.__password