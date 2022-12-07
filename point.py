# Classe que representa um ponto no espaço 3D

from math import sqrt

class Point:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    
    def get_x(self):
        return self._x

    def get_y(self):
        return self._y
    
    def get_z(self):
        return self._z

    x = property(get_x, None)
    y = property(get_y, None)
    z = property(get_z, None)

    def dist(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def __str__(self):
        return "(" + str(self.x) + " ; " + str(self.y) + " ; " + str(self.z) + ")"

    def __add__(self, otherPoint):
        return Point(self.x + otherPoint.x, self.y + otherPoint.y, self.z + otherPoint.z)

    def __sub__(self, otherPoint):
        return Point(self.x - otherPoint.x, self.y - otherPoint.y, self.z - otherPoint.z)