#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:12:24 2022

@author: larsnolden
"""

# train
exhalation_height = 1
train_height = 2

# general
particle_density = 997 # kg/m^3
fluid_density = 1.255 # kg/m^3
dynamic_viscosity_air_25C = 1.849e-5
mean_free_path_air_25C = 6.826e-8
p_train = 101325 #Pa

# evaporation
diffusion_coefficient_water_in_air = 0.260*1e-4
saturation_pressure_water_1atm_25C = 3171 #Pa
temp = 273+25 #K
M_v = 18.05*1e-3 #g/mol molar mass water vapor
M_g = 28.96*1e-3 #g/mol molar mass air

surf_tension_water = 73e-3 #N/m
R_v = 461.9 #specific gas constant J/(kg*K)
vapor_mass_frac_inf = 0.01191 #Elena link
minimum_virus_particle_size = 0.09e-6