# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 19:22:11 2025

@author: Xfact
"""

import taskSystem as tsk
import islandPathway as island
import greenPointsSystem as gps

import json
import os

#File for save stuff
FILEPATH = 'EcoQuestSave.txt'

#Basically just chec for save, and load if there is
def initProgress():
    if os.path.exists(FILEPATH):
        #Read file and get dictionary
        with open(FILEPATH, 'r') as file:
            value = json.load(file)
        
        #Add all stats
        gps.greenPointsCount = value['greenPointsCount']
        gps.lifetimeGreenPointsCount = value['lifeTimeGreenPointsCount']
        
        gps.updateGreenPointsText()
        #Add taskMessages and porgress
        for i in range(len(value['taskMessage'])):
            tsk.addTask(tsk.Task(value['taskAmount'][i],
                                 value['taskCurrentValue'][i],
                                 value['taskMessage'][i],
                                 value['taskWorth'][i]))
        
        #Add all the islands
        for i, unlock in enumerate(value['islandUnlocks']):
            if unlock:
                island.attemptIslandUnlock(i, True)

#Save progress
def saveProgress():
    #Put all data in dictionary
    data = {'greenPointsCount':gps.greenPointsCount,
            'lifeTimeGreenPointsCount':gps.lifetimeGreenPointsCount,
            'taskMessage':[],
            'taskWorth':[],
            'taskAmount':[],
            'taskCurrentValue':[],
            'islandUnlocks':island.activatedIslands}
    
    #Class cant be dumped directly, so add it as individual values
    for i in tsk.taskList:
        data['taskAmount'].append(i.maxValue)
        data['taskCurrentValue'].append(i.currentValue)
        data['taskMessage'].append(i.taskMessage)
        data['taskWorth'].append(i.taskWorth)
    
    #Write to file
    with open(FILEPATH, 'w') as file:
        json.dump(data, file)
            
        