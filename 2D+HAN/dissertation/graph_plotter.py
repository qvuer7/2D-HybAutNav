import matplotlib.pyplot as plt



x = [195,523,811, 934, 1303, 1312, 1962, 2076]
y = [0.010,0.0649,0.1562, 0.2079, 0.2439, 0.5987, 0.9541, 1.21]


plt.plot(x,y, marker = 'o', color = 'r')
plt.xlabel('Number of nodes')
plt.ylabel('Computation time, s')
plt.show()