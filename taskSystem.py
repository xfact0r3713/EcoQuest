# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:57:52 2025

@author: Xfact
"""

import math
import style
import dearpygui.dearpygui as dpg

taskHeight = 100
taskSpacing = 5
taskWidth = 400
taskWindow = -1

taskList = list()
    
def dropCallback(sender, app_data, user_data):
    userData = dpg.get_item_user_data(sender)
    
    dpg.configure_item(taskList[userData].childWindow, pos = (0, app_data * (taskHeight + taskSpacing)))
    dpg.configure_item(taskList[app_data].childWindow, pos = (0, userData * (taskHeight + taskSpacing)))
    
    taskList[app_data], taskList[userData] = taskList[userData], taskList[app_data]

class Task:
    def __init__(self, maxValue = math.inf, currentValue = 0, taskMessage = ""):
        self.maxValue = maxValue
        self.currentValue = currentValue
        self.taskMessage = taskMessage
        
        self.progressBar = 0
        self.messageText = 0
        self.childWindow = 0
        
        # with dpg.child_window(parent = 'taskWindow', show = False, border = False, pos = (0,0), no_scrollbar = True, height = taskHeight, width = taskWidth) as self.childWindow:
        #     self.progressBar = dpg.add_progress_bar(default_value = currentValue / maxValue, width = taskWidth, height = taskHeight, pos = (0, 0), drop_callback = dropCallback, user_data = self.taskIndex)
            
        #     with dpg.drag_payload(parent = self.progressBar, drag_data = self.taskIndex):
        #         dpg.add_text(taskMessage)
                
        #     self.messageText = dpg.add_text(taskMessage + ' - ' + str(self.currentValue) + '/' + str(self.maxValue), wrap = taskWidth, pos = (15,taskHeight / 2 - 30)) 
        
        # dpg.bind_item_theme(self.progressBar, style.roundCornersTheme)

    # def updateProgress(self):
    #     dpg.set_value(self.progressBar, self.currentValue / self.maxValue)
    #     dpg.set_value(self.messageText, self.taskMessage + ' - ' + str(self.currentValue) + '/' + str(self.maxValue))
        
def addTask(task):
    taskList.append(task)
    index = len(taskList) - 1
    
    with dpg.child_window(parent = 'taskWindow', border = False, pos = (0, index * (taskHeight + taskSpacing)), no_scrollbar = True, height = taskHeight, width = taskWidth) as task.childWindow:
        task.progressBar = dpg.add_progress_bar(default_value = task.currentValue / task.maxValue, width = taskWidth, height = taskHeight, pos = (0, 0), drop_callback = dropCallback, user_data = index)
        
        with dpg.drag_payload(parent = task.progressBar, drag_data = index):
            dpg.add_text(task.taskMessage)
            
        task.messageText = dpg.add_text(task.taskMessage + ' - ' + str(task.currentValue) + '/' + str(task.maxValue), wrap = taskWidth, pos = (15,taskHeight / 2 - 30)) 
    
    dpg.bind_item_theme(task.progressBar, style.roundCornersTheme)

def makeTaskWindow(pos, width, height):
    taskWindow = dpg.add_window(tag = "taskWindow", no_scrollbar = False, pos = pos, width = width, height = height, no_move = True, no_resize = True, no_collapse = True, no_title_bar = True, no_close = True)
    taskWidth = width
    taskHeight = height / 8
