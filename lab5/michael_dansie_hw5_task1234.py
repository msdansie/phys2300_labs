#from vpython import *
from math import cos, sin, radians
import argparse
from matplotlib import pyplot as plt

def set_scene(data):
    """
    Set Vpython Scene
    :param:data-dictionary of collected data
    """
    scene.title = "Assignment 5: Projectile motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1

    # Set background: floor, table, etc
    ground = box(pos=vector(0, 0, 0), size=vector(data['distance'] + 15, .05, 15), color=color.green)
    fence = box(pos=vector(0, (data['max_height']+5)/2, -7.5), size=vector(data['distance'] + 15, data['max_height'] + 5, .05), color=color.white)
    pillar  = cylinder(pos=vector(-(ground.size.x/2)+3,0,0), axis=vector(0, data['init_height'], 0), radius =.5)
    
def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :param:data-dictionary of collected data
    """
    #calculate velocity components
    velocity_x = cos(radians(data['theta'])) * data['init_velocity']
    velocity_y = sin(radians(data['theta'])) * data['init_velocity']
    time = 0

    #set up the ball
    ball_nd = sphere(pos=vector((-(data['distance']+15)/2)+3, data['init_height'], 0),
                     radius=data['ball_radius'], color=color.cyan, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity
    ball_nd.velocity = vector(velocity_x, velocity_y, 0)
    
    data['posy_no_drag'] = [data['init_height']]
    data['posx_no_drag'] = [0]
    data['time_no_drag'] = [time]

    # Animate
    while ball_nd.pos.y > 0:
        rate(60)
        ball_nd.pos.x = ball_nd.pos.x + ball_nd.velocity.x * data['deltat']
        ball_nd.pos.y = ball_nd.pos.y + ball_nd.velocity.y * data['deltat']
        ball_nd.velocity.y = ball_nd.velocity.y + data['gravity'] * data['deltat']
        
        #store the data
        time = time + data['deltat']
        data['posy_no_drag'].append(ball_nd.pos.y)
        data['posx_no_drag'].append(ball_nd.pos.x + (data['distance']/2) + 5)
        data['time_no_drag'].append(time)     
    
def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    :param:data-dictionary for collected data
    """
    #calculate velocity components
    velocity_x = cos(radians(data['theta'])) * data['init_velocity']
    velocity_y = sin(radians(data['theta'])) * data['init_velocity']
    time = 0

    #set up the ball
    ball_nd = sphere(pos=vector((-(data['distance'] + 15)/2)+3, data['init_height'], 0),
                    radius=data['ball_radius'], color=color.orange, make_trail=True)

    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position
    ball_nd.velocity = vector(velocity_x, velocity_y, 0)

    data['posy_drag'] = [data['init_height']]
    data['posx_drag'] = [0]
    data['time_drag'] = [time]

    # Animate
    while ball_nd.pos.y > 0:
        rate(60)
        #calculate air resistance
        air_res_x = -.5 * data['rho'] * ball_nd.velocity.x**2 * data['Cd'] * data['ball_area']
        air_res_y = -.5 * data['rho'] * ball_nd.velocity.y**2 * data['Cd'] * data['ball_area']

        #update position and velocity
        ball_nd.pos.x = ball_nd.pos.x + ball_nd.velocity.x * data['deltat']
        ball_nd.pos.y = ball_nd.pos.y + ball_nd.velocity.y * data['deltat']

        ball_nd.velocity.y = ball_nd.velocity.y + (data['gravity'] + air_res_y / data['ball_mass']) * data['deltat']
        ball_nd.velocity.x = ball_nd.velocity.x + (air_res_x / data['ball_mass']) * data['deltat']

        #store data
        time = time + data['deltat']
        data['posy_drag'].append(ball_nd.pos.y)
        data['posx_drag'].append(ball_nd.pos.x + (data['distance']/2) + 5)
        data['time_drag'].append(time)

def plot_data(data):
    """
    Plots the collected flight data
    :param:data-dictionary of collected data
    """
    
    plt.subplot(2, 1, 1)#First Plot: Height vs. Time
    plt.plot(data['time_no_drag'], data['posy_no_drag'], label="No Air Resistance")
    plt.plot(data['time_drag'], data['posy_drag'], label="With Air Resistance")
    plt.ylabel("Height in meters")
    plt.title("Flight Position of a Projectile")
    plt.legend()

    plt.subplot(2, 1, 2)#Second Plot: Distance vs. Time
    plt.plot(data['time_no_drag'], data['posx_no_drag'], label="No Air Resistance")
    plt.plot(data['time_drag'], data['posx_drag'], label="With Air Resistance")
    plt.ylabel("Distance in meters")
    plt.xlabel("Time in seconds")
    plt.legend()
    
    plt.show()

def main():
    """
    Parses the input, plots the projectile motion, and display data
    """ 
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Projectile Motion Demo")

    parser.add_argument("--velocity", action = "store",
                        dest = "velocity", type = float,
                        required=True, help = "--velocity 20 (in m)")
    parser.add_argument("--angle", action = "store",
                        dest = "angle", type = float,
                        required=True, help = "--angle 45 (in degrees)")
    parser.add_argument("--height", action = "store",
                        dest = "height", type = float,
                        default = 1.2, help = "--height 1.2 (in m)")
    
    args = parser.parse_args()

    # Set Variables
    data = {}       # empty dictionary for all data and variables
    data['init_height'] = args.height   # y-axis
    data['init_velocity'] = args.velocity  # m/s
    data['theta'] = args.angle       # degrees

    # Constants
    data['rho'] = 1.225  # kg/m^3
    data['Cd'] = 0.5   # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.075  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']
    data['distance'] = (data['init_velocity']**2 * sin(radians(2*data['theta']))) / (-1*data['gravity'])#calculate the flight distance
    data['max_height'] = (data['init_velocity']**2 * sin(radians(data['theta'])**2))/(-2*data['gravity'])#calculate max height

    # Set Scene
    set_scene(data)

    # 2) No Drag Animation
    motion_no_drag(data)

    # 3) Drag Animation
    motion_drag(data)

    # 4) Plot Information: extra credit
    plot_data(data)

if __name__ == "__main__":
    main()
    exit(0)
