# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 20:48:07 2025

@author: Xfact
"""

import dearpygui.dearpygui as dpg

islandPositions = [(0,0), (-2,1), (2,1), (-3,2), (-1,2), (1,2), (3,2)]
islandPlotPadding = 0
islandLayers = 3

arrowThickness = 0.05
arrowSize = 0.1

def initIslandSystem(pos, width, height):
    with dpg.window(tag = "islandWindow", no_scrollbar = True, pos = pos, width = width, height = height, no_move = True, no_resize = True, no_collapse = True, no_title_bar = True, no_close = True):
        with dpg.plot(tag = "islandPlot", pos = (0,0), width = width, height = height, no_mouse_pos = True, no_box_select = True, no_menus = True, equal_aspects = True):
            xAxis = dpg.add_plot_axis(dpg.mvXAxis, no_tick_marks = True, no_tick_labels = True, no_gridlines = True)
            dpg.set_axis_limits_constraints(xAxis, min(islandPositions, key = lambda x: x[0])[0] + islandPlotPadding, max(islandPositions, key = lambda x: x[0])[0] + islandPlotPadding) 
            yAxis = dpg.add_plot_axis(dpg.mvYAxis, no_tick_marks = True, no_tick_labels = True, no_gridlines = True)
            dpg.set_axis_limits_constraints(yAxis, min(islandPositions, key = lambda x: x[1])[1] + islandPlotPadding, max(islandPositions, key = lambda x: x[1])[1] + islandPlotPadding)
            
            prevLayerNode = 0
            nextLayerNode = 1
            for layer in range(1, islandLayers):
                layerSize = 2**layer
                for node in range(layerSize):
                    p1 = islandPositions[node + nextLayerNode]
                    p3 = islandPositions[node // 2 + prevLayerNode]
                    p2 = (p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2
                    pLeft = (p3[0] - p1[0] - p3[1] + p1[1]) * arrowSize + p2[0], (p3[0] - p1[0] + p3[1] - p1[1]) * arrowSize + p2[1]
                    pRight = (p3[0] - p1[0] + p3[1] - p1[1]) * arrowSize + p2[0], (p3[1] - p1[1] - p3[0] + p1[0]) * arrowSize + p2[1]
                    
                    dpg.draw_circle(p1, arrowThickness / 2, fill = (255,255,255))
                    dpg.draw_circle(p2, arrowThickness / 2, fill = (255,255,255))
                    dpg.draw_circle(p3, arrowThickness / 2, fill = (255,255,255))
                    dpg.draw_circle(pRight, arrowThickness, fill = (255,255,255))
                    dpg.draw_circle(pLeft, arrowThickness, fill = (255,255,255))
                    
                    dpg.draw_line(p2, pRight, thickness = arrowThickness)  
                    dpg.draw_line(p2, pLeft, thickness = arrowThickness)
                    dpg.draw_line(islandPositions[node // 2 + prevLayerNode], islandPositions[node + nextLayerNode], thickness = arrowThickness)
                
                prevLayerNode = nextLayerNode
                nextLayerNode += layerSize
    
