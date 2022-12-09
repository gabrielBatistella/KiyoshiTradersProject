# Classe abstrata que representa as juntas de um manipulador genérico

import numpy as np
import abc

class Joints(abc.ABC):
    def __init__(self, dof, jointTypes):
        self._joints = [None] * dof
        self._jointTypes = jointTypes

    @classmethod
    @property
    @abc.abstractmethod
    def qLim(cls):
        pass

    def __getitem__(self, index):
        return self._joints[index]

    def __setitem__(self, index, qx):
        if qx == None:
            return
        elif qx >= type(self).qLim[index][0] and qx <= type(self).qLim[index][1]:
            self._joints[index] = qx
        else:
            raise ValueError()

    def __iter__(self):
        return iter(self._joints)

    def __str__(self):
        string = "(" 
        for joint, jointType in zip(self._joints, self._jointTypes):
            jointFormatted = ""
            if jointType:
                jointFormatted += str(round(np.rad2deg(joint), 2))
            else:
                jointFormatted += str(round(joint, 2))
            string += jointFormatted + " ; "
        string = string.removesuffix(" ; ")
        string += ")"
        return string