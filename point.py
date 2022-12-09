# Classe que representa um ponto no espaço 3D

from math import sqrt

class Point:
    """ 
    A class to represent a point in 3D space

    ...

    Attributes
    ----------
    x : float
        x coordinate of the point
    y : float
        y coordinate of the point
    z : float
        z coordinate of the point

    Methods
    -------
    dist():
        Calculates the distance from the point to the origin (0, 0, 0).
    """

    def __init__(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z

    def dist(self):
        return sqrt(self._x**2 + self._y**2 + self._z**2)

    def __add__(self, otherPoint):
        return Point(self._x + otherPoint._x, self._y + otherPoint._y, self._z + otherPoint._z)

    def __sub__(self, otherPoint):
        return Point(self._x - otherPoint._x, self._y - otherPoint._y, self._z - otherPoint._z)

    def __str__(self):
        return "(" + str(round(self._x, 2)) + " ; " + str(round(self._y, 2)) + " ; " + str(round(self._z, 2)) + ")"
p = Point()