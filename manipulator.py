# Classe abstrata que representa um manipulador genérico

import abc
from point import Point
from joints import Joints

class Manipulator(abc.ABC):
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