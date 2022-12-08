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
        return sqrt(self._x**2 + self._y**2 + self._z**2)

    def __add__(self, otherPoint):
        return Point(self._x + otherPoint._x, self._y + otherPoint._y, self._z + otherPoint._z)

    def __sub__(self, otherPoint):
        return Point(self._x - otherPoint._x, self._y - otherPoint._y, self._z - otherPoint._z)

    def __str__(self):
        return "(" + str(round(self._x, 2)) + " ; " + str(round(self._y, 2)) + " ; " + str(round(self._z, 2)) + ")"