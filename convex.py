from matplotlib import pyplot as plt, patches  # for plotting
import math
from matplotlib.path import Path
import functions as fn
import figures as fg
import random

# funkcja scatter_plot - potrzebna do samodzielnego działania programu (bez GUI)
'''def scatter_plot(coords, convex_hull=None):
    chcoords = []
    xs, ys, xsch, ysch, verts, codes = [], [], [], [], [], []
    for i in coords:
        xs.append(i.x)
        ys.append(i.y)
    for i in range(len(convex_hull)):

        xsch.append(convex_hull[i].x)
        ysch.append(convex_hull[i].y)
        verts.append((convex_hull[i].x, convex_hull[i].y))
        if i == 0:
            codes.append(Path.MOVETO)
        elif i == len(convex_hull) - 1:
            codes.append(Path.LINETO)
            verts.append(verts[0])
            codes.append(Path.CLOSEPOLY)
        else:
            codes.append(Path.LINETO)

    fig, ax = plt.subplots()
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor="None", lw=2)
    ax.add_patch(patch)

    plt.scatter(xs, ys)
    plt.scatter(xsch, ysch, marker="D")
    plt.show()
'''

# funkcja find_angle - zwracaa kąt pomiędzy dwoma punktami, potrzebne do sortowania wzgl kątów
def find_angle(p0, p1=None):
    if p1 is None:
        p1 = anchor
    y_span = p0.y - p1.y
    x_span = p0.x - p1.x
    return math.atan2(y_span, x_span)

# funkcja zwracająca odległość między dwoma punktami
def distance(p0, p1=None):
    if p1 is None:
        p1 = anchor
    y_span = p0.y - p1.y
    x_span = p0.x - p1.x
    return y_span * y_span + x_span * x_span

# funkcja zwracająca wyznacznik, służy do sprawdzenia, czy punkt leży po lewej/prawej stronie linii, bądź na niej
def det(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

# funkcja sortująca względem kątów tworzonych przez początek ukłądu współrzędnych i kolejne punkty z chmury punktów
def quicksort(a):
    if len(a) <= 1:
        return a
    smaller, equal, larger = [], [], []
    piv_ang = find_angle(a[random.randint(0, len(a) - 1)])
    for pt in a:
        pt_ang = find_angle(pt)
        if pt_ang < piv_ang:
            smaller.append(pt)
        elif pt_ang == piv_ang:
            equal.append(pt)
        else:
            larger.append(pt)
    return quicksort(smaller) + sorted(equal, key=distance) + quicksort(larger)

# algorytm grahama wyznaczający otoczkę wypukłą. zwraca listę punktów należącą do otoczki.
def graham_scan(points):
    global anchor
    min_idx = -1
    for i in range(len(points)):
        if min_idx == -1 or points[i].y < points[min_idx].y:
            min_idx = i
        if points[i].y == points[min_idx].y and points[i].x < points[min_idx].x:
            min_idx = i

    anchor = points[min_idx]

    sorted_pts = quicksort(points)
    del sorted_pts[sorted_pts.index(anchor)]

    hull = [anchor, sorted_pts[0]]
    for s in sorted_pts[1:]:
        while det(hull[-2], hull[-1], s) <= 0:
            del hull[-1]

        hull.append(s)
    return hull

