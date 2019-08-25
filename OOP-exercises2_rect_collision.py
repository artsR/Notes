'''In games, we often put a rectangular "bounding box" around our sprites
in the game. We can then do collision detection between, say, bombs and spaceships,
by comparing whether rectangles overlap anywhere.'''
# Determine whether two rectangles collide:
#   - I made assumption that rectangles of my sprite is parallel to axis.

def collision(r1, r2):
    # TODO:
    #wyznaczyc wierzcholki prostokatow
    #sprawdzic czy ktorykolwiek z nich lezy w drugim prostokacie
    pass

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

    def __str__(self):
        return f'Point({self.x}, {self.y})'

class Rectangle():
    """Rectangle class using 'Point' class, width and height.
    Takes arguments: lowleft,"""

    def __init__(self, lowleft, width=0, height=0, topright=''):
        self.lowleft  = lowleft
        if topright=='':
            self.topright = Point(lowleft.x+width,lowleft.y+height)
            self.width  = width
            self.height = height
        else:
            self.topright = topright
            self.width = ((topright.x-lowleft.x)**2+(topright.y-lowleft.y)**2)**0.5
            self.height= (())

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
        return f'{self.lowleft}, {self.width}, {self.height}'

class Obstacle(Rectangle):
    def __init(self, lowleft, topright, width, height):
        super().__init(lowleft, width, height)
        self.topright = topright


posx = 0
posy = 0
w    = 2
h    = 6
sprite = Rectangle(Point(posx, posy), w, h)
print(sprite)
#num_obst = input('How many rectangles against sprite?..')
num_obst = 1
