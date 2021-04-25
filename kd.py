import math
import functions as fn
import figures as fg
from operator import attrgetter
import convex


# klasa Node - węzeł w drzewie kd
# x - x'owa współrżedna, y - y-owa współrzędna
# left - wskazanie na lewego syna, right - na prawego syna
# parent - wskazanie na rodzica
class Node:
    x = 0.0
    y = 0.0
    left = None
    right = None
    parent = None


# klasa Tree (KD-TREE)
# addNode(node), dodaje węzeł do drzewa KD w odpowiednie miejsce
# postOrder - wypisanie drzewa KD w kolejności postOrder
# findNearestNeighbour(node, target) - przeszukuje drzewo pod kątem najbliższego sąsiada
# node - korzeń drzewa, target - węzeł, dla którego poszukiwany jest najbliższy sąsiad
# generateTree - generuje drzewo, z przekazanej jako argument listy punktów , axis = 0 dla osi X
class Tree:
    root = None
    depth = 1

    def addNode(self, node):
        i = 0
        side = 0
        if self.root is None:
            self.root = node
        else:
            tmp2, tmp = self.root, self.root
            while tmp2 is not None:
                tmp = tmp2
                if i % 2 == 0:
                    if node.x < tmp.x:
                        tmp2 = tmp.left
                        side = 0
                    else:
                        tmp2 = tmp.right
                        side = 1
                else:
                    if node.y < tmp.y:
                        tmp2 = tmp.left
                        side = 0
                    else:
                        tmp2 = tmp.right
                        side = 1
                i += 1
            node.parent = tmp
            tmp2 = node
            if side == 0:
                tmp.left = tmp2
            else:
                tmp.right = tmp2

    def postOrder(self, node):
        if node:
            self.postOrder(node.left)
            print("(", node.x, ",", node.y, ")")
            self.postOrder(node.right)

    def findNearestNeighbour(self, node, target):
        best = None
        bestdistance = math.inf

        def search(node, depth):
            nonlocal best, bestdistance
            if node is None:
                return None
            distance = convex.distance(node, target)

            if distance != 0 and (best is None or distance < bestdistance):
                best = node
                bestdistance = distance
            if depth % 2 == 0:
                diff = target.x - node.x
                if diff <= 0:
                    close, away = node.left, node.right
                else:
                    close, away = node.right, node.left
            else:
                diff = target.y - node.y
                if diff <= 0:
                    close, away = node.left, node.right
                else:
                    close, away = node.right, node.left
            search(close, depth + 1)
            if diff ** 2 < bestdistance:
                search(away, depth + 1)

        search(node, 0)
        return best

    def generateTree(self, points, axis):
        if len(points) <= 0:
            return None
        elif len(points) == 1:
            node = Node()
            node.x = points[0].x
            node.y = points[0].y
            self.addNode(node)
            return None
        if axis % 2 == 0:
            sorted_points = sorted(points, key=attrgetter('x'))
        else:
            sorted_points = sorted(points, key=attrgetter('y'))

        center = math.floor(len(sorted_points) / 2) + len(sorted_points) % 2
        node = Node()
        node.x = sorted_points[center].x
        node.y = sorted_points[center].y
        self.addNode(node)
        self.generateTree(sorted_points[:center], axis + 1)
        self.generateTree(sorted_points[center + 1:], axis + 1)
