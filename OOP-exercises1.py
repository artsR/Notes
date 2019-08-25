
class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        pass

    # Compute distance between two points:
    def distanceFromPoint(self, other):
        import math
        return math.sqrt( (other.x - self.x)**2 + (other.y - self.y)**2 )

    # Reflect point about x-axis:
    def reflect_x(self):
        return Point(self.x, -self.y)

    # Compute equation of the straight line joining the two points:
    def getLine(self, other):
        a = (other.y - self.y) / (other.x - self.x)
        b = self.y - a * self.x
        return (a, b)

    # Move point relative distance given as arguments:
    def move(self, dx, dy):
        self.x += + dx
        self.y += + dy
        return self  # is it a good practice?

    # Find center of circle with 3 points:
    def findCenter(self, other1, other2):
        pass

    # Replace str() functionality to make special  :
    def __str__(self):
        return f'Point({self.x}, {self.y})'
#-------------------------------------------------------------------------------
# Exercises2

class Rectangle():
    """Rectangle class using 'Point' class, width and height."""

    def __init__(self, point, width, height):
        self.point  = point
        self.width  = width
        self.height = height

    def getWidth(self):
        print(self.width)

    def getHeigth(self):
        print(self.height)

    def transpose(self):
        w = self.width
        self.width = self.height
        self.height = w
        return self

    def contains(self, oth_point):
        ch_height = (oth_point.x < (self.width + self.point.x) and
                    (oth_point.x >= self.point.x))
        ch_width = (oth_point.y < (self.height + self.point.y) and
                    (oth_point.y >= self.point.y))
        return ch_height and ch_width

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * self.width + 2 * self.height

    def diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** 0.5

    def __str__(self):
        return f'{self.point}, {self.width}, {self.height}'


#-------------------------------------------------------------------------------
p1 = Point(3, 3)
p2 = Point(6, 7)

d = p1.distanceFromPoint(p2)
print(d)

reflx = p2.reflect_x()
print(reflx)
# Find line between 2 points:
print(Point(4, 11).getLine(Point(6, 15)))

print(p1.move(1,4))

p3 = p1.move(0,0)
print(p1, p3)

# 'is' refers to deep equiality: checks if variables refer to the same object:
print(p1 is p3) # in this case p1 i p3 refers to the same object in memory.

#-------------------------------------------------------------------------------
# Exercises 2
#-------------------------------------------------------------------------------
rect = Rectangle(Point(4,2), 4, 5)
r1 = Rectangle(Point(0, 0), 10, 5)
r2 = Rectangle(Point(3, 1), 3, 4)
print(rect)
print(f'Area      = {rect.area()}')
print(f'Perimeter = {rect.perimeter()}')
print(rect.transpose())

print(r1.contains(Point(0,0)))
print(r1.contains(Point(3,3)))
print(r1.contains(Point(3,7)))
print(r1.contains(Point(3,5)))
print(r1.contains(Point(3,4.99999)))
print(r1.contains(Point(-3,-3)))

print(f'Diagonal of {r2} = {r2.diagonal()}')
