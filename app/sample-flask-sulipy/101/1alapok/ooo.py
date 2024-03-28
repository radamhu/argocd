class User():
    def __init__(self, email):
        self.email = email
    def sign_in(self):
        print('logged in')

class Wizard(User):
    def __init__(self, name, power, email):
        #User.__init__(self, email) : ennek egyszerűbb változata a super()
        super().__init__(email)
        self.name = name
        self.power = power
    def attack(self):
        print(f'attacking with power of {self.power}')

class Archer(User):
    def __init__(self, name, num_arrows):
        User.__init__(self, email)
        self.name = name
        self.num_arrows = num_arrows    
    def attack(self):
        print(f'attacking with arrows: arrows left: {self.num_arrows}')

wizard1 = Wizard('Merlin', 50, 'merlin@gmail.com')

print(wizard1.email)
#wizard1.attack()
#archer1.attack()


