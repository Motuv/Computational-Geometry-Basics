import tkinter as tk
from tkinter import simpledialog
import figures as fg
import functions as fn
import convex
import kd
from tkinter.ttk import *
from tkinter import *
import random as rd


class Application:
    pointdb, linedb, triangledb, polygondb, circledb = [], [], [], [], []
    chosenpoint, chosenline, chosentriangle, chosenpolygon, chosencircle = None, None, None, None, None
    windows = []

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Computational Geometry")
        self.window.geometry("800x800")
        self.windows.append(self.window)
        self.menu = tk.Menu(self.window)
        self.clearCanvas = tk.Button(text="Clear board", command=self.clear)
        cascade = tk.Menu(self.menu)
        self.menu.add_cascade(label="Creator", menu=cascade)
        cascade.add_command(label="Create point", command=self.createPointDialogBox)
        cascade.add_command(label="Create line", command=self.createLineDialogBox)
        cascade.add_command(label="Create polygon", command=self.createPolygonDialogBox)
        cascade.add_command(label="Create circle", command=self.createCircleDialogBox)
        cascade2 = tk.Menu(self.menu)
        self.menu.add_cascade(label="Generator", menu=cascade2)
        cascade2.add_command(label="Generate random point", command=lambda: self.generateFigure(0))
        cascade2.add_command(label="Generate random line", command=lambda: self.generateFigure(1))
        cascade2.add_command(label="Generate random triangle", command=lambda: self.generateFigure(2))
        cascade2.add_command(label="Generate random polygon", command=lambda: self.generateFigure(3))
        cascade3 = tk.Menu(self.menu)
        self.menu.add_cascade(label="Selector", menu=cascade3)
        cascade3.add_command(label="Select point", command=lambda: self.selectFigure(0))
        cascade3.add_command(label="Select line", command=lambda: self.selectFigure(1))
        cascade3.add_command(label="Select triangle", command=lambda: self.selectFigure(2))
        cascade3.add_command(label="Select polygon", command=lambda: self.selectFigure(3))
        cascade3.add_command(label="Select circle", command=lambda: self.selectFigure(4))
        cascade4 = tk.Menu(self.menu)
        self.menu.add_cascade(label="Algorithms", menu=cascade4)
        cascade4.add_command(label="Point to line", command=self.pointToLineWhichSide)
        cascade4.add_command(label="Point to triangle", command=self.pointToTriangle)
        cascade4.add_command(label="Point to polygon", command=self.pointToPolygon)
        cascade4.add_command(label="Area of the triangle", command=self.getTriangleArea)
        cascade4.add_command(label="Two points equation", command=self.twoPointsEquation)
        cascade4.add_command(label="Two lines intersection", command=self.twoLinesIntersection)
        cascade4.add_command(label="Line with circle intersection", command=self.lineWithCircleIntersection)
        cascade4.add_command(label="Convex hull", command=self.convexHull)
        cascade4.add_command(label="Nearest neighbours", command=self.nearestNeighbours)

        self.window.config(menu=self.menu)
        self.my_canvas = tk.Canvas(width=600, height=600, bg="white")
        self.my_canvas.create_line(300, 0, 300, 600, fill="black")
        self.my_canvas.create_line(0, 300, 600, 300, fill="black")
        self.my_canvas.pack()
        self.clearCanvas.pack()
        self.window.mainloop()

# funkcje wyświetlające dialogboxy, potrzebne do wprowadzania koordynatów punktów, linii, wielokątów
    def createPointDialogBox(self):
        x = (tk.simpledialog.askinteger("Input", "Enter x-coordinate: ", minvalue=-50, maxvalue=50) * 6) + 300
        y = 300 - (tk.simpledialog.askinteger("Input", "Enter y-coordinate: ", minvalue=-50, maxvalue=50) * 6)
        p = fg.Point(x, y)
        self.my_canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="blue")
        self.pointdb.append(p)

    def createLineDialogBox(self):
        x1 = (tk.simpledialog.askinteger("Input", "Enter x-coordinate of first point: ", minvalue=-50,
                                         maxvalue=50) * 6) + 300
        y1 = 300 - (tk.simpledialog.askinteger("Input", "Enter y-coordinate of first point: ", minvalue=-50,
                                               maxvalue=50) * 6)
        x2 = (tk.simpledialog.askinteger("Input", "Enter x-coordinate of first point: ", minvalue=-50,
                                         maxvalue=50) * 6) + 300
        y2 = 300 - (tk.simpledialog.askinteger("Input", "Enter y-coordinate of first point: ", minvalue=-50,
                                               maxvalue=50) * 6)
        p1 = fg.Point(x1, y1)
        p2 = fg.Point(x2, y2)
        l1 = fg.Line(p1, p2)
        l1.calcEnds()
        self.my_canvas.create_line(l1.begin.x, l1.begin.y, l1.end.x, l1.end.y, fill="blue")
        self.linedb.append(l1)

    def createPolygonDialogBox(self):
        n = tk.simpledialog.askinteger("Input", "Enter number of points in polygon: ", minvalue=3, maxvalue=10)
        points = []
        drawcoords = []
        for i in range(n):
            x = (tk.simpledialog.askinteger("Input", "Enter x-coordinate of %d point: " % i, minvalue=-50,
                                            maxvalue=50) * 6) + 300
            y = 300 - (tk.simpledialog.askinteger("Input", "Enter y-coordinate of %d point: " % i, minvalue=-50,
                                                  maxvalue=50) * 6)
            p = fg.Point(x, y)
            points.append(p)
            drawcoords.append(x)
            drawcoords.append(y)
        if n == 3:
            triangle = fg.Triangle(points[0], points[1], points[2])
            self.triangledb.append(triangle)
        else:
            polygon = fg.Polygon(points)
            self.polygondb.append(polygon)
        self.my_canvas.create_polygon(drawcoords, outline="blue", fill="white", width=5)

    def createCircleDialogBox(self):
        x = (tk.simpledialog.askinteger("Input", "Enter x-coordinate of center: ", minvalue=-50, maxvalue=50) * 6) + 300
        y = 300 - (tk.simpledialog.askinteger("Input", "Enter y-coordinate of center: ", minvalue=-50, maxvalue=50) * 6)
        r = tk.simpledialog.askinteger("Input", "Enter y-coordinate of center: ", minvalue=-50, maxvalue=50) * 6
        center = fg.Point(x, y)
        c = fg.Circle(center, r)
        self.my_canvas.create_oval(x - r, y - r, x + r, y + r, outline="blue", fill="white")
        self.circledb.append(c)

# funkcje służące do wyboru figury, wywoływana jest tylko selectFigure, która komunikuje się z chooseFigure

    def selectFigure(self, opt):
        newWindow = tk.Tk()
        newWindow.geometry("200x200")
        self.windows.append(newWindow)
        i = 0
        if opt == 0:
            tk.Label(newWindow, text="List of points:").pack()
            for p in self.pointdb:
                tk.Label(newWindow, text="%d: Point coords (%d,%d)" % (i, (p.x - 300) / 6, (p.y - 300) / -6)).pack()
                i += 1

        elif opt == 1:
            tk.Label(newWindow, text="List of lines:").pack()
            for l in self.linedb:
                tk.Label(newWindow, text="%d: Line equation %d x + %d" % (i, l.a, l.b)).pack()
                i += 1
        elif opt == 2:
            tk.Label(newWindow, text="List of triangles:").pack()
            for t in self.triangledb:
                tk.Label(newWindow, text="%d: Triangle" % (i)).pack()
                i += 1
        elif opt == 3:
            tk.Label(newWindow, text="List of polygons:").pack()
            for t in self.triangledb:
                tk.Label(newWindow, text="%d: Polygon" % (i)).pack()
                i += 1
        elif opt == 4:
            tk.Label(newWindow, text="List of circles:").pack()
            for t in self.circledb:
                tk.Label(newWindow, text="%d: Circle" % (i)).pack()
                i += 1
        x = tk.simpledialog.askinteger("Input", "Enter number of figure: ")
        self.chooseFigure(opt, x)

    def chooseFigure(self, opt, x):
        drawcoords = []
        if opt == 0:
            self.chosenpoint = self.pointdb[x]
            self.my_canvas.create_oval(self.chosenpoint.x - 3, self.chosenpoint.y - 3, self.chosenpoint.x + 3,
                                       self.chosenpoint.y + 3, fill="red")

        elif opt == 1:
            self.chosenline = self.linedb[x]
            self.my_canvas.create_line(self.chosenline.begin.x, self.chosenline.begin.y, self.chosenline.end.x,
                                       self.chosenline.end.y, fill="red")
        elif opt == 2:
            self.chosentriangle = self.triangledb[x]
            drawcoords.append(self.chosentriangle.a.x)
            drawcoords.append(self.chosentriangle.a.y)
            drawcoords.append(self.chosentriangle.b.x)
            drawcoords.append(self.chosentriangle.b.y)
            drawcoords.append(self.chosentriangle.c.x)
            drawcoords.append(self.chosentriangle.c.y)
            self.my_canvas.create_polygon(drawcoords, outline="red", fill="white", width=5)
        elif opt == 3:
            self.chosenpolygon = self.polygondb[x]
            for i in range(len(self.chosenpolygon.pointsList)):
                drawcoords.append(self.chosenpolygon.pointsList[i].x)
                drawcoords.append(self.chosenpolygon.pointsList[i].y)
            self.my_canvas.create_polygon(drawcoords, outline="red", fill="white", width=5)
        elif opt == 4:
            self.chosencircle = self.circledb[x]
            self.my_canvas.create_oval(self.chosencircle.center.x - self.chosencircle.r,
                                       self.chosencircle.center.y - self.chosencircle.r,
                                       self.chosencircle.center.x + self.chosencircle.r,
                                       self.chosencircle.center.y + self.chosencircle.r, outline="red", fill="white")
        self.windows[-1].destroy()

# graficzne implementacje algorytmów z plików functions, convex, kd
    def pointToLineWhichSide(self):
        self.selectFigure(0)
        self.selectFigure(1)
        result = fn.pointToLine(self.chosenpoint, self.chosenline)
        if result == -1:
            side = "left side of the line"
        elif result == 0:
            side = "line"
        else:
            side = "right side of the line"
        tk.Label(self.windows[0], text="Point (%d,%d) is on the %s %d x + %d" % ((self.chosenpoint.x - 300) / 6,
                                                                                 (self.chosenpoint.y - 300) / -6, side,
                                                                                 self.chosenline.a,
                                                                                 (self.chosenline.b - 300) / -6)).pack()

    def pointToTriangle(self):
        self.selectFigure(0)
        self.selectFigure(2)
        result = fn.pointToTriangle(self.chosenpoint, self.chosentriangle)
        if result == 1:
            tk.Label(self.windows[0], text="Point is inside the triangle").pack()
        else:
            tk.Label(self.windows[0], text="Point is outside the triangle").pack()

    def pointToPolygon(self):
        self.selectFigure(0)
        self.selectFigure(3)
        result = fn.pointToPolygon(self.chosenpoint, self.chosenpolygon)
        if result == 1:
            tk.Label(self.windows[0], text="Point is inside the polygon").pack()
        else:
            tk.Label(self.windows[0], text="Point is outside the polygon").pack()

    def getTriangleArea(self):
        self.selectFigure(2)
        tk.Label(self.windows[0], text="Area of the selected triangle = %.2f" % self.chosentriangle.getArea()).pack()

    def generateFigure(self, opt):
        drawcoords = []
        if opt == 0:
            point = fn.generateRandomPoint()
            self.my_canvas.create_oval(point.x - 3, point.y - 3, point.x + 3, point.y + 3, fill="blue")
            self.pointdb.append(point)
        elif opt == 1:
            line = fn.generateRandomLine()
            line.calcEnds()
            self.my_canvas.create_line(line.begin.x, line.begin.y, line.end.x, line.end.y, fill="blue")
            self.linedb.append(line)
        elif opt == 2:
            triangle = fn.generateRandomTriangle()
            drawcoords.append(triangle.a.x)
            drawcoords.append(triangle.a.y)
            drawcoords.append(triangle.b.x)
            drawcoords.append(triangle.b.y)
            drawcoords.append(triangle.c.x)
            drawcoords.append(triangle.c.y)
            self.my_canvas.create_polygon(drawcoords, outline="blue", fill="white", width=5)
            self.triangledb.append(triangle)
        elif opt == 3:
            polygon = fn.generateCloudOfPoints(rd.randint(3, 10))
            hull = convex.graham_scan(polygon)
            chcoords = []
            for i in hull:
                chcoords.append(i.x)
                chcoords.append(i.y)
            self.my_canvas.create_polygon(chcoords, outline="blue", fill="white", width=5)
            polygon = fg.Polygon(hull)
            self.polygondb.append(polygon)

    def lineWithCircleIntersection(self):
        self.selectFigure(1)
        self.selectFigure(4)
        result = fn.lineWithCircleIntersection(self.chosenline, self.chosencircle)
        if result is not None:
            if len(result) == 2:
                self.my_canvas.create_oval(result[0].x - 3, result[0].y - 3, result[0].x + 3, result[0].y + 3,
                                           fill="red")
                self.my_canvas.create_oval(result[1].x - 3, result[1].y - 3, result[1].x + 3, result[1].y + 3,
                                           fill="red")
            elif len(result) == 1:
                self.my_canvas.create_oval(result.x - 3, result.y - 3, result.x + 3, result.y + 3, fill="red")

    def convexHull(self):
        x = tk.simpledialog.askinteger("Input", "Enter number of points in hull: ", minvalue=3, maxvalue=100)
        points = fn.generateCloudOfPoints(x)
        hull = convex.graham_scan(points)
        chcoords = []
        for i in hull:
            chcoords.append(i.x)
            chcoords.append(i.y)
        self.my_canvas.create_polygon(chcoords, outline="red", fill="white", width=5)
        for p in points:
            self.my_canvas.create_oval(p.x - 3, p.y - 3, p.x + 3, p.y + 3, fill="blue")

    def clear(self):
        self.pointdb = []
        self.linedb = []
        self.triangledb = []
        self.polygondb = []
        self.circledb = []
        self.chosenpoint = None
        self.chosenline = None
        self.chosentriangle = None
        self.chosenpolygon = None
        self.chosencircle = None
        self.my_canvas.delete("all")
        self.my_canvas.create_line(300, 0, 300, 600, fill="black")
        self.my_canvas.create_line(0, 300, 600, 300, fill="black")
        self.my_canvas.pack()

    def nearestNeighbours(self):
        x = tk.simpledialog.askinteger("Input", "Enter number of points in kd-tree: ", minvalue=3, maxvalue=100)
        tree = kd.Tree()
        points_set = fn.generateCloudOfPoints(x)
        tree.generateTree(points_set, 0)
        for p in points_set:
            self.my_canvas.create_oval(p.x - 3, p.y - 3, p.x + 3, p.y + 3, fill="blue")
            near = tree.findNearestNeighbour(tree.root, p)
            self.my_canvas.create_line(p.x, p.y, near.x, near.y, fill="black")

    def twoLinesIntersection(self):
        self.selectFigure(1)
        l1 = self.chosenline
        self.selectFigure(1)
        p = fn.twoLinesIntersection(l1, self.chosenline)
        self.my_canvas.create_oval(p.x - 3, p.y - 3, p.x + 3, p.y + 3, fill="blue")

    def twoPointsEquation(self):
        self.selectFigure(0)
        p1 = self.chosenpoint
        self.selectFigure(0)
        self.my_canvas.create_line(p1.x, p1.y, self.chosenpoint.x, self.chosenpoint.y, fill="black")
        eq = fn.twoPointsEquation(p1, self.chosenpoint)
        tk.Label(self.windows[0], text="Line equation: y = %.2f x + %.2f" % (eq[0], eq[1])).pack()


app = Application()
