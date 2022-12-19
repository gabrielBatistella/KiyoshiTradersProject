from trajectoryPlanner import TrajectoryPlanner
from lineTrajectoryPlanner import LineTrajectoryPlanner
from barretwam4 import BarretWAM_4
from point import Point

############################### INSTANCIATE DESIRED MANIPULATOR ####################################

manipulatorOptions = (BarretWAM_4, ) ### Change here if you want to add more manipulators

inputText = "\n-------------------------------\n"
for manipIndex in range(len(manipulatorOptions)):
    inputText += "(" + str(manipIndex+1) + ") " + manipulatorOptions[manipIndex]._manipName + "\n"
inputText += "Select manipulator: "

whichRobot = 0
while whichRobot not in range(1, len(manipulatorOptions) + 1):
    try:
        whichRobot = int(input(inputText))
        if whichRobot not in range(1, len(manipulatorOptions) + 1):
            print("INVALID Input! Choose again")
    except ValueError:
        print("INVALID Input! Choose again")
        continue

robot = manipulatorOptions[whichRobot-1]()



############################ INSTANCIATE DESIRED TRAJECTORY PLANNER ################################

trajectoryOptions = (TrajectoryPlanner, LineTrajectoryPlanner) ### Change here if you want to add more trajectory types

inputText = "\n-------------------------------\n"
for trajecIndex in range(len(trajectoryOptions)):
    inputText += "(" + str(trajecIndex+1) + ") " + trajectoryOptions[trajecIndex]._trajectoryDescription + "\n"
inputText += "Select trajectory type: "

whichTrajectory = 0
while whichTrajectory not in range(1, len(trajectoryOptions) + 1):
    try:
        whichTrajectory = int(input(inputText))
        if whichTrajectory not in range(1, len(trajectoryOptions) + 1):
            print("INVALID Input! Choose again")
    except ValueError:
        print("INVALID Input! Choose again")
        continue

planner = trajectoryOptions[whichTrajectory-1](robot)



############################## INPUT POINTS AND CALCULATE TRAJECTORY ################################

ret = False
while not ret:
    print("\n-------------------------------\n")
    pointIndex = 1
    pathPoints = []
    while True:
        point = None
        inWorkspace = False
        while not inWorkspace:
            point = None
            coords = input("Enter the coordinates for point" + str(pointIndex) + " (F to finish inputting points): ")
            if coords == "F":
                break
            try:
                x, y, z = [float(c) for c in coords.split()]
            except ValueError:
                print("INVALID Input! Enter again\n")
                continue

            point = Point(x, y, z)
            inWorkspace = robot.isInWorkspace(point)
            if not inWorkspace:
                print("Point chosen is OUTSIDE the Workspace!! Choose again\n")

        if point == None:
            break
        pointIndex += 1
        pathPoints.append(point)

    try:
        ret, coeffs, durations = planner.trajectoryThroughPoints(pathPoints)
    except ValueError as e:
        print(e)

    if ret:
        values, time = planner.curvesValues(coeffs, durations)
        planner.drawJointCurves(values, time)
        planner.drawTrajectory(values, time, pathPoints)