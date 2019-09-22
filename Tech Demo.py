# mazeSolver.py
import pygame
import random

from pygamegame import PygameGame

from tkinter import *

import math

class MazeGenerator(PygameGame):
    

##################################### draw #####################################

    def redrawAll(self, screen):
        #canvas.create_rectangle(0,0,data.width,data.height,fill = "black")
        self.drawBridges(screen)
        self.drawIslands(screen)
    
    def drawIslands(self, screen):
        islands = self.maze
        rows,cols = len(islands),len(islands[0])
        color = self.islandColor
        r = min(self.cW,self.cH)/6
        for row in range(rows):
            for col in range(cols):
                drawCircle(screen, self.islandCenter(row,col),r,color)
    

    
    def islandCenter(self, row, col):
        if self.isPolar:
            cx,cy = self.width/2,self.height/2
            rows,cols = len(self.maze),len(self.maze[0])
            maxR = min(cx,cy)
            r = maxR*(row+1)/(rows+1)
            theta = 2*math.pi*col/cols
            return cx+r*math.cos(theta), cy-r*math.sin(theta)
        else:
            cellWidth,cellHeight = self.cW,self.cH
            return (int((col+0.5)*cellWidth),int((row+0.5)*cellHeight))
    
    def drawBridges(self, screen):
        islands = self.maze
        rows,cols = len(islands),len(islands[0])
        color = self.bridgeColor
        width = int(min(self.cW,self.cH)/15)
        for r in range(rows):
            for c in range(cols):
                island = islands[r][c]
                if (island.east):
                    pygame.draw.line(screen, color, self.islandCenter(r,c), self.islandCenter(r,c+1), width)
                    
                    # canvas.create_line(islandCenter(self, r,c),
                    #                 islandCenter(self, r,c+1),
                    #                 fill=color, width=width)
                if (island.south):
                    pygame.draw.line(screen, color, self.islandCenter(r,c), self.islandCenter(r+1,c), width)
                    
                    # canvas.create_line(islandCenter(self, r,c),
                    #                 islandCenter(self, r+1,c),
                    #                 fill=color, width=width)
    
    ##################################### init #####################################
    
    def init(self, rows=10, cols=10):
        if (rows < 1): rows = 1
        if (cols < 1): cols = 1
        self.rows = rows
        self.cols = cols
        self.islandColor = (0,0,0)
        self.bridgeColor = (0,0,0)
        self.isPolar = False
        self.path = set()
        self.solution = None
        self.playerSpot = (0,0)
        self.path.add(self.playerSpot)
        margin = 5
        self.cW = (self.width - margin)/cols
        self.cH = (self.height - margin)/rows
        self.margin = margin
        #make the islands
        self.maze = makeBlankMaze(rows,cols)
        #connect the islands
        connectIslands(self.maze)
    
class Struct(object): pass

def drawCircle(screen, position, r, color):
    (cx,cy) = position
    cx = int(cx)
    cy = int(cy)
    r = int(r)
    pygame.draw.circle(screen, color, (cx, cy), r, 0)
    #canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)

def makeIsland(number):
    island = Struct()
    island.east = island.south = False
    island.number = number
    return island

def makeBlankMaze(rows,cols):
    islands = [[0]*cols for row in range(rows)]
    counter = 0
    for row in range(rows):
        for col in range(cols):
            islands[row][col] = makeIsland(counter)
            counter+=1
    return islands

def connectIslands(islands):
    rows,cols = len(islands),len(islands[0])
    for i in range(rows*cols-1):
        makeBridge(islands)

def makeBridge(islands):
    rows,cols = len(islands),len(islands[0])
    while True:
        row,col = random.randint(0,rows-1),random.randint(0,cols-1)
        start = islands[row][col]
        if flipCoin(): #try to go east
            if col==cols-1: continue
            target = islands[row][col+1]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.east = True
            renameIslands(start,target,islands)
        else: #try to go south
            if row==rows-1: continue
            target = islands[row+1][col]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.south = True
            renameIslands(start,target,islands)
        #only got here if a bridge was made
        return

def renameIslands(i1,i2,islands):
    n1,n2 = i1.number,i2.number
    lo,hi = min(n1,n2),max(n1,n2)
    for row in islands:
        for island in row:
            if island.number==hi: island.number=lo

def flipCoin():
    return random.choice([True, False])

def mousePressed(event, data): pass

def timerFired(data): pass
    
def main():
    game = MazeGenerator()
    game.run()

if __name__ == '__main__':
    main()