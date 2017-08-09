import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

test = 1,2
2,3
3,6
4,9
5,4
6,7
7,7
8,4
9,3
10,7

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    pullData = test #open("sampleText.txt","r").read()
    dataArray = pullData.split(';')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar,yar)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

import pdb; pdb.set_trace()  # breakpoint 7110a2d0 //

import matplotlib.pyplot as plt
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot(111)

# some X and Y data
x = np.arange(100)
y = np.random.randn(100)

li, = ax.plot(x, y)

# draw and show it
ax.relim() 
ax.autoscale_view(True,True,True)
fig.canvas.draw()
plt.show(block=False)

# loop to update the data
while True:
    try:
        y[:-10] = y[10:]
        y[-10:] = np.random.randn(10)

        # set the new data
        li.set_ydata(y)

        fig.canvas.draw()

        time.sleep(1)
    except KeyboardInterrupt:
        break