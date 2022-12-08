# Código de cinemática inversa para o manipulador Barrett-WAM com 4 graus de liberdade
# 4 juntas rotativas
# Cinemática Inversa calculada manualmente

import numpy as np
from point import Point
from manipulator import Manipulator

class BarretWAM_4(Manipulator):
    manipName = "Barret-WAM (4 DOF)"
    manipDOF = 4
    manipJointTypes = (True, True, True, True)      # Tupla de boolean (True = Rotativa ; False = Prismática)

    class Joints:
        q_lim = np.deg2rad(((0, 360), (0, 360), (0, 360), (0, 360)))    ########### DRAMIN DPS COLOCA OS LIMITES DE CADA JUNTA PF

        def __init__(self, q1 = None, q2 = None, q3 = None, q4 = None):
            self._joints = [None, None, None, None]
            self[0] = q1
            self[1] = q2
            self[2] = q3
            self[3] = q4

        def __getitem__(self, index):
            return self._joints[index]

        def __setitem__(self, index, qx):
            if qx == None:
                return
            elif qx >= BarretWAM_4.Joints.q_lim[index][0] and qx <= BarretWAM_4.Joints.q_lim[index][1]:
                self._joints[index] = qx
            else:
                raise ValueError()

        def __iter__(self):
            return iter(self._joints)

        def __str__(self):
            string = "(" 
            for joint in self._joints:
                joint_deg = round(np.rad2deg(joint), 2)
                string += str(joint_deg) + " ; "
            string = string.removesuffix(" ; ")
            string += ")"
            return string

    la = 0.55
    lb = 0
    lc = 0.35

    def __init__(self):
        super().__init__(BarretWAM_4.manipName, BarretWAM_4.manipDOF, BarretWAM_4.manipJointTypes)

    def fkine(self, jointVals : Joints):
        pass        ######## DRAMIN COLOCA AQUI A CINEMATICA DIRETA PF kkkkkkkkkk (SO DA TRANSLACAO MSM, A SAIDA EH UM POINT)

    def ikine(self, point : Point):
        q1 = np.arctan2(point.y, point.x)
        q3 = 0
        q4 = np.arcsin(((point.x*np.cos(q1) + point.y*np.sin(q1))**2 + (-point.z)**2 - BarretWAM_4.lc**2 - BarretWAM_4.la**2)/(-2*BarretWAM_4.la*BarretWAM_4.lc))
        
        c1 = BarretWAM_4.lc*np.cos(q4)
        c2 = BarretWAM_4.la - BarretWAM_4.lc*np.sin(q4)
        c3 = point.x*np.cos(q1) + point.y*np.sin(q1)
        c4 = -point.z
        sin_q2 = ((c4 + c2*c3/c1)/(c2*c2/c1 + c1))
        cos_q2 = (c3-c2*sin_q2)/c1
        
        q2 = np.arctan2(sin_q2, cos_q2)
        
        return BarretWAM_4.Joints(q1, q2, q3, q4)


robot = BarretWAM_4()
print(robot)
jointVals = robot.ikine(Point(-0.292, 0.38, 0.051))
print(jointVals)
jointVals[0] = np.deg2rad(30)
print(jointVals)
jointVals[2] = jointVals[1]
print(jointVals)
#jointVals[0] = np.deg2rad(361)  ## DA ERRO PQ TA FORA DO LIMITE (TESTE)
#jointVals2 = BarretWAM_4.Joints(0, 3, 0, np.deg2rad(361))   ## DA ERRO PQ TA FORA DO LIMITE (TESTE)