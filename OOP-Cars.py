
class Vehicle:
    def __init__(self, price, color):
        self.color = color
        self.price = price
        self.gas   = 0

    def fillUpTank(self):
        self.gas    = 10

    def emptyTank(self):
        self.gas    = 0

    def gasLeft(self):
        return self.gas

class Truck(Vehicle):
    def __init__(self, price, color, tires):
        # Inherit:
        super().__init__(price, color) # Calls the 'Vehicle' classes 'contructor' method (__init__)
        self.tires  = tires

    def beep(self):
        print('Honk honk !!')

class Car(Vehicle):
    def __init(self, price, color, speed):
        # Inherit:
        super().__init__(price, color) # Calls the 'Vehicle' classes 'contructor' method (__init__)
        self.speed  = speed

    def beep(self):
        print('Beep beep !!')
