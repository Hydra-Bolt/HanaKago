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
        self.username = username
        self.password = password