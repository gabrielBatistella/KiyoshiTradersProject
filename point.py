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

    Implemented Operations
    ----------------------
    addition : Point = Point + Point
        P = (P1.x + P2.x, P1.y + P2.y, P1.z + P2.z).
    subtraction : Point = Point - Point
        P = (P1.x - P2.x, P1.y - P2.y, P1.z - P2.z).
    multiplication : Point = Point * float|int
        P = (P1.x * k, P1.y * k, P1.z * k).
    reverse_multiplication : Point = float|int * Point
        P = (P1.x * k, P1.y * k, P1.z * k).
    true_division : Point = Point / float|int
        P = (P1.x / k, P1.y / k, P1.z / k).
    str : string = str(Point)
        S = "(P1.x ; P1.y ; P1.z)".
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
        """
        Calculates the distance from the point to the origin (0, 0, 0).
        Can be used to calculate distance between 2 specific points by using (p1 - p2).dist().

        Returns
        -------
        dist : float
            Distance from the point to the origin (0, 0, 0).
        """

        return sqrt(self._x**2 + self._y**2 + self._z**2)

    def __add__(self, other):
        if type(other) == Point:
            return Point(self._x + other._x, self._y + other._y, self._z + other._z)
        else:
            raise TypeError("unsupported operand type(s) for +: 'Point' and " + type(other).__name__)

    def __sub__(self, other):
        if type(other) == Point:
            return Point(self._x - other._x, self._y - other._y, self._z - other._z)
        else:
            raise TypeError("unsupported operand type(s) for -: 'Point' and " + type(other).__name__)

    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Point(self._x*other, self._y*other, self._z*other)
        else:
            raise TypeError("unsupported operand type(s) for -: 'Point' and " + type(other).__name__)

    def __rmul__(self, other):
        return self*other

    def __truediv__(self, other):
        if type(other) == int or type(other) == float:
            return Point(self._x/other, self._y/other, self._z/other)
        else:
            raise TypeError("unsupported operand type(s) for -: 'Point' and " + type(other).__name__)

    def __str__(self):
        return "(" + str(round(self._x, 2)) + " ; " + str(round(self._y, 2)) + " ; " + str(round(self._z, 2)) + ")"