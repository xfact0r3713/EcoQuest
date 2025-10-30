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

FILEPATH = 'environmentalTrackerAppSave.txt'

def initProgress():
    if os.path.exists(FILEPATH):
        with open(FILEPATH, 'r') as file:
            value = json.load(file)
            
        gps.greenPointsCount = value['greenPointsCount']
        gps.lifetimeGreenPointsCount = value['lifeTimeGreenPointsCount']
        
        gps.updateGreenPointsText()
        
        for i in range(len(value['taskMessage'])):
            tsk.addTask(tsk.Task(value['taskAmount'][i],
                                 value['taskCurrentValue'][i],
                                 value['taskMessage'][i],
                                 value['taskWorth'][i]))
            
        for i, unlock in enumerate(value['islandUnlocks']):
            if unlock:
                island.attemptIslandUnlock(i, True)
            
def saveProgress():
    data = {'greenPointsCount':gps.greenPointsCount,
            'lifeTimeGreenPointsCount':gps.lifetimeGreenPointsCount,
            'taskMessage':[],
            'taskWorth':[],
            'taskAmount':[],
            'taskCurrentValue':[],
            'islandUnlocks':island.activatedIslands}
    
    for i in tsk.taskList:
        data['taskAmount'].append(i.maxValue)
        data['taskCurrentValue'].append(i.currentValue)
        data['taskMessage'].append(i.taskMessage)
        data['taskWorth'].append(i.taskWorth)
        
    with open(FILEPATH, 'w') as file:
        json.dump(data, file)
            
        