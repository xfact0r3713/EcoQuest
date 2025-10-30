# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 17:14:21 2025

@author: Xfact
"""

import dearpygui.dearpygui as dpg

mainTheme = 0

def initThemes():
    global mainTheme
    
    with dpg.theme() as mainTheme:
        with dpg.theme_component(dpg.mvProgressBar):
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (0, 130, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category = dpg.mvThemeCat_Core)
            
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 130, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 150, 0))