# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 18:43:28 2025

@author: Xfact
"""

import random as rand

easyTasks = ['Walk or bike instead of driving',
             'Use public transport',
             'Mantain Tire pressure to save fuel',
             'Turn off lights when leaving room',
             'Unplug unused devices',
             'Replace lightbulb with LED',
             'Wash clothes in cold water',
             'Turn off computer overnight',
             'Use natural light instead of lamps',
             'Take 5 minute or less shower',
             'Turn off tap while brushing teeth',
             'Bring reusable bottle or cup',
             'Reuse leftovers',
             'Bring your own shopping bag',
             'Pick up litter at neighborhood etc.']

mediumTasks = ['Carpool with friend or coworker',
              'Hang clothes to dry instead of user dryer',
              'Do not use heater or airconditioner',
              'Collect rainwater to water plants',
              'Use leftover cooking water for plants',
              'Avoid using single use plastics for a day', 
              'Grow a small plant',
              'Reuese old item', 
              'Repair something instead of buying something new',
              'Donate clothes you do not wear']

hardTasks = ['No Car day',
             'Replace car trip with walk or bike',
             'Fix item leaking water',
             'Start a compost bin',
             'Recycle batteries/electric waste properly',
             'Volunteer for local cleanup',
             'Create a small garden']

def generateTask():
    randNumber = rand.randint(1,10)
    taskAmount = 1
    taskMessage = ''
    taskReward = 1
    
    if randNumber < 2:
        taskMessage = rand.choice(hardTasks)
        taskReward = 3
        taskAmount = rand.randint(1,3)
    elif randNumber < 6:
        taskMessage = rand.choice(mediumTasks)
        taskReward = 2
        taskAmount = rand.randint(1,5)
    else:
        taskMessage = rand.choice(hardTasks)
        taskAmount = rand.randint(1,7)
        
    return taskMessage, taskAmount, taskReward * taskAmount
        
        