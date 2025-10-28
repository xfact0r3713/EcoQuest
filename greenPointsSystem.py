# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 18:53:49 2025

@author: Xfact
"""

import dearpygui.dearpygui as dpg

greenPointsCount = 0
lifetimeGreenPointsCount = 0

spacing = 5

def initGreenPoints(pos, width, height):
    with dpg.window(label = 'Confirm Green Points Spending', tag = 'confirmGreenPointsSpending', no_scrollbar = True, pos = pos, width = width, height = height, no_move = True, no_resize = True, no_collapse = True, no_close = True, show = False):
        dpg.add_text(tag = 'greenPointsText', pos = (spacing, spacing * 3), wrap = width - spacing)
        dpg.add_button(tag = 'succecfulGreenPointDecrement', label = 'Yes', pos = (spacing, height - height / 5 - spacing), width = width / 10, height = height / 5)
        dpg.add_button(label = 'No', pos = (width - width / 10 - spacing, height - height / 5 - spacing), width = width /10, height = height / 5, callback = lambda: dpg.hide_item("confirmGreenPointsSpending"))
    
    width *= 2/3
    height /= 2
    
    with dpg.window(label = 'Not Enough Green Points', tag = 'failedGreenPointsSpending', pos = pos, width = width, height = height, no_move = True, no_resize = True, no_collapse = True, no_close = True, show = False):
        dpg.add_button(label = 'Close', pos = (width / 2 - width / 10, height / 2 - height / 10), width = width / 5, height = height / 5, callback = lambda: dpg.hide_item('failedGreenPointsSpending'))

def incrementGreenPoints(amount):
    global greenPointsCount, lifetimeGreenPointsCount
    
    greenPointsCount += amount
    lifetimeGreenPointsCount += amount

def decrementGreenPoints(amount, successCallback):
    if amount > greenPointsCount:
        dpg.show_item('failedGreenPointsSpending')
        return
    
    def successfulTransaction(sender, app_data, user_data):
        global greenPointsCount
        
        greenPointsCount -= amount
        successCallback()
        dpg.hide_item('confirmGreenPointsSpending')
        
    dpg.set_value('greenPointsText', "Do you want to spend " + str(amount) + " Green Points?")
    dpg.configure_item('succecfulGreenPointDecrement', callback = successfulTransaction)
    dpg.show_item("confirmGreenPointsSpending")
    
