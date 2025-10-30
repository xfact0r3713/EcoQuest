# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg

greenPointsCount = 0
greenPointsMultiplier = 1
lifetimeGreenPointsCount = 0

spacing = 5

#Create the green point notifications
def initGreenPoints(pos, width, height, notificationPos, notificationWidth, notificationHeight):
    #notifications for buying
    with dpg.window(label = 'Confirm Green Points Spending', tag = 'confirmGreenPointsSpending', no_scrollbar = True, pos = notificationPos, width = notificationWidth, height = notificationHeight, no_move = True, no_resize = True, no_collapse = True, no_close = True, show = False, modal = True):
        dpg.add_text(tag = 'greenPointsConfirmText', pos = (spacing, spacing * 3), wrap = notificationWidth - spacing)
        dpg.add_button(tag = 'succecfulGreenPointDecrement', label = 'Yes', pos = (spacing, notificationHeight - notificationHeight / 5 - spacing), width = notificationWidth / 10, height = notificationHeight / 5)
        dpg.add_button(label = 'No', pos = (notificationWidth - notificationWidth / 10 - spacing, notificationHeight - notificationHeight / 5 - spacing), width = notificationWidth /10, height = notificationHeight / 5, callback = lambda: dpg.hide_item("confirmGreenPointsSpending"))
    
    notificationWidth *= 2/3
    notificationHeight /= 2
    #notifcation for not enough things
    with dpg.window(label = 'Not Enough Green Points', tag = 'failedGreenPointsSpending', pos = notificationPos, width = notificationWidth, height = notificationHeight, no_move = True, no_resize = True, no_collapse = True, no_close = True, show = False, modal = True):
        dpg.add_button(label = 'Close', pos = (notificationWidth / 2 - notificationWidth / 10, notificationHeight / 2 - notificationHeight / 10), width = notificationWidth / 5, height = notificationHeight / 5, callback = lambda: dpg.hide_item('failedGreenPointsSpending'))
    #Green points stats
    with dpg.window(tag = 'greenPointsWindow', pos = pos, width = width, height = height, no_scrollbar = True, no_move = True, no_resize = True, no_collapse = True, no_title_bar = True, no_close = True):
        dpg.add_text(pos = (spacing, spacing), tag = 'greenPointsText', default_value = "Green Points: " + str(greenPointsCount))
        dpg.add_text(pos = (spacing, spacing * 4), tag = 'greenPointsMultiplierText', default_value = "Green Points Multiplier: " + str(greenPointsMultiplier))
        dpg.add_text(pos = (spacing, spacing * 7), tag = 'lifetimeGreenPointsText', default_value = "Lifetime Green Points: " + str(lifetimeGreenPointsCount))

#update stats
def updateGreenPointsText():
    dpg.set_value('greenPointsText', "Green Points: " + str(greenPointsCount))
    dpg.set_value('lifetimeGreenPointsText', "Lifetime Green Points: " + str(lifetimeGreenPointsCount))
    dpg.set_value('greenPointsMultiplierText', "Green Points Multiplier: " + str(greenPointsMultiplier))

#Increase the amount of green points and update
def incrementGreenPoints(amount):
    global greenPointsCount, lifetimeGreenPointsCount
    
    greenPointsCount += amount * greenPointsMultiplier
    lifetimeGreenPointsCount += amount * greenPointsMultiplier
    
    updateGreenPointsText()

#Try to decrement and buy and update stats
def decrementGreenPoints(amount, successCallback):
    if amount > greenPointsCount:
        dpg.show_item('failedGreenPointsSpending')
        return
    
    def successfulTransaction(sender, app_data, user_data):
        global greenPointsCount
        
        greenPointsCount -= amount
        updateGreenPointsText()
        
        successCallback()
        dpg.hide_item('confirmGreenPointsSpending')
        
    dpg.set_value('greenPointsConfirmText', "Do you want to spend " + str(amount) + " Green Points?")
    dpg.configure_item('succecfulGreenPointDecrement', callback = successfulTransaction)
    dpg.show_item("confirmGreenPointsSpending")

#Add multiplier and update stats
def addGreenPointsMultiplier(multiplier):
    global greenPointsMultiplier
    greenPointsMultiplier *= multiplier
    
    updateGreenPointsText()
    
