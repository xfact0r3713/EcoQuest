# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:16:36 2025

@author: Xfact
"""
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=100, height=100)
dpg.setup_dearpygui()
dpg.maximize_viewport()
dpg.show_viewport()
dpg.render_dearpygui_frame()

maxWidth = dpg.get_viewport_client_width()
maxHeight = dpg.get_viewport_client_height()

import taskSystem as task
task.initTaskSystem((0,0), maxWidth / 2, maxHeight)

import islandPathway as island
island.initIslandSystem((maxWidth / 2, 0), maxWidth / 2,  maxHeight)

for i in range(10):
    task.addTask(task.Task(10, i, str(i)))

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()