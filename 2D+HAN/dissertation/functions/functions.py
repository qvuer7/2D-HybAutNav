import random
import math
import matplotlib.pyplot as plt
from collections import defaultdict


class node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.parent = None

class drone:
    def __init__(self,start, goal,safesize, obstaclelist):
        self.start = start
        self.goal = goal
        self.position = start
        self.nodelist = [self.start]
        self.safesize =safesize
        self.obstaclelist = obstaclelist
        self.path = None

        if node_distance(self.start, self.goal) <= self.safesize:
            self.reached = True
        else:
            self.reached = False


    def check_reached(self, node):
        if node_distance(node, self.goal) <= self.safesize:
            self.reached = True
        else:
            self.reached = False



def node_distance(node1, node2):
    dx = node1.x - node2.x
    dy = node1.y - node2.y


    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance

def get_random_node(minRandX, maxRandX, minRandY, maxRandY,  goalSampleRate, goal):
    i = random.randint(0,100)
    if i >= goalSampleRate:
        x = random.randint(minRandX, maxRandX)
        y = random.randint(minRandY, maxRandY)
        randomnode = node(x,y)
        return randomnode
    else:
        return goal

def make_step(nodef, nodet, stepx, stepy):

    dx = nodet.x - nodef.x
    dy = nodet.y - nodef.y

    r = math.sqrt(dx ** 2 + dy ** 2)

    xx = dx * (stepx / r)
    yy = dy * (stepy / r)
    newnode = node(nodef.x + xx, nodef.y + yy)

    return newnode


def get_nearest_node(nodelist, node):
    minDistance = float("inf")
    nearestNode = None
    distance = 0
    for i in range(len(nodelist)):
        distance = node_distance(node1 = node, node2 = nodelist[i])
        if nodelist[i] == node: pass
        else:
            if distance < minDistance:
                minDistance = distance
                nearestNode = nodelist[i]
    return nearestNode

def check_obstacle(safesize, node, obstaclelist):
    for i in range(len(obstaclelist)):
        dist = node_distance(node1 = node, node2 = obstaclelist[i][0])
        if node_distance(node1 = node, node2 = obstaclelist[i][0]) <= safesize + obstaclelist[i][1]:
            return True
        else : continue
    return False


def generate_final_course(gnode, nodelist):

    path = [[gnode.x, gnode.y]]
    node = nodelist[len(nodelist) - 2]
    while node.parent is not None:
        path.append([node.x, node.y])
        node = node.parent
    path.append([node.x, node.y])

    return path

def check_drones(drone, drones, node):
    for i in range(len(drones)):
        if drone == drones[i]: pass
        else :

            if node_distance(node1 = drones[i].position, node2 = node) <= drones[i].safesize + drone.safesize :
                return True
            else : continue
    return False

#--------------------PRM-----------------------#



def random_node_list_generation(numberOfVertices, minRand, maxRand, obstaclelist, safesize):
    list = []
    for i in range(numberOfVertices ) :
        nodel = node(random.randint(minRand, maxRand), random.randint(minRand, maxRand))
        while check_obstacle(node = nodel, obstaclelist = obstaclelist, safesize = safesize):
            nodel = node(random.randint(minRand,maxRand), random.randint(minRand,maxRand))

        list.append(nodel)

    return list

def k_nearest(nodelist,node,k,obstaclelist, safesize):
    l = 0
    nearest = []
    nodelist2 = nodelist.copy()

    while l < k:
        if len(nodelist2) < 2 : break
        nearestNode = get_nearest_node(nodelist = nodelist2, node = node)

        if possible_to_connect(node1 = node, node2 = nearestNode, obstaclelist=obstaclelist, safesize=safesize):
            nearest.append(nearestNode)
            nodelist2.remove(nearestNode)
            l = l + 1
        else:
            nodelist2.remove(nearestNode)

    return nearest

def possible_to_connect(node1, node2,obstaclelist, safesize):
    newnode = node1

    while node_distance(newnode, node2) > safesize:
        newnode = make_step(newnode,node2, stepx = 0.1, stepy = 0.1)
        if check_obstacle(safesize = safesize, node = newnode, obstaclelist = obstaclelist):
            return False
    return True


def initialize_graph(list):
    g = Graph()
    for i in range(len(list)):
        for j in range(len(list[i].nearest)):
            dist = node_distance(list[i], list[i].nearest[j])
            g.add_edge(from_node=list[i], to_node=list[i].nearest[j], weight = dist)
    return g



def dijsktra(graph, initial, end):

    shortest_paths = {initial: (None, 0)}
    current_node = initial
    visited = set()

    while current_node != end:
        visited.add(current_node)
        destinations = graph.edges[current_node]
        weight_to_current_node = shortest_paths[current_node][1]

        for next_node in destinations:
            weight = graph.weights[(current_node, next_node)] + weight_to_current_node
            if next_node not in shortest_paths:
                shortest_paths[next_node] = (current_node, weight)
            else:
                current_shortest_weight = shortest_paths[next_node][1]
                if current_shortest_weight > weight:
                    shortest_paths[next_node] = (current_node, weight)

        next_destinations = {nodee: shortest_paths[nodee] for nodee in shortest_paths if nodee not in visited}
        if not next_destinations:
            return "Route Not Possible"
        current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

    # Work back through destinations in shortest path
    path = []
    while current_node is not None:
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    # Reverse path
    path = path[::-1]
    return path

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}



    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def remove_edge(self, from_node, to_node):
        self.edges[from_node].remove(to_node)
        self.edges[to_node].remove(from_node)




def line_intercepting(line1, line2, safesize1, safesize2, stepx, stepy):

    newnode2 = line2[0]
    while node_distance(node1 = newnode2, node2 = line2[1]) >= safesize2:
        newnode1 = line1[0]

        while node_distance(node1 = newnode1, node2 = line1[1]) > safesize1 :
            if check_obstacle(safesize = safesize1, node = newnode1, obstaclelist = [[newnode2, safesize2]]): return True
            newnode1 = make_step(nodef = newnode1, nodet = line1[1], stepx = stepx, stepy = stepy)
        newnode2 = make_step(nodef = newnode2, nodet = line2[1], stepx = stepx, stepy = stepy)
    return False

def path_intercepting(path1, path2, safesize1, safesize2, stepx, stepy):

    for i in range(len(path1)):
        if i < len(path1) - 1:
            for j in range(len(path2)):
                if j < len(path2) - 1 :
                    if line_intercepting(line1 = [path1[i],path1[i + 1]], line2 = [path2[j], path2[j+1]], safesize1 =safesize1, safesize2 = safesize2,stepx =stepx,  stepy = stepy):
                        return [path1[i],path1[i + 1]], [path2[j], path2[j+1]]

                    else: continue

        else : return True, True
    return True, True


def build_paths(drones, colors, list):
    colors = ['r', 'y', 'g']
    for i in range(len(list)):
        plt.plot(list[i].x, list[i].y, marker='x', color='g')
    x = [[] for i in range(len(drones))]
    y = [[] for i in range(len(drones))]
    distances = []
    for k in range(len(drones)):
        distance = 0
        for i in range(len(drones[k].path)):
            x[k].append(drones[k].path[i].x)
            y[k].append(drones[k].path[i].y)
            if i < len(drones[k].path) - 1:
                distance = distance + node_distance(node1=drones[k].path[i], node2=drones[k].path[i + 1])
        distances.append(distance)
    for i in range(len(drones)):
        plt.plot(x[i], y[i], color=colors[i])
        plt.plot(x[i], y[i], color=colors[i])