# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:16:36 2025

@author: Xfact
"""
import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=800)
dpg.setup_dearpygui()
dpg.maximize_viewport()

import taskSystem as task
task.makeTaskWindow((0,0), dpg.get_viewport_client_width() / 2, dpg.get_viewport_client_height())

for i in range(2):
    task.addTask(task.Task(10, i, str(i)))

dpg.show_viewport()

while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()

dpg.destroy_context()