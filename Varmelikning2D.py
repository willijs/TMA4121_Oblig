import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#Used for plotting the graph
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
plot_args = {'rstride': 1, 'cstride': 1, 'cmap':
             cm.bwr, 'linewidth': 0.01, 'antialiased': True, 'color': 'w',
             'shade': True}


#
H = 0.05 #Constant used to aproximate derivation of x and y
K = 0.0005 #Constant used to aproximate derivation of time.
length = 1  #Total lenght of both x- and y-axis
t_time = 10 #Total time
height = 1 #Height of the starting spikes

m = n = int(length/H) #How many points to calculate the lengths for
l = int(t_time/K) #How many points to calculate the time for

u = np.zeros((n,m,l)) #Temperature at each point and time



#Initial values of the surface at t = 0
def f(x,y):
    # if (x == m//2 and y == n//2):
    #     return height
    # else:
    #     return 0
    if ((x == m//4 and y == n//4) or (x == m-m//4 and y == n-n//4)):
        return height
    else:
        return 0

#From 1 to n-1 to make the boundary 0.
for x in range(1,n-1):
    for y in range(1,m-1):
        u[x,y,0] = f(x,y)
        
        
#Using euler explicit to calculate the temperature at each point on the surface at times 0 to l.
for k in range(0,l-1):
    for j in range(1,m-1):
        for i in range(1,n-1):
            u[i,j,k+1] = u[i,j,k] + (K/H**2)*(u[i+1,j,k] + u[i-1,j,k] + u[i,j+1,k] + u[i,j-1,k] - 4*u[i,j,k])
            # print(u[i,j,k+1])






#Animation of a surface plot. Heavily inspired by the answer from this stack question: https://stackoverflow.com/questions/17299917/how-to-animate-3d-plot-surface-in-matplotlib
soln = u[:,:,0]
X = np.linspace(0, length, n)
Y = np.linspace(0, length, m)
X, Y = np.meshgrid(X, Y)
plot = ax.plot_surface(X, Y, soln, **plot_args)

#Generates a new plot every frame, and resets after 80 frames.
def data_gen(framenumber, soln, plot):
    # print(u[5,5,framenumber-negate*80])
    soln = u[:,:,framenumber % 80]
    ax.clear()
    plot = ax.plot_surface(X, Y, soln, **plot_args)
    ax.axes.set_zlim3d(bottom=0, top = height)
    return plot,

#Uses data_gen() to animate the surface plot.
pam_ani = animation.FuncAnimation(fig, data_gen, fargs=(soln, plot),
                              interval=30, blit=False)
plt.show()