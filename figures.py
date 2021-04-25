import math

'''Klasa Point, współrzędne x,y'''
class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = round(x)
        self.y = round(y)

    def __repr__(self):
        return repr((self.x, self.y))

    def print(self):
        print("x: ", self.x, " y: ", self.y, "")

'''Klasa Line, współrzędne początku i końca linii, a - współczynnik kierunkowy, b - wyraz wolny'''
class Line:
    begin = Point(0, 0)
    end = Point(0, 0)
    a = 0
    b = 0

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.a = round((begin.y - end.y) / (begin.x - end.x), 2)
        self.b = round((begin.y - self.a * begin.x), 2)

    def print(self):
        print("Begin: ")
        self.begin.print()
        print("End: ")
        self.end.print()
        print("y=", self.a, "x+", self.b)

    def calcEnds(self):
        self.begin.x = 0
        self.begin.y = self.a*self.begin.x+self.b
        self.end.x = 600
        self.end.y = self.a*self.end.x+self.b

'''Klasa Triangle, współrzędne 3 punktów'''
'''Posiada Metodę obliczającą pole trójkąta'''
class Triangle:
    a = Point(0, 0)
    b = Point(0, 0)
    c = Point(0, 0)
    area = 0

    def getArea(self):
        print("(%d,%d)"%(self.a.x,self.a.y))
        print("(%d,%d)" % (self.b.x, self.b.y))
        print("(%d,%d)" % (self.c.x, self.c.y))
        a = math.sqrt((self.a.x - self.b.x) * (self.a.x - self.b.x) + (self.a.y - self.b.y) * (self.a.y - self.b.y))
        b = math.sqrt((self.b.x - self.c.x) * (self.b.x - self.c.x) + (self.b.y - self.c.y) * (self.b.y - self.c.y))
        c = math.sqrt((self.c.x - self.a.x) * (self.c.x - self.a.x) + (self.c.y - self.a.y) * (self.c.y - self.a.y))
        p = 0.5 * (a + b + c)
        return math.sqrt(p * (p - a) * (p - b) * (p - c))/36

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

'''Klasa Polygon - atrybut - lista punktów składających się na wielokąt'''
class Polygon:
    pointsList = []

    def __init__(self, pointsList):
        i = 0
        while i < len(pointsList):
            self.pointsList.append(pointsList[i])
            i += 1

    def print(self):
        i = 0
        while i < len(self.pointsList):
            print("Point nr ",i," (",self.pointsList[i].x,",",self.pointsList[i].y,")")
            i += 1
'''Klasa Circle - atrybuty: center - zmienna typu Point, radius - promień koła'''
class Circle:
    def __init__(self, point, radius):
        self.center = point
        self.r = radius