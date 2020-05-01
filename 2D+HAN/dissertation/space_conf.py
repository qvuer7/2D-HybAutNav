import matplotlib.pyplot as plt
from dissertation.functions import *
ax = plt.gca()
ax.cla()
ax.set_xlim((-20, 120))
ax.set_ylim((-20, 120))
obstaclelist = [[node(-10,-10),5]]
circles = [plt.Circle((-10,-10),5)]
#-------------FRAME---------------#
for i in range(12):
	circles.append(plt.Circle((i*10,-10), 5))
for i in range(12):
	circles.append(plt.Circle((-10,i*10),5))

for i in range(12):
	circles.append(plt.Circle((i*10,110),5))
for i in range(12):
	circles.append(plt.Circle((110,i*10),5))

# -------------FROM LEFT AND RIGHT SIDES---------------#
"""
for i in range(5):
    obstaclelist.append([node(i * 10, 40),5])
for i in range(6,12):
    obstaclelist.append([node(i*10, 60),5])
for i in range(5):
    obstaclelist.append([node(i * 10, 80),5])
"""
# -------------FROM TOP AND BOTTOM---------------#
for i in range(5):
    obstaclelist.append([node(40, i*10),5])
for i in range(5, 12):
    obstaclelist.append([node(60, i*10),5])
for i in range(5):
    obstaclelist.append([node(80, i*10),5])
for i in range(6,12):
    obstaclelist.append([node(20, i*10),5])



for i in range(len(obstaclelist)):
    circles.append(plt.Circle((obstaclelist[i][0].x, obstaclelist[i][0].y),obstaclelist[i][1] ))
for i in range(len(circles)):
    ax.add_artist(circles[i])


#plt.show()