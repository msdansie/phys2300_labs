"""
PHYS 2300 Assignment 6 - Michael Dansie
Animate a no-friction and friction pendulum
Graph the resutls of theta vs time
"""
from vpython import *
import numpy as np
from matplotlib import pyplot as plt

#Constants
g = 9.81    # m/s**2
l = 0.10    # meters
W = 0.002   # arm radius
R = 0.005   # ball radius
c = 1.5     # coefficient of friction
framerate = 100
steps_per_frame = 10

def f_no_drag(r):
    """
    Pendulum with no drag
    :param:r-numpy array with theta and omega
    :return: numpy array with new theta and omega
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta)
    return np.array([ftheta, fomega], float)

def f_drag(r):
    """
    Pendulum with drag
    :param:r-numpy array with theta and omega
    :return: numpy array with new theta and omega
    """
    theta = r[0]
    omega = r[1]
    ftheta = omega
    fomega = -(g/l)*np.sin(theta) - c * omega
    return np.array([ftheta, fomega], float)

def plot_data(data):
    """
    Plot theta in radians vs. time in seconds
    :param:theta-list of theta points
    :param:time-list of time points
    """
    #First plot no drag vs drag
    plt.subplot(2, 1, 1)
    plt.plot(data['times'], data['thetas'], label = "No Drag")
    plt.plot(data['times_drag'], data['thetas_drag'], label = "With Drag")
    plt.title("Theta of a Pendulum vs. Time")
    plt.legend()
    plt.ylabel("Theta in radians")

    #Second plot drag for extended period of time
    plt.subplot(2, 1, 2)
    plt.plot(data['times_drag_ext'], data['thetas_drag_ext'], label = "With Drag")
    plt.xlabel("Time in seconds")
    plt.ylabel("Theta in radians")
    plt.legend()
    plt.show()

def set_scene():
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 6: The Not So Simple Pendulum"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1

    #set the scene
    ceiling = box(pos=vector(0,0,0), length = 2*l, height = .005, width = .5*l)
    ball = sphere(pos=vector(0,0,0), radius = R)
       

def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :param:data-dictionary of collected data
    """
    #create the visual objects
    ball = sphere(pos=vector(l,0,0), radius = R, color = color.blue)
    bar =  cylinder(pos=vector(0,0,0), axis = vector(l, 0, 0), radius = W, color = color.blue)
    
    #initial x, y, and time
    x = data['x']
    y = data['y']
    t = 0

    #calculate the motion
    while t < data['total_time']:
        rate(60)
        
        #record the data
        data['thetas'].append(data['r'][0])
        data['times'].append(t)
        # Use the 4'th order Runga-Kutta approximation
        # Calculate the 4th Order Rung-Kutta
        
        k1 = data['h']*f_no_drag(data['r'])
        k2 = data['h']*f_no_drag(data['r'] + 0.5*k1)
        k3 = data['h']*f_no_drag(data['r'] + 0.5*k2)
        k4 = data['h']*f_no_drag(data['r'] + k3)
        data['r'] += (k1 + 2*k2 + 2*k3 + k4)/6

        #update time
        t += data['dt']
    
        # Update positions
        x =  l*np.sin(data['r'][0])
        y = -l*np.cos(data['r'][0])

        # Update the cylinder axis
        bar.axis.x = x
        bar.axis.y = y

        # Update the pendulum's bob
        ball.pos.x = x
        ball.pos.y = y

    #hide the completed animation    
    ball.visible = False
    bar.visible = False

def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :param:data-dictionary of collected data
    """
    #create the visual objects
    ball = sphere(pos=vector(l, 0, 0), radius = R, color = color.orange)
    bar =  cylinder(pos=vector(0,0, 0), axis = vector(l, 0, 0), radius = W, color = color.orange)
    
    #initial x, y, and time
    x = data['x']
    y = data['y']
    t = 0

    #calculate the motion
    while t < data['total_time']:
        rate(60)
        
        #record the data
        if data['total_time'] == 10:

            data['thetas_drag'].append(data['rdrag'][0])
            data['times_drag'].append(t)
        else:
            data['thetas_drag_ext'].append(data['rdrag'][0])
            data['times_drag_ext'].append(t)

        # Use the 4'th order Runga-Kutta approximation
        # Calculate the 4th Order Rung-Kutta
        k1 = data['h']*f_drag(data['rdrag'])
        k2 = data['h']*f_drag(data['rdrag'] + 0.5*k1)
        k3 = data['h']*f_drag(data['rdrag'] + 0.5*k2)
        k4 = data['h']*f_drag(data['rdrag'] + k3)
        data['rdrag'] += (k1 + 2*k2 + 2*k3 + k4)/6

        #update time
        t += data['dt']
    
        # Update positions
        x =  l*np.sin(data['rdrag'][0])
        y = -l*np.cos(data['rdrag'][0])

        # Update the cylinder axis
        bar.axis.x = x
        bar.axis.y = y

        # Update the pendulum's bob
        ball.pos.x = x
        ball.pos.y = y
    
    #hide the completed animation
    ball.visible = False
    bar.visible = False


def main():
    """
    Animate a no drag pendulum and a drag pendulum
    Animate an extended time drag pendulum
    Graph the resulting data
    """
    # Set up initial values
    data = {}
    data['h'] = 1.0/(framerate * steps_per_frame)
    data['r'] = np.array([np.pi*85/180, 0], float)
    data['rdrag'] = np.array([np.pi*85/180, 0], float)
    data['dt'] = 0.0167
    data['total_time'] = 10
    # Initial x and y
    data['x'] = l*np.sin(data['r'][0])
    data['y'] = -l*np.cos(data['r'][0])
    #Lists for recording data
    data['thetas'] = []#For no drag
    data['times'] = []
    data['thetas_drag'] = []#For drag
    data['times_drag'] = []
    data['thetas_drag_ext'] = []#For drag for extended time
    data['times_drag_ext'] = []

    #Animate the no drag and drag pendulums
    set_scene()
    motion_no_drag(data)
    motion_drag(data)

    #Extended time animation
    data['rdrag'] = np.array([np.pi*-80/180, 0], float)
    data['total_time'] = 60
    motion_drag(data)
    
    #plot the resulting data
    plot_data(data)

if __name__ == "__main__":
    main()
    exit(0)
