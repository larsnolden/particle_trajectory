#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:15:40 2022

@author: larsnolden
"""

import math
from math import log
from scipy import constants
from constants import *

reynolds_max = None
reynolds_min = None

Re = lambda v, particle_diameter: fluid_density*v*particle_diameter/dynamic_viscosity_air_25C  #not entirely accurate

# Slip correction factor
C_c = lambda particle_diameter: 1 + 2*mean_free_path_air_25C/particle_diameter*(1.257+0.4*math.e**(-1.1*particle_diameter/(2*mean_free_path_air_25C)))

def C_d(Re):
    global reynolds_max 
    global reynolds_min
    #if reynolds_max is None or Re > reynolds_max:
     #   reynolds_max = Re
    #if reynolds_min is None or Re < reynolds_min:
     #   reynolds_min = Re
    if Re < 0.1:
        return 24/Re
    elif Re > 0.1 and Re < 0.2:
        return 24/Re*(1+3/16*Re+9/160*Re**2*log(2*Re))
    elif Re > 0.2 and Re < 500:
        return 24/Re*(1+0.15*Re**0.686)
    elif Re > 500 and Re < 2e5:
        return 0.44
    elif Re > 2e5:
        raise Exception('Reynolds number to large')
    
def F_drag(v, particle_diameter):
    #print('v', v, 'F_drag particle_diameter', particle_diameter)
    # also add drag force = 0 if velocity is 0
    if particle_diameter <= 10e-6:
        return (3*math.pi*dynamic_viscosity_air_25C*v*particle_diameter)/(C_c(particle_diameter)*(2/particle_diameter))
    elif particle_diameter <= 10000e-6:
        return math.pi/8*C_d(Re(v, particle_diameter))*fluid_density*particle_diameter**2*v**2
    else:
        print('large droplet')
        return 2*0.47/(fluid_density*v**2*4*math.pi*(particle_diameter/2)**2)

F_g = lambda particle_mass: particle_mass*constants.g
F_b = lambda particle_volume: fluid_density*particle_volume*constants.g

def acceleration(v, speed, particle_diameter):
    particle_volume = 4/3*math.pi*(particle_diameter/2)**3
    particle_mass = particle_volume*particle_density
    #print('v', v, 'speed', speed, 'particle_diameter', particle_diameter, 'particle_volume', particle_volume, 'particle_mass', particle_mass)
    
    velocity_unitvector_x = v[0]/speed
    velocity_unitvector_y = v[1]/speed
    drag_force = F_drag(speed, particle_diameter)
    drag_force_x = -1*velocity_unitvector_x*drag_force
    drag_force_y = -1*velocity_unitvector_y*drag_force

    a_x = drag_force_x/particle_mass
    a_y = (-F_g(particle_mass) + drag_force_y + F_b(particle_volume))/particle_mass
    #print(f'{v = }\n', f'{speed = }\n', f'{velocity_unitvector_x = }\n', f'{velocity_unitvector_y = }\n', f'{drag_force = }\n', f'{drag_force_x = }\n', f'{drag_force_y = }\n', f'{a_x = }\n',f'{a_y = }\n\n')
    return [a_x, a_y]