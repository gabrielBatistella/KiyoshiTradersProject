# Classe abstrata que representa um manipulador genérico

import abc
from point import Point
from joints import Joints

class Manipulator(abc.ABC):
    def __init__(self, name, dof, jointTypes, speed = 0.05):
        self._name = name
        self._dof = dof
        self._jointTypes = jointTypes
        self._speed = speed

    def _getDOF(self):
        return self._dof

    def _getJointTypes(self):
        return self._jointTypes

    def _getSpeed(self):
        return self._speed
    
    def _setSpeed(self, speed):
        self._speed = speed

    dof = property(_getDOF, None)
    jointTypes = property(_getJointTypes, None)
    speed = property(_getSpeed, _setSpeed)

    @abc.abstractmethod
    class Joints(Joints):
        pass

    @abc.abstractmethod
    def isInWorkspace(self, point:Point):
        pass

    @abc.abstractmethod
    def fkine(self, jointVals:Joints):
        pass

    @abc.abstractmethod
    def ikine(self, point:Point):
        pass

    def __str__(self):
        return self._name