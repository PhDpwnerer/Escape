import pygame
from pygamegame import PygameGame
import random

class Psycopath(pygame.sprite.Sprite):
    
    #remember to implement a sprint mechanic (2 speeds, stamina bar)
    
    
    def __init__(self, row , col, size, player, maze, mode):
        super().__init__()
        self.cellSize = size
        self.x = col*size+size/2
        self.y = row*size+size/2
        # self.size = 40
        # self.color = (66,244,229)
        self.mode = mode
        
        self.speed = 2
        
        self.timeCounter = 0
        
        self.path = self.pathFinding(player, maze)
        self.destNode = self.path.pop()
        self.startRow, self.startCol = row, col
        
        self.entered = False #to keep track whether the AI is already in player zone
        
        
        
        self.anims = []
        for i in range(4):
            self.anims.append(pygame.image.load("resources/0x72_DungeonTileset_v1.1_individual_sprites/chort_run_anim_f"+str(i)+".png").convert_alpha())
            
        
        #for scaling
        
        for i in range(4):
            w, h = self.anims[i].get_size()
            factor = size/max(w, h)*0.50
            print(factor)
            self.anims[i] = pygame.transform.scale(self.anims[i], (int(factor*w), int(factor*h)))
        
            
        self.animIndex = 0
        
        self.image = self.anims[self.animIndex]
        
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        #self.updateRect()
        
    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.rect = pygame.Rect(int(self.x - w / 2), int(self.y - h / 2), w, h)
        
        
    # def updateRect(self):
    #     self.rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2,
    #                             self.size, 2 * self.size)
    
    # def isColliding(self, wallGroup):
    #     for wall in wallGroup:
    #         if self.rect.colliderect(wall.rect):
    #             return True
    #     return False
        
    ###
    
    def move(self, dx, dy, wallGroup):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, wallGroup)
        if dy != 0:
            self.move_single_axis(0, dy, wallGroup)
    
    def move_single_axis(self, dx, dy, wallGroup):
        
        # Move the rect
        self.x += dx
        self.y += dy
        
        self.updateRect()
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        
        
        
        # If you collide with a wall, move out based on velocity
        for wall in wallGroup:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.x = wall.rect.left-w/2
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.x = wall.rect.right+w/2
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.y = wall.rect.top-h/2
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.y = wall.rect.bottom+h/2
    

          
    def update(self, keysDown, screenWidth, screenHeight, maze, player):

        if self.mode == "multiPlayer":
            if keysDown(pygame.K_LEFT):
                self.move(-self.speed, 0, maze.wallGroup)
            if keysDown(pygame.K_RIGHT):
                self.move(self.speed, 0, maze.wallGroup)
            if keysDown(pygame.K_UP):
                self.move(0, -self.speed, maze.wallGroup)
            if keysDown(pygame.K_DOWN):
                self.move(0, self.speed, maze.wallGroup)
        
        
        if self.mode == "singlePlayer":
            # if len(self.path) == 0:
            #     self.path = self.pathFinding(player, maze)
            #     self.destNode = self.path.pop()
            #     self.startRow, self.startCol = self.destNode.coords
            #     print(player.getCoords())
            #     print(self.getCoords())
            #     print(self.path)
            
            #destNode = path.pop()
            
            psycoRow, psycoCol = self.startRow, self.startCol
            playerRow, playerCol = player.getCoords()
            distance = abs(psycoRow-playerRow)+abs(psycoCol-playerCol)
            if distance <= 2 and self.entered == False: #yeah, magic number
                self.entered = True
                self.path = self.randomPathFinding(player, maze)
                # row, col = self.getCoords()
                # startRow, startCol = row, col
                while len(self.path) == 0:
                    self.path = self.randomPathFinding(player, maze)
                print("exited this while loop")
                self.destNode = self.path.pop()
            elif distance > maze.rows//3:
                self.entered = False
            destRow, destCol = self.destNode.coords
            destY = destRow*maze.cellSize+maze.cellSize/2
            destX = destCol*maze.cellSize+maze.cellSize/2
            if (self.x, self.y) == (destX, destY):
                self.startRow, self.startCol = destRow, destCol
                goal = player.getCoords()
                if (self.startRow, self.startCol) == goal:
                    dx = player.x-self.x
                    dy = player.y-self.y
                    self.move(dx, dy, maze.wallGroup)
                else:
                    if len(self.path) == 0:
                        self.path = self.pathFinding(player, maze)
                    self.destNode = self.path.pop()
            else:
                dx = destCol-self.startCol
                dy = destRow-self.startRow
                if dx == 0 and dy == 0:
                    self.move(destX-self.x, destY-self.y, maze.wallGroup)
                elif abs(self.x-destX) < self.speed and abs(self.y-destY) < self.speed:
                    speed = max(abs(self.x-destX), abs(self.y-destY))
                    self.move(dx*speed, dy*speed, maze.wallGroup)
                else:
                    self.move(dx*self.speed, dy*self.speed, maze.wallGroup)

            
        
        #for sprite animation
        self.timeCounter += 1
        if self.timeCounter%6 == 0:
            self.animIndex += 1
            self.animIndex = self.animIndex%4
        
        self.image = self.anims[self.animIndex]
        
            
            
            
        self.updateRect()
                                
    
    
    #the following pathFinding code was inspired from the A* algorithm http://mnemstudio.org/path-finding-a-star.htm
    def getCoords(self):
        col = int(self.x//self.cellSize)
        row = int(self.y//self.cellSize)
        return (row, col)

    def pathFinding(self, player, maze):
        start = self.getCoords()
        goal = player.getCoords()
        
        self.fringe = []
        self.closed = []
        
        endNode = self.search(start, goal, maze)
        
        pathToFollow = [] #the list will be in reverse (the first item is destination and last item is starting point)
        a = endNode
        #print(type(a))
        while a.parent != None:
            pathToFollow.append(a)
            a = a.parent
        #no need to add the last node (starting point) since we don't have to move to the starting point
        return pathToFollow
        
    def randomPathFinding(self, player, maze):
        start = self.getCoords()
        tempGoal = player.getCoords()
        
        tempGoalRow, tempGoalCol = tempGoal
        directions = [(0,-1), (1,0), (0,1), (-1, 0), (0,0)]
        finalDirection = random.choice(directions)
        dy, dx = finalDirection
        newRow = tempGoalRow+dy
        newCol = tempGoalCol+dx
        
        while not (0 <= newRow <= maze.rows-1) or not(0 <= newCol <= maze.cols-1):
            directions.remove(finalDirection)
            finalDirection = random.choice(directions)
            dy, dx = finalDirection
            newRow = tempGoalRow+dy
            newCol = tempGoalCol+dx
        
        goal = (newRow, newCol)
        print(goal)
        
        
        
        self.fringe = []
        self.closed = []
        
        endNode = self.search(start, goal, maze)
        
        pathToFollow = [] #the list will be in reverse (the first item is destination and last item is starting point)
        a = endNode
        print(type(a))
        while a.parent != None:
            pathToFollow.append(a)
            a = a.parent
        #no need to add the last node (starting point) since we don't have to move to the starting point
        return pathToFollow
        
        
        
        
        
    def search(self, start, goal, maze):
        self.fringe.append(RouteNode(maze, None, start, goal))
        endNode = self.findRoute(maze, goal)
        return endNode
        
    #findRoute is a recursive function
    def findRoute(self, maze, goal):
        if len(self.fringe) == 0:
            print("Here's the error")
            return 0
        else:
            node = self.fringe.pop(0)
            if node.coords == goal:
                return node
            else:
                if not node in self.closed:
                    self.closed.append(node)
                    self.addChildrenToFringe(node, maze, goal)
                return self.findRoute(maze, goal)
                
        
    def addChildrenToFringe(self, parentNode, maze, goal):
        parentCoords = parentNode.coords
        parentRow, parentCol = parentCoords
        directions = [(0,-1), (1,0), (0,1), (-1, 0)]
        for direction in directions:
            dRow, dCol = direction
            newRow = parentRow + dRow
            newCol = parentCol + dCol
            if 0 <= newRow <= maze.rows-1 and 0 <= newCol <= maze.cols-1 and \
                RouteNode(maze,parentNode, (newRow, newCol), goal) not in self.fringe: #if there is lag, we can use binary search, since self.fringe is sorted
                    
                    if direction == (0,1):  #if EAST
                        (south, east) = maze.board[parentRow][parentCol]
                        if east == 0: #basically if no wall is blocking
                            childNode = RouteNode(maze, parentNode, (newRow, newCol), goal)
                            for i in range(len(self.fringe)):
                                if childNode.costF <= self.fringe[i].costF:
                                    self.fringe.insert(i, childNode)
                                    break
                            self.fringe.append(childNode)
                        
                    elif direction == (1,0): #if goes SOUTH since y-axis is inverted
                        (south, east) = maze.board[parentRow][parentCol]
                        if south == 0:
                            childNode = RouteNode(maze, parentNode, (newRow, newCol), goal)
                            for i in range(len(self.fringe)):
                                if childNode.costF <= self.fringe[i].costF:
                                    self.fringe.insert(i, childNode)
                                    break
                            self.fringe.append(childNode)

                    elif direction == (0,-1): #if WEST
                        (south, east) = maze.board[newRow][newCol]
                        if east == 0:
                            childNode = RouteNode(maze, parentNode, (newRow, newCol), goal)
                            for i in range(len(self.fringe)):
                                if childNode.costF <= self.fringe[i].costF:
                                    self.fringe.insert(i, childNode)
                                    break
                            self.fringe.append(childNode)

                    elif direction == (-1,0): #if NORTH
                        (south, east) = maze.board[newRow][newCol]
                        if south == 0:
                            childNode = RouteNode(maze, parentNode, (newRow, newCol), goal)
                            for i in range(len(self.fringe)):
                                if childNode.costF <= self.fringe[i].costF:
                                    self.fringe.insert(i, childNode)
                                    break
                            self.fringe.append(childNode)
                                
    
    
class RouteNode():
    def __init__(self, map, parent, coords, goal):
        self.map = map
        self.coords = coords
        self.row, self.col = self.coords
        self.rowGoal, self.colGoal = goal
        self.parent = parent
        if self.parent != None:
            self.costG = self.parent.costG + 1
        else:
            self.costG = 0
        self.costH = abs(self.row-self.rowGoal)+abs(self.col-self.colGoal)
        self.costF = self.costG = self.costH
        
    def __eq__(self, other):
        return (isinstance(other, RouteNode) and (self.coords == other.coords))
        
    def __repr__(self):
        return "("+str(self.row)+","+str(self.col)+")"