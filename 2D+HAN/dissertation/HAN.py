from functions.functions import *
import matplotlib.pyplot as plt
import time
from functions.prmforHAN import path_format, obstaclelist, safesize, stepx, stepy, drones, colors


plt.close("all")
ax = plt.gca()
ax.cla()
ax.set_xlim((-20, 120))
ax.set_ylim((-20, 120))

path = [[] for i in range(len(drones))]

for k in range(len(drones)):
    for i in range(len(path_format[k])):
        path[k].append(node(path_format[k][i][0], path_format[k][i][1]))


a = 1
goal = [None for i in range(len(drones))]
start = [None for i in range(len(drones))]
for i in range(len(path)):
    goal[i] = path[i][a]
    start[i] = path[i][a-1]

circles = []

for i in range(len(obstaclelist)):
    circles.append(plt.Circle((obstaclelist[i][0].x, obstaclelist[i][0].y), obstaclelist[i][1]))
for i in range(len(circles)):
    ax.add_artist(circles[i])




x = [[] for i in range(len(drones))]
y = [[] for i in range(len(drones))]
nodelist = [[start[i]] for i in range(len(drones))]
newnode = [[start[i]] for i in range(len(drones))]
for i in range(len(path)):
    for j in range(len(path[i])):
        x[i].append(path[i][j].x)
        y[i].append(path[i][j].y)


plt.plot(x[0],y[0], color = 'r')
plt.plot(x[1], y[1], color='y')
start_time = time.time()

a = [1 for i in range(len(drones))]
finish = [False for i in range(len(drones))]

gsrate = 100
minRandX = [0 for i in range(len(drones))]
minRandY = [0 for i in range(len(drones))]
maxRandX = [105 for i in range(len(drones))]
maxRandY = [105 for i in range(len(drones))]
while True:
    if all(finish) : break

    for i in range(len(drones)):

        randomnode = get_random_node(minRandX = minRandX[i], maxRandX = maxRandX[i], minRandY = minRandY[i] , maxRandY = maxRandY[i], goalSampleRate = gsrate, goal = goal[i])
        print('goal ->', goal[i].x, goal[i].y)
        print('random node -> ',randomnode.x, randomnode.y)
        try :newnode[i][0] = make_step(newnode[i][0], randomnode, stepx, stepy)
        except ZeroDivisionError : newnode[i][0] = goal[i]

        if check_obstacle(safesize, newnode[i][0], obstaclelist):
            gsrate = 0
            minRandX[i] = int(min(drones[i].position.x, goal[i].x))
            maxRandX[i] = int(max(drones[i].position.x, goal[i].x)) + 5
            minRandY[i] = int(min(drones[i].position.y, goal[i].y))
            maxRandY[i] = int(max(drones[i].position.y, goal[i].y)) + 5
            pass
        elif check_drones(drone=drones[i], drones=drones, node=newnode[i][0]):
            gsrate = 0
            minRandX[i] = int(min(drones[i].position.x, goal[i].x))
            maxRandX[i] = int(max(drones[i].position.x, goal[i].x)) + 5
            minRandY[i] = int(min(drones[i].position.y, goal[i].y))
            maxRandY[i] = int(max(drones[i].position.y, goal[i].y)) + 5
            pass
        else:
            newnode[i][0].parent = nodelist[i][len(nodelist[i]) - 1]
            nodelist[i].append(newnode[i][0])
            drones[i].position = newnode[i][0]
            gsrate = 100
            if node_distance(node1 = newnode[i][0],node2 = goal[i]) <= safesize :#- math.sqrt(stepx**2 + stepy**2) :
                newnode[i][0] = goal[i]
                nodelist[i].append(goal[i])
                drones[i].position = newnode[i][0]
                a[i] = a[i] + 1


                if a[i]  >= len(path[i]):
                    goal[i] = path[i][len(path[i]) - 1]
                    finish[i] = True
                else :
                    goal[i] = path[i][a[i]]

        plt.plot(newnode[i][0].x, newnode[i][0].y, marker='o', color=colors[i])
        plt.pause(0.0001)




plt.pause(5)
plt.show(block = False)
plt.close('all')

