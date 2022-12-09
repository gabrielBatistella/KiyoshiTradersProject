# Classe que representa um ponto no espaço 3D

from math import sqrt

class Point:
    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    
    def _getX(self):
        return self._x

    def _getY(self):
        return self._y
    
    def _getZ(self):
        return self._z

    x = property(_getX, None)
    y = property(_getY, None)
    z = property(_getZ, None)

    def dist(self):
        return sqrt(self._x**2 + self._y**2 + self._z**2)

    def __add__(self, otherPoint):
        return Point(self._x + otherPoint._x, self._y + otherPoint._y, self._z + otherPoint._z)

    def __sub__(self, otherPoint):
        return Point(self._x - otherPoint._x, self._y - otherPoint._y, self._z - otherPoint._z)

    def __str__(self):
        return "(" + str(round(self._x, 2)) + " ; " + str(round(self._y, 2)) + " ; " + str(round(self._z, 2)) + ")"