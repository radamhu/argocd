#OOP
class PlayerCharacter():
    # Class Object Attribute : not dynamic
    membership = True    
    def __init__(self, name='anonymous', age=0):
        self._name = name #attributes
        self._age = age

    def shout(self):
        print(f'my name is {self.name}')

    @classmethod
    def adding_things(cls, num1, num2):
        return num1 + num2

    @staticmethod
    def adding_things(num1, num2):
        return num1 + num2

    def speak(self):
        print(f'my name is {self._name}, and i am {self._age} years old')

player1 = PlayerCharacter('Tom', 10)

print(player1.adding_things(2,3))
player1.speak()