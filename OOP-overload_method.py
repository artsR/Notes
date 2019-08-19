
class Point():
    def __init__(self, x=0, y=0):
        self.x  = x
        self.y  = y
        self.coords = (self.x, self.y)

    def move(self, x, y):
        self.x  += x
        self.y  += y

    def __eq__(self, other):   # the function which overrides '=='
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __str__(self):
        return f'Point({self.x}, {self.y})'

    def length(self):
        import math
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __gt__(self, other):
        return self.length() > other.length()


p1  = Point(3,4)
p2  = Point(3,2)
p3  = Point(1,3)
p4  = Point(0,1)

# having defined '__eq__' in my class now I can easily compare coords of the points:
"""instead of using: 'p1.x == p2.x and p1.y == p2.y' I may use: 'p1 == p2' """
print(p1 == p2)

"""The other python default methods that can be overload are including:
__add__  : +
__sub__  : -
__mul__  : *
__str__  :
__gt__   : >
__ge__   : >=
__lt__   : <
__le__   : <=
"""

print(p2)
"""result: 'Point(3, 2)' - I defined the way string is displayed in my '__str__'
method."""
print(p2, p3, p1)

print(p1 > p2) # '>' has been overloaded in class
print(p4 > p3)
