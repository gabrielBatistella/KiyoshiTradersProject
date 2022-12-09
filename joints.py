# Classe abstrata que representa as juntas de um manipulador genérico

import numpy as np
import abc

class Joints(abc.ABC):
    """ 
    An abstract class to represent the manipulator's joint values.

    ...

    Attributes
    ----------
    joints : float list
        Manipulator's joint values, only accepts values within limits.
    """
    
    def __init__(self, dof):
        self._joints = [None] * dof

    def __getitem__(self, index):
        return self._joints[index]

    @abc.abstractmethod
    def __setitem__(self, index, qx):
        pass

    def __iter__(self):
        return iter(self._joints)

    @abc.abstractmethod
    def __str__(self):
        pass