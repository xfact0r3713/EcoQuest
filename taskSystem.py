# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:57:52 2025

@author: Xfact
"""

import math
import dearpygui.dearpygui as dpg
import themes
import greenPointsSystem as gps

taskHeight = 100
taskSpacing = 5
taskWidth = 400

taskList = list()

def dropCallback(sender, app_data, user_data):
    userData = dpg.get_item_user_data(sender)
    
    dpg.configure_item(taskList[userData].childWindow, pos = (0, app_data * (taskHeight + taskSpacing)))
    dpg.configure_item(taskList[app_data].childWindow, pos = (0, userData * (taskHeight + taskSpacing)))
    
    dpg.configure_item(taskList[userData].dragPayload, drag_data = app_data)
    dpg.configure_item(sender, user_data = app_data)
    dpg.configure_item(taskList[app_data].dragPayload, drag_data = userData)
    dpg.configure_item(taskList[app_data].progressBar, user_data = userData)
    
    taskList[app_data], taskList[userData] = taskList[userData], taskList[app_data]

def incrementTask(sender, app_data, user_data):
    if user_data.maxValue <= user_data.currentValue:
        return
    
    user_data.currentValue += 1
    user_data.updateTask(user_data)

def decrementTask(sender, app_data, user_data):
    if user_data.currentValue <= 0:
        return
    
    user_data.currentValue -= 1
    user_data.updateTask(user_data)
    
def claimTask(sender, app_data, user_data):
    return

class Task:
    def __init__(self, maxValue = math.inf, currentValue = 0, taskMessage = "", taskWorth = 0):
        self.maxValue = maxValue
        self.currentValue = currentValue
        
        self.taskMessage = taskMessage + ' Reward: ' + str(taskWorth) + ' green points'
        self.taskWorth = taskWorth
        
        self.progressBar = 0
        self.claimReward = 0
        self.messageText = 0
        self.childWindow = 0
        
        self.dragPayload = 0
        
    def createTask(self, index):
        with dpg.child_window(parent = 'taskWindow', border = False, pos = (0, index * (taskHeight + taskSpacing)), no_scrollbar = True, height = taskHeight, width = taskWidth) as self.childWindow:
            self.progressBar = dpg.add_progress_bar(default_value = self.currentValue / self.maxValue, width = taskWidth - taskWidth / 10, height = taskHeight, pos = (0, 0), drop_callback = dropCallback, user_data = index)
            dpg.bind_item_theme(self.progressBar, themes.roundCornersTheme)
            
            self.messageText = dpg.add_text(self.taskMessage + ' - ' + str(self.currentValue) + '/' + str(self.maxValue), wrap = taskWidth, pos = (15,taskHeight / 2 - 30)) 
            
            with dpg.drag_payload(parent = self.progressBar, drag_data = index, show = True) as self.dragPayload:
                dpg.add_text(self.taskMessage)
                
            dpg.add_button(label = '+', pos = (taskWidth - taskWidth / 10, 0), width = taskWidth / 10, height = taskHeight / 3, callback = incrementTask, user_data = self)
            dpg.add_button(label = '-', pos = (taskWidth - taskWidth / 10, taskHeight / 3), width = taskWidth / 10, height = taskHeight / 3, callback = decrementTask, user_data = self)
            dpg.add_button(label = 'Claim', pos = (taskWidth - taskWidth / 10, taskHeight - taskHeight / 3), width = taskWidth / 10, height = taskHeight / 3, show = False, callback = claimTask, user_data = self)
            
    def updateTask(self, task):
        dpg.set_value(self.messageText, self.taskMessage + ' - ' + str(self.currentValue) + '/' + str(self.maxValue))
        dpg.set_value(self.progressBar, self.currentValue / self.maxValue)
        
        if self.maxValue <= self.currentValue:
            dpg.show_item(self.claimReward)
        if self.maxValue > self.currentValue:
            dpg.hide_item(self.claimReward)

def addTask(task):
    taskList.append(task)
    task.createTask(len(taskList) - 1)
    
def initTaskSystem(pos, width, height):
    global taskWidth, taskHeight
    
    dpg.add_window(tag = "taskWindow", no_scrollbar = False, pos = pos, width = width, height = height, no_move = True, no_resize = True, no_collapse = True, no_title_bar = True, no_close = True)
    taskWidth = width - 18
    taskHeight = height / 8
    

