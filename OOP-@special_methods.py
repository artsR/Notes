
class Animal():
    animals = [] # every child has access to this list.

    def __init__(self, name, age): # I may change name of variable within 'Animal'
                                # and I don't have to change it in 'child class'.
        self.name = name
        self.age  = age
        self.animals.append(self)
        self.type = 'nobody'

    def speak(self):
        print(f'I am {self.name} and I am {self.age} years old {self.type}')

    def talk(self):
        print('Some sounds...')

    @classmethod
    def num_animals(cls):
        return len(cls.animals)

class Dog(Animal):
    num_dogs = 0
    def __init__(self, name='', age=0): # I don't even have to use 'super()'. I may input 'pass' instead of this line
        super().__init__(name, age)     # and it still will be working. However I want to add another variable: 'type' so I need it.
        self.type   = 'dog'
        Dog.num_dogs += 1
    @staticmethod # doesn't have access to class variables and instances
    def talk(n):
        for _ in range(n):
            print('Bark!!')


daisy = Dog('daisy')
who = Animal('nobody', 7)
print(Animal.animals) #1 refers to the same variable like (2)
print(daisy.animals)  #2 refers to the same variable like (1)

print(Animal.animals[0].speak()) # it seems that every index has length of 2 (obj + None)
print(Animal.animals[1].speak())

print(daisy.num_animals())

daisy.talk(2)
#Animal.talk() #it's error because there is not 'self' (instance like ex. 'daisy')
Dog.talk(3)   #it's not error because 'talk' in 'Dog class' doesn't require 'self' arg.
print(Dog.num_dogs)
simba = Dog('simba')
print(simba.num_dogs)

# Check if 'instance A' belongs to 'class X':
isinstance(daisy, Dog)      # True
isinstance(daisy, Animal)   # True

issubclass(Dog, Dog)        # True
issubclass(Dog, Animal)     # True
issubclass(Animal, Dog)     # False
