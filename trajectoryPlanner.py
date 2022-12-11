# Código do planejador de trajetória
# Calcula trajetórias com polinômios do 3º grau

import numpy as np
from math import ceil
from point import Point
from manipulator import Manipulator

from barretwam4 import BarretWAM_4

class TrajectoryPlanner:
    _maxDistanceBetweenPointsInLine = 0.1

    def __init__(self, manip : Manipulator):
        self._manip = manip

    def lineBetweenPoints(self, startPoint:Point, endPoint:Point):
        numberOfIntermediatePoints = ceil(((endPoint - startPoint).dist())/TrajectoryPlanner._maxDistanceBetweenPointsInLine) - 1
        intermediatePoints = []

        if numberOfIntermediatePoints > 0:
            displacementBetweenPoints = (endPoint - startPoint)/(numberOfIntermediatePoints + 1)
            for pointIndex in range(numberOfIntermediatePoints):
                nextPoint = startPoint + (pointIndex + 1)*displacementBetweenPoints
                intermediatePoints.append(nextPoint)

        return self.trajectoryThroughPoints((startPoint, *intermediatePoints, endPoint))

    def trajectoryThroughPoints(self, pathPoints:tuple[Point]):
        if len(pathPoints) < 2:
            raise ValueError

        coeffs = [[]] * self._manip.dof
        for point in pathPoints:
            if not self._manip.isInWorkspace(point):
                print("Trajectory goes OUTSIDE the Workspace!!")
                return False, coeffs

        pathJointValsFormatted = self._calculateJointValuesOnPathPoints(pathPoints)
        times = self._estimateTrajectoryStepsDuration(pathPoints)

        for jointIndex in range(self._manip.dof):
            coeffs[jointIndex] = self._polynomialCurvesThroughJointValues(pathJointValsFormatted[jointIndex], times)

        return True, coeffs

    def _calculateJointValuesOnPathPoints(self, pathPoints):
        pathJointVals = []
        for point in pathPoints:
            jointVals = self._manip.ikine(point)
            pathJointVals.append(jointVals)

        pathJointValsFormatted = [[]] * self._manip.dof
        for jointIndex in range(self._manip.dof):
            pathJointValsFormatted[jointIndex] = [jointVals[jointIndex] for jointVals in pathJointVals]

        return pathJointValsFormatted

    def _estimateTrajectoryStepsDuration(self, pathPoints):
        times = [0] * (len(pathPoints) - 1)
        for pointIndex in range(len(pathPoints) - 1):
            distance = (pathPoints[pointIndex + 1] - pathPoints[pointIndex]).dist()
            times[pointIndex] = max((distance/self._manip.speed, 0.1))

        return times

    def _polynomialCurvesThroughJointValues(self, values, times):
        numberOfCurves = len(values) - 1
        
        A, b = self._linearSystem(numberOfCurves, values, times)
        x = np.linalg.solve(A, b)
        coeffs = np.reshape(x, (numberOfCurves, 4))

        return coeffs

    def _linearSystem(self, numberOfCurves, values, times):
        A = np.zeros((4*numberOfCurves, 4*numberOfCurves))
        b = np.zeros(4*numberOfCurves)

        for index in range (0, numberOfCurves):
            A[4*index + 1, 4*index] = 1
            A[4*index + 2, 4*index] = 1
            A[4*index + 2, 4*index + 1] = times[index]
            A[4*index + 2, 4*index + 2] = times[index]**2
            A[4*index + 2, 4*index + 3] = times[index]**3
            A[4*index + 3, 4*index + 1] = 1
            A[4*index + 3, 4*index + 2] = 2*times[index]
            A[4*index + 3, 4*index + 3] = 3*times[index]**2
            b[4*index + 1] = values[index]
            b[4*index + 2] = values[index+1]

        for index in range (0, numberOfCurves-1):
            A[4*index + 3, 4*index + 5] = -1
            A[4*index + 4, 4*index + 2] = 2
            A[4*index + 4, 4*index + 3] = 6*times[index]
            A[4*index + 4, 4*index + 6] = -2

        A[0, 1] = 1

        return A, b

robot = BarretWAM_4()
planner = TrajectoryPlanner(robot)

print(robot.ikine(Point(-0.292, 0.38, 0.051)))
ret, coeffs = planner.lineBetweenPoints(Point(-0.292, 0.38, 0.051), Point(-0.292, 0.38, 0.051))
print(ret)
print(coeffs)