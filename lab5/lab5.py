from vpython import *
from math import sin, cos
import argparse



def set_scene(data):
    """
    Set Vpython Scene
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
    ground = box(pos=vector(0, 0, 0), size=vector(65, .05, 15), color=color.green)
    fence = box(pos=vector(0, 2.5, -7.5), size=vector(65, 5, .05), color=color.orange)
    pillar  = cylinder(pos=vector(-25,0,0), axis=vector(0, data['init_height'], 0), radius =.5)
    


def motion_no_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    velocity_x = cos(data['theta']) * data['init_velocity']
    velocity_y = sin(data['theta']) * data['init_velocity']

    ball_nd = sphere(pos=vector(-25, data['init_height'], 0),
                        radius=data['ball_radius'], color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position
    ball_nd.velocity = vector(velocity_x, velocity_y, 0)
    ball_nd.position = vector(0, data['init_height'], 0)

    # Animate
    while ball_nd.pos.y > 0:
        rate(60)
        ball_nd.pos.x = ball_nd.pos.x + velocity_x * data['deltat']
        ball_nd.pos.y = ball_nd.pos.y + velocity_y * data['deltat']
        velocity_y = velocity_y + data['gravity'] * data['deltat']




def motion_drag(data):
    """
    Create animation for projectile motion with no dragging force
    """
    velocity_x = cos(data['theta']) * data['init_velocity']
    velocity_y = sin(data['theta']) * data['init_velocity']
    

    ball_nd = sphere(pos=vector(-25, data['init_height'], 0),
                        radius=data['ball_radius'], color=color.cyan, make_trail=True)
    # Follow the movement of the ball
    scene.camera.follow(ball_nd)
    # Set initial velocity & position
    ball_nd.velocity = vector(velocity_x, velocity_y, 0)
    ball_nd.position = vector(0, data['init_height'], 0)

    # Animate
    while ball_nd.pos.y > 0:
        rate(60)
        air_res_x = -.5 * data['rho'] * velocity_x**2 * data['Cd'] * data['ball_area']
        air_res_y = -.5 * data['rho'] * velocity_y**2 * data['Cd'] * data['ball_area']

        ball_nd.pos.x = ball_nd.pos.x + velocity_x * data['deltat']
        ball_nd.pos.y = ball_nd.pos.y + velocity_y * data['deltat']

        velocity_y = velocity_y + (data['gravity'] + air_res_y * data['ball_mass']) * data['deltat']
        velocity_x = velocity_x + (air_res_x * data['ball_mass']) * data['deltat']


def main():
    """
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
    data['Cd'] = 0.5    # coefficient friction
    data['deltat'] = 0.005
    data['gravity'] = -9.8  # m/s^2

    data['ball_mass'] = 0.145  # kg
    data['ball_radius'] = 0.25  # meters
    data['ball_area'] = pi * data['ball_radius']**2
    data['alpha'] = data['rho'] * data['Cd'] * data['ball_area'] / 2.0
    data['beta'] = data['alpha'] / data['ball_mass']
    # Set Scene
    set_scene(data)
    # 2) No Drag Animation
    motion_no_drag(data)
    # 3) Drag Animation
    motion_drag(data)
    # 4) Plot Information: extra credit
#     plot_data(data)


if __name__ == "__main__":
    main()
    exit(0)
