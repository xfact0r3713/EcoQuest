# -*- coding: utf-8 -*-

import dearpygui.dearpygui as dpg
import greenPointsSystem as gps
import taskSystem as task

#list of all the island prices and positions and if they have been bought or not along wiht the multipliers they add
islandPositions = [(0,0), (-2,1), (2,1), (-3,2), (-1,2), (1,2), (3,2)]
activatedIslands = [True, False, False, False, False, False, False]
islandPrice = [0, 15, 30, 90, 270, 810, 2430]
islandMultipliers = [1, 2, 2, 3, 3, 3, 3]

islandPlotPadding = 1
islandLayers = 3
islandSize = 0.4

arrowThickness = 0.02
arrowSize = 0.1

#If island has been clicked on, then attempt to buy
def islandClick(sender, app_data):
    mousePos = dpg.get_plot_mouse_pos()
    
    #checking what island is clicked on
    for i, x in enumerate(islandPositions):
        if abs(mousePos[0] - x[0]) < islandSize / 2 and abs(mousePos[1] - x[1]) < islandSize / 2:
            attemptIslandUnlock(i)
            return
            
#Creates the island map
def initIslandSystem(pos, width, height):
    #Load all images of islands
    with dpg.texture_registry():
        for i in range(1, len(islandPositions) + 1):
            imageWidth, imageHeight, imageChannels, imageData = dpg.load_image('Island Images\Island' + str(i) + '.png')
            dpg.add_static_texture(imageWidth, imageHeight, imageData, tag = 'island' + str(i - 1))
    
    #Create window for island
    with dpg.window(tag = "islandWindow", no_scrollbar = True, pos = pos, width = width, height = height, no_move = True, no_resize = True, no_collapse = True, no_title_bar = True, no_close = True):
        with dpg.plot(tag = "islandPlot", pos = (0,0), width = width, height = height, no_mouse_pos = True, no_box_select = True, no_menus = True, equal_aspects = True):
            #Constrain axis so user doesnt get lost
            xAxis = dpg.add_plot_axis(dpg.mvXAxis, no_tick_marks = True, no_tick_labels = True, no_gridlines = True)
            dpg.set_axis_limits_constraints(xAxis, min(islandPositions, key = lambda x: x[0])[0] - islandPlotPadding, max(islandPositions, key = lambda x: x[0])[0] + islandPlotPadding) 
            yAxis = dpg.add_plot_axis(dpg.mvYAxis, no_tick_marks = True, no_tick_labels = True, no_gridlines = True)
            dpg.set_axis_limits_constraints(yAxis, min(islandPositions, key = lambda x: x[1])[1] - islandPlotPadding, max(islandPositions, key = lambda x: x[1])[1] + islandPlotPadding)
            
            #This loop finds the two nodes that connect the corresponding nodes of the bsp tree like structure and connects them with a line to create a pathway
            prevLayerNode = 0
            nextLayerNode = 1
            for layer in range(1, islandLayers):
                layerSize = 2**layer
                for node in range(layerSize):
                    index  = node + nextLayerNode
                    p1 = islandPositions[index]
                    p3 = islandPositions[node // 2 + prevLayerNode]
                    #Find the arrow points
                    p2 = (p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2
                    pLeft = (p3[0] - p1[0] - p3[1] + p1[1]) * arrowSize + p2[0], (p3[0] - p1[0] + p3[1] - p1[1]) * arrowSize + p2[1]
                    pRight = (p3[0] - p1[0] + p3[1] - p1[1]) * arrowSize + p2[0], (p3[1] - p1[1] - p3[0] + p1[0]) * arrowSize + p2[1]
                    
                    #Add circles at ends of line for more smooth look
                    dpg.draw_circle(p1, arrowThickness / 2, fill = (255,255,255))
                    dpg.draw_circle(p2, arrowThickness / 2, fill = (255,255,255))
                    dpg.draw_circle(p3, arrowThickness / 2, fill = (255,255,255))
                    dpg.draw_circle(pRight, arrowThickness, fill = (255,255,255))
                    dpg.draw_circle(pLeft, arrowThickness, fill = (255,255,255))
                    
                    #Draw the arrow
                    dpg.draw_line(p2, pRight, thickness = arrowThickness)  
                    dpg.draw_line(p2, pLeft, thickness = arrowThickness)
                    dpg.draw_line(p3, p1, thickness = arrowThickness)
                    
                    #Show the pricetag of the island, and make tag so it can be delted when bought
                    dpg.draw_text((p1[0] - 0.4, p1[1]), text = 'Green Points Cost: ' + str(islandPrice[index]), tag = 'islandPriceTag' + str(index), size = 0.1, color = (255,0,0))
                    
                prevLayerNode = nextLayerNode
                nextLayerNode += layerSize
                
            #Put in images of islands
            for i in range(len(islandPositions)):
                dpg.add_image_series("island" + str(i), (islandPositions[i][0] - islandSize / 2, islandPositions[i][1] - islandSize / 2), (islandPositions[i][0] + islandSize / 2, islandPositions[i][1] + islandSize / 2), parent = yAxis)
            
        #Click Registry so then the plot can be clikced and island can be bought            
        with dpg.item_handler_registry(tag = 'islandClickRegistry'):
            dpg.add_item_clicked_handler(callback = islandClick)    
        dpg.bind_item_handler_registry('islandPlot', 'islandClickRegistry')

#Try to unlock the island            
def attemptIslandUnlock(index, loadingStuff = False):
    if index == 0:
        return
    
    global activatedIslands
    
    #Same thing as index - 2^floor(logbase(2,index)) - 1 which gets the index of the node compared to the current layer
    islandLayerIndex = index - (1 << (index + 1).bit_length() - 1) + 1
    #Also does teh same thing, just with the previous layer
    prevIslandLayerIndex = islandLayerIndex // 2 + (1 << (index + 1).bit_length() - 2) - 1
    
    if (activatedIslands[prevIslandLayerIndex] and not activatedIslands[index]) or loadingStuff:
        #Basically just writes the overlaying green arrow
        def succecfulIslandUnlock():
            p1 = islandPositions[index]
            p3 = islandPositions[prevIslandLayerIndex]
            #Finds arrow
            p2 = (p1[0] + p3[0]) / 2, (p1[1] + p3[1]) / 2
            pLeft = (p3[0] - p1[0] - p3[1] + p1[1]) * arrowSize + p2[0], (p3[0] - p1[0] + p3[1] - p1[1]) * arrowSize + p2[1]
            pRight = (p3[0] - p1[0] + p3[1] - p1[1]) * arrowSize + p2[0], (p3[1] - p1[1] - p3[0] + p1[0]) * arrowSize + p2[1]
            #Draws circle ends
            dpg.draw_circle(p1, arrowThickness / 4, fill = (0,130,0), parent = 'islandPlot')
            dpg.draw_circle(p2, arrowThickness / 4, fill = (0,130,0), parent = 'islandPlot')
            dpg.draw_circle(p3, arrowThickness / 4, fill = (0,130,0), parent = 'islandPlot')
            dpg.draw_circle(pRight, arrowThickness / 2, fill = (0,130,0), parent = 'islandPlot')
            dpg.draw_circle(pLeft, arrowThickness / 2, fill = (0,130,0), parent = 'islandPlot')
            #Draws the lines
            dpg.draw_line(p2, pRight, thickness = arrowThickness / 2 , color = (0,130,0), parent = 'islandPlot')  
            dpg.draw_line(p2, pLeft, thickness = arrowThickness / 2, color = (0,130,0), parent = 'islandPlot')
            dpg.draw_line(islandPositions[prevIslandLayerIndex], islandPositions[index], thickness = arrowThickness / 2, color = (0,130,0), parent = 'islandPlot')
            #Add multiplier reward for islands and show island is acitvated
            gps.addGreenPointsMultiplier(islandMultipliers[index])
            activatedIslands[index] = True
            #The max task Amount is added also as a reward and updaete so more tasks
            task.maxTaskAmount += 2
            task.updateTaskAmount()
            #Removes the price tag cause bough
            dpg.delete_item('islandPriceTag' + str(index))
        
        #If adding because loading in, no need to buy because user already did
        if loadingStuff:
            succecfulIslandUnlock()
        else:
            #Buy island
            gps.decrementGreenPoints(islandPrice[index], succecfulIslandUnlock)
        
        
