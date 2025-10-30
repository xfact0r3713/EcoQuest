# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg

import themes
import taskSystem as task
import greenPointsSystem as gps
import islandPathway as island
import saveProgress as prog

#Basic Dearpygui startup
dpg.create_context()
dpg.create_viewport(title = 'EcoQuest', width = 100, height = 100)
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.render_dearpygui_frame()

#Get current window size to format everything based off of the windows
maxWidth = dpg.get_viewport_client_width()
maxHeight = dpg.get_viewport_client_height()

#initiaite all modules
themes.initThemes()
task.initTaskSystem((0,0), maxWidth / 2, maxHeight)
island.initIslandSystem((maxWidth / 2, 0), maxWidth / 2,  maxHeight - maxHeight / 5)
gps.initGreenPoints((maxWidth / 2, maxHeight - maxHeight / 5), maxWidth / 2, maxHeight - maxHeight / 5, (maxWidth / 2 - maxWidth / 10, maxHeight / 2 - maxHeight / 10), maxWidth / 5, maxHeight / 5)

#Check for saves and if there is, then load save
prog.initProgress()

#Update the tasks list to fufill the amount of tasks
task.updateTaskAmount()

#Dearpygui loop
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
    
#Save all progress before exiting
prog.saveProgress()
dpg.destroy_context()