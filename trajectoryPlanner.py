# Código do planejador de trajetória
# Calcula trajetórias com polinômios do 3º grau

import numpy as np
import matplotlib.pyplot as plt
from math import ceil
from point import Point
from manipulator import Manipulator

from barretwam4 import BarretWAM_4

class TrajectoryPlanner:
    """ 
    A class to calculate the trajectory of the end-effector of given manipulator

    ...

    Attributes
    ----------
    manip : Manipulator
        manipulator to which will be given the trajectory
    
    Methods
    -------
    lineBetweenPoints(startPoint, endPoint):
        Calculates a linear trajectory for the end-effector between two points.
    curvesValues(allCoeffs, times):
        Calculates points of joint values curve for given polynomial coefficients.
    drawJointCurves(values, timeVector):
        Plots the curves of joint values x time for given points in the curve.
    drawTrajectory(values, timeVector, pointsToMark):
        Plots the trajectory of end-effector in 3D.
    """
    _maxDistanceBetweenPointsInLine = 0.1
    _numberOfPointsPerStepForCurveDrawing = 100

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

        coeffs = [None] * self._manip.dof
        times = [0] * (len(pathPoints) - 1)
        if not self._manip.isInWorkspace(pathPoints):
            print("Trajectory goes OUTSIDE the Workspace!!")
            return False, coeffs, times

        formattedPathJointVals = self._calculateJointValuesOnPathPoints(pathPoints)
        times = self._estimateTrajectoryStepsDuration(pathPoints)

        for jointIndex in range(self._manip.dof):
            coeffs[jointIndex] = self._polynomialCurvesThroughJointValues(formattedPathJointVals[jointIndex], times)

        return True, coeffs, times

    def curvesValues(self, allCoeffs:tuple[tuple[float]], times:tuple[float]):
        formattedTimes = [0]
        for timeIndex in range(len(times)):
            formattedTimes.append(formattedTimes[timeIndex] + times[timeIndex])

        timeVector = []
        formattedTimeVector = []
        for timeIndex in range(len(times)):
            if timeIndex == len(times) - 1:
                t = np.linspace(formattedTimes[timeIndex], formattedTimes[timeIndex+1], TrajectoryPlanner._numberOfPointsPerStepForCurveDrawing + 1, endpoint=True)
            else:
                t = np.linspace(formattedTimes[timeIndex], formattedTimes[timeIndex+1], TrajectoryPlanner._numberOfPointsPerStepForCurveDrawing, endpoint=False)
            timeVector += [*t]
            formattedTimeVector.append(t)

        allValues = [None] * self._manip.dof
        for jointIndex in range(len(allCoeffs)):
            allValues[jointIndex] = []
            for curveIndex in range(len(allCoeffs[jointIndex])):
                for time in formattedTimeVector[curveIndex]:
                    coeffs = allCoeffs[jointIndex][curveIndex]
                    t = time - formattedTimes[curveIndex]
                    value = coeffs[3]*(t**3) + coeffs[2]*(t**2) + coeffs[1]*(t) + coeffs[0]
                    allValues[jointIndex].append(value)

        return allValues, timeVector

    def drawJointCurves(self, values:tuple[tuple[float]], timeVector:tuple[float]):
        fig, axs = plt.subplots(2, 2)

        for jointIndex in range(len(values)):
            jointValues = None
            ylabel = ""
            if self._manip.jointTypes[jointIndex]:
                jointValues = np.rad2deg(values[jointIndex])
                ylabel = "Angle (º)"
            else:
                jointValues = np.array(values[jointIndex])
                ylabel = "Length (m)"

            axs[jointIndex//2, jointIndex%2].plot(timeVector, jointValues)
            axs[jointIndex//2, jointIndex%2].set_title("Joint" + str(jointIndex+1))
            axs[jointIndex//2, jointIndex%2].set(xlabel = "Time (s)", ylabel = ylabel)
            axs[jointIndex//2, jointIndex%2].grid()

        plt.tight_layout()
        plt.show()

    def drawTrajectory(self, values:tuple[tuple[float]], timeVector:tuple[float], pointsToMark:tuple[Point] = None):
        formattedValues = []
        for timeIndex in range(len(timeVector)):
            formattedValues.append(self._manip.Joints(*[values[jointIndex][timeIndex] for jointIndex in range(self._manip.dof)]))
        
        pathPoints = self._manip.fkine(tuple(formattedValues))

        fig = plt.figure
        axs = plt.axes(projection="3d")
        axs.plot3D([point.x for point in pathPoints], [point.y for point in pathPoints], [point.z for point in pathPoints])
        if pointsToMark == None:
            pointsToMark = (pathPoints[0], pathPoints[-1])
        for point in pointsToMark:
            axs.scatter(point.x, point.y, point.z, color="red")
            axs.text(point.x, point.y, point.z, str(point), color="red")
        axs.set_title("Trajectory")
        axs.set(xlabel = "x (m)", ylabel = "y (m)", zlabel = "z (m)")
        plt.tight_layout
        plt.show()

    def _calculateJointValuesOnPathPoints(self, pathPoints):
        pathJointVals = self._manip.ikine(pathPoints)
        formattedPathJointVals = [None] * self._manip.dof
        for jointIndex in range(self._manip.dof):
            formattedPathJointVals[jointIndex] = [jointVals[jointIndex] for jointVals in pathJointVals]

        return formattedPathJointVals

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

point1 = Point(0.35, 0.0, 0.55)
point2 = Point(-0.292, 0.38, 0.051)
point3 = Point(0.2, 0.1, -0.1)

ret, coeffs, durations = planner.lineBetweenPoints(point1, point2)

if ret:
    values, time = planner.curvesValues(coeffs, durations)
    planner.drawJointCurves(values, time)
    planner.drawTrajectory(values, time)