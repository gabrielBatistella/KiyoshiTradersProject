# Classe abstrata que representa um manipulador genérico

import abc
from point import Point

class Manipulator(abc.ABC):
    def __init__(self, name, dof, jointTypes, speed = 0.05):
        self._name = name
        self._dof = dof
        self._jointTypes = jointTypes
        self._speed = speed

    def get_dof(self):
        return self._dof

    def get_jointTypes(self):
        return self._jointTypes

    def get_speed(self):
        return self._speed
    
    def set_speed(self, speed):
        self._speed = speed

    dof = property(get_dof, None)
    jointTypes = property(get_jointTypes, None)
    speed = property(get_speed, set_speed)

    @abc.abstractmethod
    class Joints():
        def __init__(self):
            raise NotImplementedError()

    @abc.abstractmethod
    def isInWorkspace(self, point : Point):
        raise NotImplementedError()

    @abc.abstractmethod
    def fkine(self, jointVals : Joints):
        raise NotImplementedError()

    @abc.abstractmethod
    def ikine(self, point : Point):
        raise NotImplementedError()

    def __str__(self):
        return self._name