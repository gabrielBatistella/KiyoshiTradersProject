import abc
from point import Point
from joints import Joints_

class Manipulator(abc.ABC):
    """ 
    An abstract class to represent a generic manipulator

    ...

    Attributes
    ----------
    name : string
        name of the manipulator
    dof : int
        manipulator's number of degrees of freedom
    jointTypes : tuple[bool]
        indicates the type of the joints; True = rotative, False = prismatic
    jointLims : tuple[tuple[float]]
        indicates the limits of the joints
    speed : float
        avarage speed of the manipulator's end-effector
    
    Methods
    -------
    isInWorkspace(point):
        Verifies if the given point is inside of the manipulator's workspace.
        If argument is a iterable, verify all points.
    fkine(jointVals):
        Calculates the manipulator's end-effector position in the space for given joint values - forward kinematics.
        If argument is a iterable, apply method to all values.
    ikine(point):
        Calculates the manipulator's joint values for given end-effector position in the space - inverse kinematics.
        If argument is a iterable, apply method to all points.

    Inner Class
    -----------
    Joints:
        A structure that stores the manipulator's joint values.

    Implemented Operations
    ----------------------
    str : string = str(Manipulator)
        S = "manip.name".
    """
    
    def __init__(self, name, dof, jointTypes, jointLims, speed = 0.05):
        self._name = name
        self._dof = dof
        self._jointTypes = jointTypes
        self._jointLims = jointLims
        self._speed = speed

    @property
    def dof(self):
        return self._dof

    @property
    def jointTypes(self):
        return self._jointTypes

    @property
    def jointLims(self):
        return self._jointLims

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, speed):
        self._speed = speed

    @abc.abstractmethod
    class Joints(Joints_):
        """
        A structure that stores the manipulator's joint values.
        Abstract method to be implemented in subclass (specific manipulator).
        """
        pass

    @abc.abstractmethod
    def isInWorkspace(self, point:Point | tuple[Point]):
        """
        Verifies if the given point is inside of the manipulator's workspace.
        If argument is a iterable, verify all points.

        Abstract method to be implemented in subclass (specific manipulator).
        """
        pass

    @abc.abstractmethod
    def fkine(self, jointVals:Joints | tuple[Joints]):
        """
        Calculates the manipulator's end-effector position in the space for given joint values - forward kinematics.
        If argument is a iterable, apply method to all values.

        Abstract method to be implemented in subclass (specific manipulator)
        """
        pass

    @abc.abstractmethod
    def ikine(self, point:Point | tuple[Point]):
        """
        Calculates the manipulator's joint values for given end-effector position in the space - inverse kinematics.
        If argument is a iterable, apply method to all points.

        Abstract method to be implemented in subclass (specific manipulator)
        """
        pass

    def __str__(self):
        return self._name