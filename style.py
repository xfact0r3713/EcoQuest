# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 18:58:08 2025

@author: Xfact
"""

import dearpygui.dearpygui as dpg

with dpg.theme() as roundCornersTheme:
    with dpg.theme_component(dpg.mvProgressBar):
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10, category=dpg.mvThemeCat_Core)