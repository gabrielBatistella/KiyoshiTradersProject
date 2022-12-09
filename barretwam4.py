# Código de cinemática inversa para o manipulador Barrett-WAM com 4 graus de liberdade
# 4 juntas rotativas
# Cinemática Inversa calculada manualmente

import numpy as np
from point import Point
from joints import Joints
from manipulator import Manipulator

class BarretWAM_4(Manipulator):
    manipName = "Barret-WAM (4 DOF)"
    manipDOF = 4
    manipJointTypes = (True, True, True, True)      # Tupla de boolean (True = Rotativa ; False = Prismática)   :   RRRR

    def __init__(self):
        super().__init__(BarretWAM_4.manipName, BarretWAM_4.manipDOF, BarretWAM_4.manipJointTypes)

    class Joints(Joints):
        def __init__(self, q1 = None, q2 = None, q3 = None, q4 = None):
            super().__init__(BarretWAM_4.manipDOF, BarretWAM_4.manipJointTypes)
            self[0] = q1
            self[1] = q2
            self[2] = q3
            self[3] = q4

        @classmethod
        @property
        def qLim(cls):
            return ((np.deg2rad(-150), np.deg2rad(150)),   # R
                    (np.deg2rad(-113), np.deg2rad(113)),   # R
                    (np.deg2rad(-157), np.deg2rad(157)),   # R
                    (np.deg2rad(-140), np.deg2rad(90)))    # R

    la = 0.55
    lb = 0
    lc = 0.35

    def isInWorkspace(self, point:Point):
        return True               ########## DRAMIN DPS COLOCA UMA FUNCAO AQUI QUE VE SE O PONTO TA NO ESPACO DE TRABALHO (retorna boolean)

    def fkine(self, jointVals:Joints):
       px = BarretWAM_4.la*np.cos(jointVals[0])*np.sin(jointVals[1]) - BarretWAM_4.lc*np.cos(jointVals[3])*(np.sin(jointVals[0])*np.sin(jointVals[2]) - np.cos(jointVals[0])*np.cos(jointVals[1])*np.cos(jointVals[2])) - BarretWAM_4.lc*np.cos(jointVals[0])*np.sin(jointVals[1])*np.sin(jointVals[3])
       py = BarretWAM_4.lc*np.cos(jointVals[3])*(np.cos(jointVals[0])*np.sin(jointVals[2]) + np.cos(jointVals[1])*np.cos(jointVals[2])*np.sin(jointVals[0])) + BarretWAM_4.la*np.sin(jointVals[0])*np.sin(jointVals[1]) - BarretWAM_4.lc*np.sin(jointVals[0])*np.sin(jointVals[1])*np.sin(jointVals[3])
       pz = BarretWAM_4.la*np.cos(jointVals[1]) - BarretWAM_4.lc*np.cos(jointVals[1])*np.sin(jointVals[3]) - BarretWAM_4.lc*np.cos(jointVals[2])*np.cos(jointVals[3])*np.sin(jointVals[1])
       
       return Point(px,py,pz)

    def ikine(self, point:Point):
        q1 = np.arctan2(point.y, point.x)
        q3 = 0
        q4 = np.arcsin(((point.x*np.cos(q1) + point.y*np.sin(q1))**2 + (-point.z)**2 - BarretWAM_4.lc**2 - BarretWAM_4.la**2)/(-2*BarretWAM_4.la*BarretWAM_4.lc))
        
        sin_q2 = ((BarretWAM_4.la - BarretWAM_4.lc*np.sin(q4))*(point.x*np.cos(q1) + point.y*np.sin(q1))/(BarretWAM_4.lc*np.cos(q4)) - point.z)/((BarretWAM_4.la - BarretWAM_4.lc*np.sin(q4))**2/(BarretWAM_4.lc*np.cos(q4)) + BarretWAM_4.lc*np.cos(q4))
        cos_q2 = (point.x*np.cos(q1) + point.y*np.sin(q1) - (BarretWAM_4.la - BarretWAM_4.lc*np.sin(q4))*sin_q2)/(BarretWAM_4.lc*np.cos(q4))
        q2 = np.arctan2(sin_q2, cos_q2)
        
        return BarretWAM_4.Joints(q1, q2, q3, q4)


robot = BarretWAM_4()
print(robot)
jointVals = robot.ikine(Point(-0.292, 0.38, 0.051))
position = robot.fkine(jointVals)
print(position)
print(jointVals)