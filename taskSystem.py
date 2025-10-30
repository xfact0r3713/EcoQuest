# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg
import themes
import greenPointsSystem as gps
import taskGenerater as tskGen

taskHeight = 100
taskSpacing = 5
taskWidth = 400
maxTaskAmount = 2

taskList = list()
#drop callback for the task to be shifted
def dropCallback(sender, app_data, user_data):
    userData = dpg.get_item_user_data(sender)
    #Swap positions
    dpg.configure_item(taskList[userData].childWindow, pos = (0, app_data * (taskHeight + taskSpacing)))
    dpg.configure_item(taskList[app_data].childWindow, pos = (0, userData * (taskHeight + taskSpacing)))
    #Swap the indexes
    dpg.configure_item(taskList[userData].dragPayload, drag_data = app_data)
    dpg.configure_item(sender, user_data = app_data)
    dpg.configure_item(taskList[app_data].dragPayload, drag_data = userData)
    dpg.configure_item(taskList[app_data].progressBar, user_data = userData)
    #Swap the list position
    taskList[app_data], taskList[userData] = taskList[userData], taskList[app_data]

#Increase task amount
def incrementTask(sender, app_data, user_data):
    if user_data.maxValue <= user_data.currentValue:
        return
    
    user_data.currentValue += 1
    user_data.updateTask(user_data)

#decrease task amount
def decrementTask(sender, app_data, user_data):
    if user_data.currentValue <= 0:
        return
    
    user_data.currentValue -= 1
    user_data.updateTask(user_data)

#Claim tasks and reward
def claimTask(sender, app_data, user_data):
    #Get greenPoints
    gps.incrementGreenPoints(user_data.taskWorth)
    index = dpg.get_item_user_data(user_data.progressBar)
    #Remove the task
    taskList.pop(index)
    dpg.delete_item(user_data.childWindow)
    del user_data
    #Shift all tasks back up
    for i in range(index, len(taskList)):
        dpg.configure_item(taskList[i].dragPayload, drag_data = i)
        dpg.configure_item(taskList[i].progressBar, user_data = i)
        dpg.configure_item(taskList[i].childWindow, pos = (0, i * (taskHeight + taskSpacing)))
    #update the amount of task because task was removed
    updateTaskAmount()

#Class for tasks data
class Task:
    def __init__(self, maxValue = 0, currentValue = 0, taskMessage = "", taskWorth = 0):
        #Actual values
        self.maxValue = maxValue
        self.currentValue = currentValue
        
        self.taskMessage = taskMessage
        self.taskWorth = taskWorth
        
        #Dearpygui tags
        self.progressBar = 0
        self.claimReward = 0
        self.messageText = 0
        self.childWindow = 0
        
        self.dragPayload = 0
        
    def createTask(self, index):
        with dpg.child_window(parent = 'taskWindow', border = False, pos = (0, index * (taskHeight + taskSpacing)), no_scrollbar = True, height = taskHeight, width = taskWidth) as self.childWindow:
            self.progressBar = dpg.add_progress_bar(default_value = self.currentValue / self.maxValue, width = taskWidth - taskWidth / 10, height = taskHeight, pos = (0, 0), drop_callback = dropCallback, user_data = index)
            
            self.messageText = dpg.add_text(self.taskMessage + ' Reward: ' + str(self.taskWorth) + ' green points - ' + str(self.currentValue) + '/' + str(self.maxValue), wrap = taskWidth - taskWidth / 10, pos = (15,taskHeight / 2 - 30)) 
            
            #Payload so can be dragged and index as appdata
            with dpg.drag_payload(parent = self.progressBar, drag_data = index, show = True) as self.dragPayload:
                dpg.add_text(self.taskMessage)
                
            #increment and decrement and calim tasks buttons
            dpg.add_button(label = '+', pos = (taskWidth - taskWidth / 10, 0), width = taskWidth / 10, height = taskHeight / 3, callback = incrementTask, user_data = self)
            dpg.add_button(label = '-', pos = (taskWidth - taskWidth / 10, taskHeight / 3), width = taskWidth / 10, height = taskHeight / 3, callback = decrementTask, user_data = self)
            self.claimReward = dpg.add_button(label = 'Claim', pos = (taskWidth - taskWidth / 10, taskHeight - taskHeight / 3), width = taskWidth / 10, height = taskHeight / 3, show = self.currentValue >= self.maxValue, callback = claimTask, user_data = self)
        
        #Add theme
        dpg.bind_item_theme(self.childWindow, themes.mainTheme)    
    
    #Update all tasks stats
    def updateTask(self, task):
        dpg.set_value(self.messageText, self.taskMessage + ' Reward: ' + str(self.taskWorth) + ' green points - ' + str(self.currentValue) + '/' + str(self.maxValue))
        dpg.set_value(self.progressBar, self.currentValue / self.maxValue)
        #if enoguh, then give user option to claim
        if self.maxValue <= self.currentValue:
            dpg.show_item(self.claimReward)
        if self.maxValue > self.currentValue:
            dpg.hide_item(self.claimReward)

#Add task adn task dearpygui stuff
def addTask(task):
    taskList.append(task)
    task.createTask(len(taskList) - 1)

#Initiate task system
def initTaskSystem(pos, width, height):
    global taskWidth, taskHeight
    
    dpg.add_window(tag = "taskWindow", no_scrollbar = False, pos = pos, width = width, height = height, no_move = True, no_resize = True, no_collapse = True, no_title_bar = True, no_close = True)
    taskWidth = width - 18
    taskHeight = height / 8
    
#Increase task amount if not enough
def updateTaskAmount():
    while len(taskList) < maxTaskAmount:
        tsk = tskGen.generateTask()
        addTask(Task(tsk[1], 0, tsk[0], tsk[2]))
    

