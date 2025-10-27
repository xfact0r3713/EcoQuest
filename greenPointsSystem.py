# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 18:53:49 2025

@author: Xfact
"""

import dearpygui.dearpygui as dpg

greenPointsCount = 0
lifetimeGreenPointsCount = 0

greenPointsConfirm = 0
spacing = 5

def initGreenPoints(pos, width, height):
    global greenPointsConfirm
    with dpg.window(pos = pos, width = width, height = height) as greenPointsConfirm:
        dpg.add_text(tag = 'greenPointsText', pos = (spacing, spacing))
        dpg.add_button(label = 'Yes', pos = (spacing, height - height / 5 - spacing), width = width / 10, height = height / 5)
        dpg.add_button(label = 'No', pos = (width - width / 10 - spacing, height - height / 5 + spacing), width = width /10, height = height / 5)

def incrementGreenPoints(amount):
    global greenPointsCount, lifetimeGreenPointsCount
    
    greenPointsCount += amount
    lifetimeGreenPointsCount += amount
    
def decrementGreenPoints(amount):
    if amount > greenPointsCount:
        dpg.popup(parent = 'taskWindow', )
    
