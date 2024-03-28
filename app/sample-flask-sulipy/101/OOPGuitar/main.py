class Guitar:
    def __init__(self, n_strings=6): # instead of hardcoding attribute we can use parameters
        self.n_strings = n_strings # attribute
        self.play() # call play method on the CLASS itself
        self.__cost = 50
    def play(self): # create wo/ self we just create a function, not a method
        # play() simple function
        # object.play() we call method on SOMETHING :)
        print("pam pam pam pam")

# inheritance
class BassGuitar(Guitar):
    pass

# take all the data from parent class (Guitar)
class ElectricGuitar(Guitar):
    def __init__(self):
        super().__init__(n_strings = 8) # access parent attributes, methods
        self.colour = ("#000000", "#FFFFFF") # you can add atrr, meth also
        # self.__cost = 50 # confidental data use __, de mindenhonnan elérhető :)
    def playLouder(self):
        print("pam pam pam pam".upper())
    def __secret(self):
        print("this guitar actually cost me $", self._Guitar__cost, "only!")

my_guitar = ElectricGuitar()
my_guitar.playLouder()
print("child class: ", my_guitar.n_strings)
print("parent class: ", BassGuitar(4).n_strings)
print("my bass guitar has", BassGuitar(4).n_strings, "strings")
print("my electric guitar has", my_guitar.n_strings, "strings")
# my_guitar._ElectricGuitar
# my_guitar.play() # call the mothed on the object itself