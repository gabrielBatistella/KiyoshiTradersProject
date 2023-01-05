import linalg
from point import Point
from manipulator import Manipulator

class TrajectoryPlanner:
    """ 
    A class to calculate the trajectory of the end-effector of given manipulator

    ...

    Attributes
    ----------
    manip : Manipulator
        manipulator for which the trajectory will be calculated
    
    Methods
    -------
    trajectoryThroughPoints(pathPoints):
        Calculates a trajectory for the end-effector through all the points in pathPoints.
    curvesValues(allCoeffs, times):
        Calculates values in time of joint values curve for given polynomial coefficients and curve durations.
    """

    _trajectoryDescription = "Curved trajectory through points"
    _numberOfPointsPerStepForCurveDrawing = 100

    def __init__(self, manip):
        self._manip = manip

    def trajectoryThroughPoints(self, pathPoints):
        """
        Calculates a trajectory for the end-effector through all the points in pathPoints.
        Defines a 3rd degree polynomial trajectory between the 2 points in each pair of points.
        Every trajectory is defined to have continuous acceleration and speed curves.
        By joining all of the curves, the total trajectory through all points is defined to have initial and final speeds of zero.

        Parameters
        ----------
        pathPoints:tuple[Point]
            points to create end-effector's trajectory.
        
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

    def curvesValues(self, allCoeffs, times):
        """
        Calculates values in time of joint values curve for given polynomial coefficients and curve durations.
        
        Parameters
        ----------
        allCoeffs:tuple[tuple[tuple[float]]]
            curves coefficients to create values in time of joint values
        times:tuple[float]
            duration of each curve
        
        Returns
        -------
        allValues : tuple[float]
            Values of each joint values.
        timeVector : tuple[float]
            Times of each joint values. 
        """

        formattedTimes = [0]
        for timeIndex in range(len(times)):
            formattedTimes.append(formattedTimes[timeIndex] + times[timeIndex])

        timeVector = []
        formattedTimeVector = []
        for timeIndex in range(len(times)):
            if timeIndex == len(times) - 1:
                t = linalg.linspace(formattedTimes[timeIndex], formattedTimes[timeIndex+1], TrajectoryPlanner._numberOfPointsPerStepForCurveDrawing + 1, endIncluded=True)
            else:
                t = linalg.linspace(formattedTimes[timeIndex], formattedTimes[timeIndex+1], TrajectoryPlanner._numberOfPointsPerStepForCurveDrawing, endIncluded=False)
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
        x = linalg.solve_equations(A, b)
        coeffs = [None] * numberOfCurves
        for curveIndex in range(numberOfCurves):
            coeffs[curveIndex] = [coeff[0] for coeff in x[4*curveIndex : 4*(curveIndex+1)]]

        return coeffs

    def _linearSystem(self, numberOfCurves, values, times):
        A = linalg.zeros_matrix(4*numberOfCurves, 4*numberOfCurves)
        b = linalg.zeros_matrix(4*numberOfCurves, 1)

        for index in range(numberOfCurves):
            A[4*index + 1][4*index] = 1
            A[4*index + 2][4*index] = 1
            A[4*index + 2][4*index + 1] = times[index]
            A[4*index + 2][4*index + 2] = times[index]**2
            A[4*index + 2][4*index + 3] = times[index]**3
            A[4*index + 3][4*index + 1] = 1
            A[4*index + 3][4*index + 2] = 2*times[index]
            A[4*index + 3][4*index + 3] = 3*times[index]**2
            b[4*index + 1][0] = values[index]
            b[4*index + 2][0] = values[index+1]

        for index in range(numberOfCurves-1):
            A[4*index + 3][4*index + 5] = -1
            A[4*index + 4][4*index + 2] = 2
            A[4*index + 4][4*index + 3] = 6*times[index]
            A[4*index + 4][4*index + 6] = -2

        A[0][1] = 1

        return A, b