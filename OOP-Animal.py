
class Animal():
    version = 1
    def __init__(self, name, age):
        self.name = name
        self.age  = age
        self.sound = 'some sounds...'

    def speak(self):
        print(f'I am {self.name} and I am {self.age} years old')

    def talk(self):
        print(f'{self.sound}')

class Dog(Animal):
    def __init__(self, name='', age=0):
        super().__init__(name, age)
        self.type   = 'dog'
        self.sound  = 'Bark !!'

    # def talk(self):
    #     print('Bark!!') # Overrides 'talk' method of parent class

class Cat(Animal):
    def __init__(self, name='', age=0):
        self.name   = name
        self.age    = age
        self.type   = 'cat'
        self.sound  = 'Moew...'

    def change_age(self, age):
        self.age    = age

tim = Dog('Tim', 3)
tim.speak()
"""
tim.name = 'Bruno' # however best practice is to change 'attribute' within class:
tim.change_name('Bruno') # change_name(self, name): self.name = name
"""
fred = Dog('Fred')
pusia = Cat('Pusia')
nobody = Animal('nobody', 10)
fred.speak()
fred.talk()
pusia.talk()
nobody.talk()
fred.version = 2 # the better way is to do it through 'method'
print(fred.version)
print(nobody.version) # outcome: 1 - still 1 even if 'fred' changed to 2
simba = Dog('Simba')
print(simba.version)  # outcome: 1
print(fred.version)   # outcome: 2 - by assign value to this variable 'fred' creates his own 'version'
