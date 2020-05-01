from   functions.functions import *
import matplotlib.pyplot as plt
import time



start = [node(0,0)]
goal = [node(100,100)]
#start = [node(0,0), node(100,0)]
#goal = [node(100,100), node(0,100)]


ax = plt.gca()
ax.cla()
ax.set_xlim((-5, 105))
ax.set_ylim((-5, 105))
stepx = 3
stepy = 3

safesize = 10


obstaclelist = [[node(50,50), 10], [node(30,60), 10], [node(60,30), 10], [node(60,60), 10], [node(60,40), 10], [node(40,70), 10], [node(60,80), 10]]
#obstaclelist = [[node(50,50), 10], [node(65,35), 10], [node(35,65), 10]]
#obstaclelist = [[node(50,50), 20]]
#obstaclelist = []

drones = []
for i in range(len(start)):
    drones.append(drone(start[i], goal = goal[i], safesize = safesize, obstaclelist = obstaclelist))
finish = 0
s = 0
start_time = time.time()

while finish < len(drones):
    for l in range(len(drones)):

        if drones[l].reached == True:

            pass
        else:
            gsrate = 100
            k = True
            while k == True:

                randomnode = get_random_node(minRandX = 0, maxRandX = 100, minRandY = 0, maxRandY = 100, goalSampleRate = 1, goal = drones[l].goal)
                nearestnode = get_nearest_node(drones[l].nodelist, randomnode)
                newnode = make_step(nearestnode, randomnode, stepx, stepy)

                if check_obstacle(drones[l].safesize, newnode, obstaclelist):
                    gsrate = 0
                    pass
                elif check_drones(drone = drones[l], drones = drones, node = newnode):
                    gsrate = 0
                    pass
                else:
                    newnode.parent = nearestnode
                    drones[l].nodelist.append(newnode)
                    s = s + 1
                    k = False
                    drones[l].check_reached(newnode)
                    if drones[l].reached == True:
                        finish = finish + 1
                        drones[l].nodelist.append(drones[l].goal)



paths = []
distances = []
nodedistances = []
time = time.time() - start_time
colors = ['r', 'b', 'y']


for l in range(len(drones)):
    nodedistance = 0
    for i in range(len(drones[l].nodelist)):
        ax.plot(drones[l].nodelist[i].x, drones[l].nodelist[i].y,marker = 'x', color = 'g')
        if i < len(drones[l].nodelist) - 1:
            nodedistance = nodedistance + node_distance(drones[l].nodelist[i], drones[l].nodelist[i+1])
    nodedistances.append(nodedistance)
    paths.append(generate_final_course(gnode = drones[l].goal, nodelist = drones[l].nodelist))


for i in range(len(paths)):
    distance = 0

    for j in range(len(paths[i])):
        ax.plot(paths[i][j][0], paths[i][j][1], marker ='x', color = colors[i])
        if j< len(paths[i]) - 1:
            distance = distance + node_distance(node1= node(paths[i][j][0], paths[i][j][1]), node2 = node(paths[i][j+1][0], paths[i][j+1][1]))
    distances.append(distance)


circles = []
for i in range(len(obstaclelist)):
    circles.append(plt.Circle((obstaclelist[i][0].x, obstaclelist[i][0].y), obstaclelist[i][1]))
for i in range(len(circles)):
    ax.add_artist(circles[i])
plt.ylabel('m')
plt.xlabel('m')
plt.show()

print("--- %s seconds ---" , time)
print ("nodes generated for this case ", s)
print('graph distance -> ', distances)
print('nodelist distances ->', nodedistances)

