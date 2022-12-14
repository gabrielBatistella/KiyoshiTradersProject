from math import radians, degrees, cos, sin, asin, atan2
from point import Point
from joints import Joints_
from manipulator import Manipulator

class BarretWAM_4(Manipulator):
    """ 
    A class to represent the Barret WAM manipulator with 4 DOF

    ...

    Attributes
    ----------
    name : string
        name of the manipulator (Barret-WAM (4 DOF))
    dof : int
        Barret-WAM's number of degrees of freedom (4)
    jointTypes : tuple[bool]
        indicates the type of the joints ; True = rotative, False = prismatic (RRRR)
    jointLims : tuple[tuple[float]]
        indicates the limits of the joints ((-150, 150), (-113, 113), (-157, 157), (-140, 90))
    speed : float
        avarage speed of the Barret-WAM's end-effector
    
    Methods
    -------
    isInWorkspace(point):
        Verify if the given point is inside of the Barret-WAM's workspace.
        If argument is a iterable, verify all points.
    fkine(jointVals):
        Calculates the Barret-WAM's end-effector position in the space for given joint values - forward kinematics.
        If argument is a iterable, apply method to all values.
    ikine(point):
        Calculates the Barret-WAM's joint values for given end-effector position in the space - inverse kinematics.
        If argument is a iterable, apply method to all points.

    Inner Class
    -----------
    Joints:
        A structure that stores the Barret-WAM's joint values.

    Implemented Operations
    ----------------------
    str : string = str(BarretWAM_4)
        S = "Barret-WAM (4 DOF)".
    """

    _manipName = "Barret-WAM (4 DOF)"
    _manipDOF = 4
    _manipJointTypes = (True, True, True, True)
    _manipJointLims = ((radians(-150), radians(150)),
                       (radians(-113), radians(113)),
                       (radians(-157), radians(157)),
                       (radians(-140), radians(90)))

    def __init__(self):
        super().__init__(BarretWAM_4._manipName, BarretWAM_4._manipDOF, BarretWAM_4._manipJointTypes, BarretWAM_4._manipJointLims)

    class Joints(Joints_):
        """ 
        A class to represent the Barret-WAM's joint values.

        ...

        Attributes
        ----------
        joints : list[float]
            Barret-WAM's joint values, only accepts values within limits.

        Implemented Operations
        ----------------------
        getItem : float|int = Joints[int]
            val = joints[idx].
        setItem : Joints[int] = float|int
            joints[idx] = val (only accepts values within limits).
        iterator : Iterator = iter(Joints)
            iter = joints (iterates over the joint values).
        str : string = str(Joints)
            S = "(joints[0] ; joints[1] ; joints[2] ; joints[3])".
        """

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
                raise ValueError("Joint values are outside of workspace!")

        def __str__(self):
            string = "(" 
            for joint, jointType in zip(self._joints, BarretWAM_4._manipJointTypes):
                jointFormatted = ""
                if jointType:
                    jointFormatted += str(round(degrees(joint), 2)) + "??"
                else:
                    jointFormatted += str(round(joint, 2)) + "m"
                string += jointFormatted + " ; "
            string = string.removesuffix(" ; ")
            string += ")"
            return string

    _la = 0.55
    _lb = 0
    _lc = 0.35

    def isInWorkspace(self, point):
        """
        Verifies if the given point is inside of the Barret-WAM's workspace.
        If argument is a iterable, verify all points.
        
        Parameters
        ----------
        point : Point | Iterable[Point]
            x, y and z coordinates of a point in 3D space for the end-effector.

        Returns
        -------
        isInWorkspace : bool
            Whether given point(s) is(are) inside of the workspace.
        """

        try:
            self.ikine(point)
            return True
        except ValueError:
            return False

    def fkine(self, jointVals):
        """
        Calculates the Barret-WAM's end-effector position in the space for given joint values - forward kinematics.
        If argument is a iterable, apply method to all values.

        Parameters
        ----------
        jointVals : BarretWAM_4.Joints | Iterable[BarretWAM_4.Joints]
            Barret-WAM's joint values.

        Returns
        -------
        point : Point | Iterable[Point]
            x, y and z coordinates of point(s) in 3D space for the Barret-WAM's end-effector given values.
        """

        if type(jointVals) == BarretWAM_4.Joints:
            px = BarretWAM_4._la*cos(jointVals[0])*sin(jointVals[1]) - BarretWAM_4._lc*cos(jointVals[3])*(sin(jointVals[0])*sin(jointVals[2]) - cos(jointVals[0])*cos(jointVals[1])*cos(jointVals[2])) - BarretWAM_4._lc*cos(jointVals[0])*sin(jointVals[1])*sin(jointVals[3])
            py = BarretWAM_4._lc*cos(jointVals[3])*(cos(jointVals[0])*sin(jointVals[2]) + cos(jointVals[1])*cos(jointVals[2])*sin(jointVals[0])) + BarretWAM_4._la*sin(jointVals[0])*sin(jointVals[1]) - BarretWAM_4._lc*sin(jointVals[0])*sin(jointVals[1])*sin(jointVals[3])
            pz = BarretWAM_4._la*cos(jointVals[1]) - BarretWAM_4._lc*cos(jointVals[1])*sin(jointVals[3]) - BarretWAM_4._lc*cos(jointVals[2])*cos(jointVals[3])*sin(jointVals[1])
            return Point(px,py,pz)

        elif type(jointVals) == tuple or type(jointVals) == list:
            pointsVec = []
            for thisJointVals in jointVals:
                thisPoint = self.fkine(thisJointVals)
                pointsVec.append(thisPoint)
            return pointsVec

        else:
            raise TypeError("fkine can only operate on Joints, tuple[Joints] or list[Joints]")

    def ikine(self, point):
        """
        Calculates the Barret-WAM's joint values for given end-effector position in the space - inverse kinematics.
        If argument is a iterable, apply method to all points.

        Parameters
        ----------
        point : Point | Iterable[Point]
            x, y and z coordinates of point(s) in 3D space for the end-effector.

        Returns
        -------
        jointVals : BarretWAM_4.Joints | Iterable[BarretWAM_4.Joints]
            Barret-WAM's joint values for the given point.
        """

        if type(point) == Point:
            q1 = atan2(point.y, point.x)
            q3 = 0
            q4 = asin(((point.x*cos(q1) + point.y*sin(q1))**2 + (-point.z)**2 - BarretWAM_4._lc**2 - BarretWAM_4._la**2)/(-2*BarretWAM_4._la*BarretWAM_4._lc))
            sin_q2 = ((BarretWAM_4._la - BarretWAM_4._lc*sin(q4))*(point.x*cos(q1) + point.y*sin(q1))/(BarretWAM_4._lc*cos(q4)) - point.z)/((BarretWAM_4._la - BarretWAM_4._lc*sin(q4))**2/(BarretWAM_4._lc*cos(q4)) + BarretWAM_4._lc*cos(q4))
            cos_q2 = (point.x*cos(q1) + point.y*sin(q1) - (BarretWAM_4._la - BarretWAM_4._lc*sin(q4))*sin_q2)/(BarretWAM_4._lc*cos(q4))
            q2 = atan2(sin_q2, cos_q2)
            return BarretWAM_4.Joints(q1, q2, q3, q4)

        elif type(point) == tuple or type(point) == list:
            jointValsVec = []
            for thisPoint in point:
                thisJointVals = self.ikine(thisPoint)
                jointValsVec.append(thisJointVals)
            return jointValsVec

        else:
            raise TypeError("ikine can only operate on Point, tuple[Point] or list[Point]")