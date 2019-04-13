"""
Assignment 7 to animate planetary motion
Michael Dansie
"""
from vpython import *
from math import cos, sin, radians, sqrt, e
import argparse
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

# Constants
G = 1.36*10**-34         # Newton's Gravitational Contant 
M = 1.9891e30           # Mass of the Sun (kg)

def set_scene():
    """
    Set Vpython Scene
    """
    scene.title = "Assignment 7: Planetary motion"
    scene.width = 800
    scene.heigth = 600
    scene.caption = """Right button drag or Ctrl-drag to rotate "camera" to view scene.
    To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
    On a two-button mouse, middle is left + right.
    Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""
    scene.forward = vector(0, -.3, -1)
    scene.x = -1

def system_motion(planet_data):
    """"
    This plots the motion of the solar system
    :param:planet data dictionary
    """
    #Set up the planets
    mercury = sphere(pos=vector(planet_data['Mercury'][0], planet_data['Mercury'][1], 0), 
              velocity = vector(planet_data['Mercury'][2], planet_data['Mercury'][3], 0),acceleration = vector(0,0,0),
              radius = .1, color=color.white, mass = planet_data['Mercury'][4])
    venus = sphere(pos=vector(planet_data['Venus'][0], planet_data['Venus'][1], 0), 
              velocity = vector(planet_data['Venus'][2], planet_data['Venus'][3], 0),acceleration = vector(0,0,0),
              radius = .15, color=color.yellow, mass = planet_data['Venus'][4])
    earth = sphere(pos=vector(planet_data['Earth'][0], planet_data['Earth'][1], 0), 
              velocity=vector(planet_data['Earth'][2], planet_data['Earth'][3], 0),acceleration = vector(0,0,0),
              radius = .15, color=color.blue, mass = planet_data['Earth'][4])
    mars = sphere(pos=vector(planet_data['Mars'][0], planet_data['Mars'][1], 0), 
              velocity=vector(planet_data['Mars'][2], planet_data['Mars'][3], 0), acceleration = vector(0,0,0),
              radius = .1, color=color.red, mass = planet_data['Mars'][4])
    saturn = sphere(pos=vector(planet_data['Saturn'][0], planet_data['Saturn'][1], 0), 
              velocity=vector(planet_data['Saturn'][2], planet_data['Saturn'][3], 0), acceleration = vector(0,0,0),
              radius = .5, color=color.yellow, mass = planet_data['Saturn'][4])
    jupiter = sphere(pos=vector(planet_data['Jupiter'][0], planet_data['Jupiter'][1], 0), 
              velocity=vector(planet_data['Jupiter'][2], planet_data['Jupiter'][3], 0),acceleration = vector(0,0,0), 
              radius = .6, color=color.orange, mass = planet_data['Jupiter'][4])
    uranus = sphere(pos=vector(planet_data['Uranus'][0], planet_data['Uranus'][1], 0), 
              velocity=vector(planet_data['Uranus'][2], planet_data['Uranus'][3], 0), acceleration = vector(0,0,0),
              radius = .5, color=color.cyan, mass = planet_data['Uranus'][4])
    neptune = sphere(pos=vector(planet_data['Neptune'][0], planet_data['Neptune'][1], 0), 
              velocity=vector(planet_data['Neptune'][2], planet_data['Neptune'][3], 0), acceleration = vector(0,0,0), 
              radius = .3, color=color.cyan, mass = planet_data['Neptune'][4])
    pluto = sphere(pos=vector(planet_data['Pluto'][0], planet_data['Pluto'][1], 0), 
              velocity=vector(planet_data['Pluto'][2], planet_data['Pluto'][3], 0), acceleration = vector(0,0,0), 
              radius = .1, color=color.white, mass = planet_data['Pluto'][4])
    sun = sphere(pos=vector(0,0,0), velocity = vector(0,0,0), acceleration = vector(0,0,0), radius=.1, color=color.yellow, mass = M)
    #Store them in a list
    planets = [mercury, venus, earth, mars, saturn, jupiter, uranus, neptune, pluto, sun]
    
    #calculate the motion and animate it
    if planet_data['method'] == "euler-cromer":
      euler_cromer(planets)
    elif planet_data['method'] == "leap-frog":
      leap_frog(planets)
    
def leap_frog(planets):
  """
  Calculates the euler cromer motion of a list of planets
  :param:planets-list of vypython sphere objects
  """
  #time variables
  t = 0
  dt = 1
  first_step = 0

  while(t < 3000):
    rate(60)
    for i in planets:
      i.acceleration = vector(0,0,0)
      for j in planets:
        if i != j:
          dist = j.pos - i.pos
          i.acceleration = i.acceleration + G * j.mass * dist / mag(dist)**3 #calculate the acceleration
    if first_step == 0:
      for i in planets:
          if i != planets[9]:
            i.velocity = i.velocity + i.acceleration*dt/2.0 #calculate velocity
            i.pos = i.pos + i.velocity * dt #calculate position
      first_step =1
    else:
      for i in planets:
          if i != planets[9]:
            i.velocity = i.velocity + i.acceleration*dt #calculate velocity
            i.pos = i.pos + i.velocity * dt #calculate position
    t = t + dt #update time

def euler_cromer(planets):
  """
  Calculates the euler cromer motion of a list of planets
  :param:planets-list of vypython sphere objects
  """
  #time variables
  t = 0
  dt = 1

  while(t < 3000):
    rate(60)
    for i in planets:
      i.acceleration = vector(0,0,0)
      for j in planets:
        if i != j:
          dist = j.pos - i.pos
          i.acceleration = i.acceleration + G * j.mass * dist / mag(dist)**3 #calculate the acceleration
    for i in planets:
        if i != planets[9]:
          i.velocity = i.velocity + i.acceleration*dt #calculate velocity
          i.pos = i.pos + i.velocity * dt #calculate position
    t = t + dt #update time

def read_planet_data(planet_file, planet_data):
    """
    Read the planet data from the file and put it into the dictionary
    :param planet_file: File string with planet data
    :param planet_data: A dictionary to collect data.
    :return: data frame
    """
    #store the planet data
    data = pd.read_csv(planet_file, delimiter = ",",  names = ['planet', 'pos_x', 'pos_y', 'vel_x', 'vel_y', 'mass'], 
            usecols = [0,1,2,4,5,7] , skiprows=2)#read planets, positions, velocities, and masses

    #add an np array for each planet to the dictionary
    for index, row in data.iterrows():
        i = index
        if data['planet'].iloc[i] == "Earth+Moon barycenter":
            planet_data['Earth'] = np.array([data['pos_x'].iloc[i],data['pos_y'].iloc[i],
                    data['vel_x'].iloc[i],data['vel_y'].iloc[i],data['mass'].iloc[i]], float)
        else:
            planet_data[data['planet'].iloc[i]] = np.array([data['pos_x'].iloc[i],data['pos_y'].iloc[i],
                    data['vel_x'].iloc[i],data['vel_y'].iloc[i],data['mass'].iloc[i]], float)
    
def main():
    """
    Parse the argument, read the file, plot the motion
    """
    #dictionary for data
    planet_data = {}
    # 1) Parse the arguments
    parser = argparse.ArgumentParser(description="Solar System Demo")
    parser.add_argument("--file", action = "store",
                        dest = "file", type = str,
                        required=True, help = "--file solar_system_points.csv")
    parser.add_argument("--method", action = "store",
                        dest = "method", type = str,
                        required=True, help = "--method euler-cromer OR leap-frog")
    
    args = parser.parse_args()
    file = args.file
    planet_data['method'] = args.method
    #read in the data from the file
    read_planet_data(file, planet_data)
    #set scene
    set_scene()
    #animate the motion
    system_motion(planet_data)

if __name__ == "__main__":
    main()
    exit(0)