import figures as fg
import random as rd
import math


# generowanie chmury punktów
def generateCloudOfPoints(a):
    points_set = []
    for i in range(a):
        points_set.append(generateRandomPoint())
    return points_set


# generowanie losowego punktu
def generateRandomPoint():
    point = fg.Point((rd.random()) * 600, (rd.random()) * 600)
    return point


# generowanie losowej linii (losowy punkt początku i końca)
def generateRandomLine():
    line = fg.Line(generateRandomPoint(), generateRandomPoint())
    return line


# generowanie losowego trójkąta (losowe trzy punkty)
def generateRandomTriangle():
    triangle = fg.Triangle(generateRandomPoint(), generateRandomPoint(), generateRandomPoint())
    return triangle


# generowanie losowego wielokąta - losowe n punktów, n - losowa liczba z zakresu 3-10
def generateRandomPolygon():
    i = 0
    n = rd.randint(3, 10)
    lista = []

    while i < n:
        lista.append(generateRandomPoint())
        i += 1
    polygon = fg.Polygon(lista)
    return polygon


# funkcja sprawdzająca po której stronie linii jest punkt
# -1 - lewa, 0 - na linii, 1 - prawa
def pointToLine(p, l):
    if -l.a * p.x + p.y - l.b < 0:
        return -1
    elif -l.a * p.x + p.y - l.b == 0:
        return 0
    else:
        return 1


# funkcja sprawdzająca czy punkt leży w trójkącie (metoda sumy pól trójkątów)
# 1 - punkt wewnątrz trójkąta, 0 - poza nim
def pointToTriangle(p, t):
    t1 = fg.Triangle(p, t.a, t.b)
    t2 = fg.Triangle(p, t.b, t.c)
    t3 = fg.Triangle(p, t.c, t.a)
    sum = t1.getArea() + t2.getArea() + t3.getArea()
    area = t.getArea()
    if area + 0.5 >= sum >= area - 0.5:
        return 1
    else:
        return 0


# funkcja sprawdzająca czy punkt leży w wielokącie, metoda sumy pól trójkątów
# 1 - punkt wewnątrz wielokąta, 0 - poza nim
def pointToPolygon(point, polygon):
    i = 0
    sum = 0
    area = 0
    while i < len(polygon.pointsList):
        if i == len(polygon.pointsList) - 1:
            t = fg.Triangle(point, polygon.pointsList[i], polygon.pointsList[0])
            sum += t.getArea()
            break
        t = fg.Triangle(point, polygon.pointsList[i], polygon.pointsList[i + 1])
        sum += t.getArea()
        i += 1
    point = polygon.pointsList[0]
    i = 1
    while i < len(polygon.pointsList):
        if i == len(polygon.pointsList) - 1:
            t = fg.Triangle(point, polygon.pointsList[i], polygon.pointsList[0])
            area += t.getArea()
            break
        t = fg.Triangle(point, polygon.pointsList[i], polygon.pointsList[i + 1])
        area += t.getArea()
        i += 1

    if area + 1 >= sum >= area - 1:
        return 1
    else:
        return 0


# wyznaczenie punktów przecięcia linii z okręgiem
def lineWithCircleIntersection(l, circle):
    a = math.pow(l.begin.x, 2) + math.pow(l.begin.y, 2) + math.pow(l.end.x, 2) + math.pow(l.end.y, 2) - (
            2 * ((l.begin.x * l.end.x) + (l.begin.y * l.end.y)))
    b = 2 * ((circle.center.x * (l.end.x - l.begin.x)) + (circle.center.y * (l.end.y - l.begin.y)) + (
                l.begin.x * l.end.x) + (
                     l.begin.y * l.end.y) - math.pow(l.end.x, 2) - math.pow(l.end.y, 2))
    c = -1 * (circle.r * circle.r) + math.pow(l.end.x, 2) + math.pow(l.end.y, 2) + math.pow(circle.center.x,
                                                                                            2) + math.pow(
        circle.center.y, 2) - (
                2 * ((circle.center.x * l.end.x) + (circle.center.y * l.end.y)))
    delta = (b * b) - (4 * a * c)

    if delta > 0:
        e1 = (-b + math.sqrt(delta)) / (2 * a)
        e2 = (-b - math.sqrt(delta)) / (2 * a)
        x1 = e1 * l.begin.x + (1 - e1) * l.end.x
        y1 = e1 * l.begin.y + (1 - e1) * l.end.y
        x2 = e2 * l.begin.x + (1 - e2) * l.end.x
        y2 = e2 * l.begin.y + (1 - e2) * l.end.y
        point1 = fg.Point(x1, y1)
        point2 = fg.Point(x2, y2)
        points = [point1, point2]
        return points

    elif delta == 0:
        e1 = -b / (2 * a)
        x0 = e1 * l.begin.x + (1 - e1) * l.end.x
        y0 = e1 * l.begin.y + (1 - e1) * l.end.y
        point1 = fg.Point(x0, y0)
        return point1
    else:
        return None


# wyznaczenie punktu przecięcia dwóch linii
def twoLinesIntersection(l1, l2):
    if l1.a != l2.a:
        x = (l2.b - l1.b) / (l1.a - l2.a)
        y = l1.a * x + l1.b
        point = fg.Point(x, y)
        return point
    else:
        return None


# wyznaczenie równania funkcji liniowej przechodzącej przez dwa punkty p1, p2
# zwrócona zostaje tablica equation, equation[0] - wsp. kierunkowy, equation[1] - wyraz wolny
def twoPointsEquation(p1, p2):
    a = -(((p1.y - 300) / 6) - ((p2.y - 300) / 6)) / (((p1.x - 300) / 6) - ((p2.x - 300) / 6))
    b = ((p1.y - 300) / 6) - (a * ((p1.x - 300) / 6))
    equation = [a, b]
    return equation
