# Classe abstrata que representa um manipulador genérico

import abc

class Manipulator(abc.ABC):
    def __init__(self, name, dof, jointTypes):
        self._name = name
        self._dof = dof
        self._jointTypes = jointTypes

    def get_dof(self):
        return self._dof

    def get_jointTypes(self):
        return self._jointTypes

    dof = property(get_dof, None)
    jointTypes = property(get_jointTypes, None)

    @abc.abstractmethod
    def fkine(self, jointVals):
        raise NotImplementedError()

    @abc.abstractmethod
    def ikine(self, point):
        raise NotImplementedError()

    def __str__(self):
        return self._name