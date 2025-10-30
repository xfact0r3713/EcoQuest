# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg

mainTheme = 0

#initiate all themes
def initThemes():
    global mainTheme
    
    with dpg.theme() as mainTheme:
        #make theme for progress bars for tasks
        with dpg.theme_component(dpg.mvProgressBar):
            dpg.add_theme_color(dpg.mvThemeCol_PlotHistogram, (0, 130, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category = dpg.mvThemeCat_Core)
        #make themes for button for tasks
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 130, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 150, 0))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category = dpg.mvThemeCat_Core)