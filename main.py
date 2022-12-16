from trajectoryPlanner import TrajectoryPlanner
from barretwam4 import BarretWAM_4
from point import Point

x1, y1, z1 = [int(x) for x in input("Enter the initial coordinate ").split()]
x2, y2, z2 = [int(x) for x in input("Enter the final coordinate ").split()]

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