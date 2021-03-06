from MAIN.node.node import node
import random
import math
from MAIN.input.input import droneSize
from heapq import nsmallest
def get_random_node(goalSampleRate, goalNode,
                    minRandx, maxRandx, minRandy, maxRandy, minRandz, maxRandz):
    a = True

    goalProbability = random.randint(1,100)

    if goalSampleRate <= goalProbability:
        x = random.randint(minRandx, maxRandx)
        y = random.randint(minRandy, maxRandy)
        z = random.randint(minRandz, maxRandz)
        randomNode = node(x, y, z)

        return randomNode
    else:
        randomNode = goalNode
        return randomNode


def check_nearest(nodeList, node1):
    minDistance = float("inf")
    minDistanceNumber = None
    for i in range(len(nodeList)):

        distance = node_distance(node1 = node1, node2 = nodeList[i])
        if distance <= minDistance:
            minDistance = distance
            minDistanceNumber = i

    node1.nearest = nodeList[minDistanceNumber]


def node_distance(node1, node2):
    dx = node1.x - node2.x
    dy = node1.y - node2.y
    dz = node1.z - node2.z

    distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    return distance

def make_step(nodef, nodet, stepx, stepy, stepz):

    dx = nodet.x - nodef.x
    dy = nodet.y - nodef.y
    dz = nodet.z - nodef.z

    r = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    xx = dx * (stepx / r)
    yy = dy * (stepy / r)
    zz = dz * (stepz / r)
    newnode = node(nodef.x + xx, nodef.y + yy, nodef.z + zz)

    return newnode

def node_obstacle_collision(node1, obstacles):
    a = None
    for i in range(len(obstacles)):
        if node_distance(obstacles[i][0], node1) <= obstacles[i][1] + droneSize :
            return True
        else:
            a = False
    return a

def generate_final_course(gnode, nodelist):
    """
           Generates final course
    """
    path = [[gnode.x, gnode.y, gnode.z]]
    node = nodelist[len(nodelist) - 2]
    while node.parent is not None:
        path.append([node.x, node.y, node.z])
        node = node.parent
    path.append([node.x, node.y, node.z])

    return path

def drone_collision(drone, node1):
    for j in range(len(drone.recipents)):
        if node_distance(node1 = drone.recipents[j].position, node2= node1)<= drone.size + drone.recipents[j].size:
            return True
    return False

def get_random_nodes(point,radius, obstacles):
    nodes = []
    for i in range(100):
        nodes.append(get_random_node(goalSampleRate=0, goalNode=node(0,0,0), obstacles = obstacles,
                                     minRandx=int(point.x) - radius, maxRandx= int(point.x) + radius,
                                     minRandy= int(point.y) - radius, maxRandy=int(point.y) + radius,
                                     minRandz = int(point.z) - radius, maxRandz = int(point.z) + radius))

    return nodes

def draw_line(start,end,size):
    line = [start]
    i = 0
    while node_distance(line[i],end) >= size :
        line.append(make_step(nodef = line[i], nodet = end, stepx = size, stepy = size, stepz = size))
        i = i + 1
    return line

def get_interception_point(line1, line2, size1, size2):
    for j in range(len(line1)):
        for k in range(len(line2)):
            if node_distance(node1 = line1[j], node2 = line2[k]) <= size1 + size2 : return line1[j]

    return node(-666,-500,-500)




