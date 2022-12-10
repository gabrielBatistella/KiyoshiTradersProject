# Código de cinemática inversa para o manipulador Barrett-WAM com 4 graus de liberdade
# 4 juntas rotativas
# Cinemática Inversa calculada manualmente

import numpy as np
from point import Point
from joints import Joints
from manipulator import Manipulator

class BarretWAM_4(Manipulator):
    _manipName = "Barret-WAM (4 DOF)"
    _manipDOF = 4
    _manipJointTypes = (True, True, True, True)      # Tupla de boolean (True = Rotativa ; False = Prismática)   :   RRRR
    _manipJointLims = ((np.deg2rad(-150), np.deg2rad(150)),   # R
                       (np.deg2rad(-113), np.deg2rad(113)),   # R
                       (np.deg2rad(-157), np.deg2rad(157)),   # R
                       (np.deg2rad(-140), np.deg2rad(90)))    # R

    def __init__(self):
        super().__init__(BarretWAM_4._manipName, BarretWAM_4._manipDOF, BarretWAM_4._manipJointTypes, BarretWAM_4._manipJointLims)

    class Joints(Joints):
        def __init__(self, q1 = None, q2 = None, q3 = None, q4 = None):
            super().__init__(BarretWAM_4._manipDOF)
            self[0] = q1
            self[1] = q2
            self[2] = q3
            self[3] = q4

        def __setitem__(self, index, qx):
            if qx == None:
                return
            elif qx >= BarretWAM_4._manipJointLims[index][0] and qx <= BarretWAM_4._manipJointLims[index][1]:
                self._joints[index] = qx
            else:
                raise ValueError()

        def __str__(self):
            string = "(" 
            for joint, jointType in zip(self._joints, BarretWAM_4._manipJointTypes):
                jointFormatted = ""
                if jointType:
                    jointFormatted += str(round(np.rad2deg(joint), 2))
                else:
                    jointFormatted += str(round(joint, 2))
                string += jointFormatted + " ; "
            string = string.removesuffix(" ; ")
            string += ")"
            return string

    _la = 0.55
    _lb = 0
    _lc = 0.35

    def isInWorkspace(self, point:Point):
        return True               ########## DRAMIN DPS COLOCA UMA FUNCAO AQUI QUE VE SE O PONTO TA NO ESPACO DE TRABALHO (retorna boolean)

    def fkine(self, jointVals:Joints):
       px = BarretWAM_4._la*np.cos(jointVals[0])*np.sin(jointVals[1]) - BarretWAM_4._lc*np.cos(jointVals[3])*(np.sin(jointVals[0])*np.sin(jointVals[2]) - np.cos(jointVals[0])*np.cos(jointVals[1])*np.cos(jointVals[2])) - BarretWAM_4._lc*np.cos(jointVals[0])*np.sin(jointVals[1])*np.sin(jointVals[3])
       py = BarretWAM_4._lc*np.cos(jointVals[3])*(np.cos(jointVals[0])*np.sin(jointVals[2]) + np.cos(jointVals[1])*np.cos(jointVals[2])*np.sin(jointVals[0])) + BarretWAM_4._la*np.sin(jointVals[0])*np.sin(jointVals[1]) - BarretWAM_4._lc*np.sin(jointVals[0])*np.sin(jointVals[1])*np.sin(jointVals[3])
       pz = BarretWAM_4._la*np.cos(jointVals[1]) - BarretWAM_4._lc*np.cos(jointVals[1])*np.sin(jointVals[3]) - BarretWAM_4._lc*np.cos(jointVals[2])*np.cos(jointVals[3])*np.sin(jointVals[1])
       
       return Point(px,py,pz)

    def ikine(self, point:Point):
        q1 = np.arctan2(point.y, point.x)
        q3 = 0
        q4 = np.arcsin(((point.x*np.cos(q1) + point.y*np.sin(q1))**2 + (-point.z)**2 - BarretWAM_4._lc**2 - BarretWAM_4._la**2)/(-2*BarretWAM_4._la*BarretWAM_4._lc))
        
        sin_q2 = ((BarretWAM_4._la - BarretWAM_4._lc*np.sin(q4))*(point.x*np.cos(q1) + point.y*np.sin(q1))/(BarretWAM_4._lc*np.cos(q4)) - point.z)/((BarretWAM_4._la - BarretWAM_4._lc*np.sin(q4))**2/(BarretWAM_4._lc*np.cos(q4)) + BarretWAM_4._lc*np.cos(q4))
        cos_q2 = (point.x*np.cos(q1) + point.y*np.sin(q1) - (BarretWAM_4._la - BarretWAM_4._lc*np.sin(q4))*sin_q2)/(BarretWAM_4._lc*np.cos(q4))
        q2 = np.arctan2(sin_q2, cos_q2)
        
        return BarretWAM_4.Joints(q1, q2, q3, q4)