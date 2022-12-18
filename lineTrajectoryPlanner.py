from math import ceil
from point import Point
from manipulator import Manipulator
from trajectoryPlanner import TrajectoryPlanner

class LineTrajectoryPlanner(TrajectoryPlanner):
    """ 
    A class to calculate the linear trajectory of the end-effector of given manipulator

    ...

    Attributes
    ----------
    manip : Manipulator
        manipulator for which the linear trajectory will be calculated
    
    Methods
    -------
    trajectoryThroughPoints(pathPoints):
        Calculates a linear trajectory for the end-effector through each pair of points in pathPoints.
    curvesValues(allCoeffs, times):
        Calculates values in time of joint values curve for given polynomial coefficients and curve durations.
    drawJointCurves(values, timeVector):
        Plots the curves of joint values x time for given values in time.
    drawTrajectory(values, timeVector, pointsToMark=None):
        Plots the trajectory of end-effector in 3D based on the joint values in time. Also highlights the start and end points of the trajectory. 
        If the argument pointsToMark is given, then highlights the points in pointsToMark.
    """

    _trajectoryDescription = "Linear trajectories through points"
    _maxDistanceBetweenPointsInLine = 0.05

    def __init__(self, manip : Manipulator):
        super().__init__(manip)

    def trajectoryThroughPoints(self, pathPoints:tuple[Point]):
        """
        Calculates a linear trajectory for the end-effector through each pair of points in pathPoints.
        Aproximates a linear trajectory by dividing the path from the starting point to the end point of each pair into some number of smaller paths (by defining intermediate points).
        The intermediate points are defined so that they are not spaced further than a pre-defined max distance
        After defining intermediate points, the trajectory is calculated normally:
            Defines a 3rd degree polynomial trajectory between the 2 points in each pair of points.
            Every trajectory is defined to have continuous acceleration and speed curves.
            By joining all of the curves, the total trajectory through all points is defined to have initial and final speeds of zero.
        
        Parameters
        ----------
        pathPoints:tuple[Point]
            points to create end-effector's linear trajectory.
        
        Returns
        -------
        succeeded : bool
            Whether the operation succeeded (fails when desired trajectory goes out of workspace).
        coeffs : tuple[tuple[tuple[float]]]
            Polynomial coefficients for each curve of each joint.
        times : tuple[float]
            Duration of each curve.
        """

        if len(pathPoints) < 2:
            raise ValueError("Needs at least 2 points to calculate trajectory")

        pathPointsWithIntermediate = [pathPoints[0]]
        for pointIndex in range(1, len(pathPoints)):
            intemerdiatePoints = self._defineIntermediatePoints(pathPoints[pointIndex-1], pathPoints[pointIndex])
            pathPointsWithIntermediate += [*intemerdiatePoints, pathPoints[pointIndex]]

        return super().trajectoryThroughPoints(pathPointsWithIntermediate)

    def _defineIntermediatePoints(self, startPoint, endPoint):
        numberOfIntermediatePoints = ceil(((endPoint - startPoint).dist())/LineTrajectoryPlanner._maxDistanceBetweenPointsInLine) - 1
        intermediatePoints = []

        if numberOfIntermediatePoints > 0:
            displacementBetweenPoints = (endPoint - startPoint)/(numberOfIntermediatePoints + 1)
            for pointIndex in range(numberOfIntermediatePoints):
                nextPoint = startPoint + (pointIndex + 1)*displacementBetweenPoints
                intermediatePoints.append(nextPoint)

        return intermediatePoints
