#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 18:14:02 2022

@author: larsnolden
"""
import pandas as pd

from constants import train_height

def build_train_coordinates(number_of_seats):
    # plot the train interior walls
    x = [0]
    y = [0]
    for i in range(number_of_seats):
        seat_n = i+1
        shift_x = (seat_n*1.1)
        x.extend([0+shift_x, 0.5+shift_x, 0.5+shift_x, 1+shift_x, 1+shift_x, 1.1+shift_x, 1.1+shift_x])
        y.extend([0, 0, 0.5, 0.5, 1, 1, 0])
    return [x, y, ]

def collision_detection(train, pos):
    y = train.iloc[(train['x_train']-12).abs().argsort()[:1]]['y_train'].values[0]
    if(y >= pos[1]):
        return True
    elif(pos[1] >= train_height or pos[1] <= 0):
        # train ceilling/floor
        return True
    elif(pos[0] <= 0 or pos[0] >= max(train['x_train'])):
        #train left/right wall
        return True
    return False

def collision_detection_init(x_train, y_train):
    train = pd.DataFrame({'x_train': x_train, 'y_train': y_train})
    return lambda pos: collision_detection(train, pos)