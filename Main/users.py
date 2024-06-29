from abc import ABC, abstractmethod


class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.age} years old"


class User(Person, ABC):
    def __init__(self, first_name, last_name, age, username, password):
        super().__init__(first_name, last_name, age)
        self._username = username  # Protected attribute
        self._password = password  # Protected attribute

    def __str__(self):
        return f"{self.first_name} {self.last_name} is {self.age} years old and is identified by {self.get_username}"

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
        return self._username

    @property
    def get_password(self):
        return self._password


class Customer(User):
    def __init__(self, first_name, last_name, age, username, password):
        super().__init__(first_name, last_name, age, username, password)

    @property
    def get_username(self):
        return self._username

    @property
    def get_password(self):
        return self._password

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "username": self._username,
            "password": self._password,
        }
