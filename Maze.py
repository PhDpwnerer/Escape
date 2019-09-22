import random
import copy
from Wall import *
from Floor import *
from Hatch import *


#the maze algorithm is Recursive Backtracking, which is inspired from http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking
class MazeRecursive(object):
    def __init__(self, rows, cols):
        #(south,east), 1 signifies there is a wall
        self.board = [[(1,1)]*cols for i in range(rows)] 
        #self.walls = [[1]*33 for i in range(19)]
        self.rows = rows
        self.cols = cols
        self.cellHeight = 720//rows
        self.cellWidth = 1280//cols
        
        
        self.cellSize = min(self.cellHeight, self.cellWidth) ### Let's figure this out later 
        self.startRow =  random.randint(0,rows-1)
        self.startCol =  random.randint(0,cols-1)
        #self.row = self.startRow
        #self.col = self.startCol
        self.directions = [(0,-1), (1,0), (0,1), (-1, 0)]
        self.carvePassagesFrom(self.startRow, self.startCol)
        self.wallGroup = pygame.sprite.Group()
        self.wallSprites()
        self.floorGroup = pygame.sprite.Group()
        self.floorSprites()
        
        self.hatchRow = random.randint(0,rows-1)
        self.hatchCol = random.randint(0, cols-1) 
        self.hatch = Hatch(self.hatchRow, self.hatchCol, self.cellSize)
        self.hatchGroup = pygame.sprite.Group(self.hatch)
        self.hatchRow2 = random.randint(0,rows-1)
        self.hatchCol2 = random.randint(0, cols-1)
        self.hatch2 = Hatch(self.hatchRow2, self.hatchCol2, self.cellSize)
        self.hatchGroup.add(self.hatch2)
        
        
        
    def carvePassagesFrom(self, row, col, visited=None): #no need for board as parameter, because already have self
        if visited == None:
            visited = set()
            #visited.add((row, col))
        #base case
        # if row == self.startRow and col == self.startCol and len(visited) != 0: 
        #     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        #     print(visited)
        #     print(len(visited))
        #     return #to simply end the function
        #else:
        directions = copy.deepcopy(self.directions) #to avoid aliasing issues
        random.shuffle(directions) #so that the "wall carving" is randomized
        for direction in directions:
            dRow, dCol = direction
            newRow = row + dRow
            newCol = col + dCol
            if 0 <= newRow <= self.rows-1 and 0 <= newCol <= self.cols-1 and \
                (newRow, newCol) not in visited:
                    visited.add((newRow, newCol))
                    if direction == (0,1):  #if EAST
                        (south, east) = self.board[row][col]
                        east = 0
                        self.board[row][col] = (south, east)
                    elif direction == (1,0): #if goes SOUTH since y-axis is inverted
                        (south, east) = self.board[row][col]
                        south = 0
                        self.board[row][col] = (south, east)
                    elif direction == (0,-1): #if WEST
                        (south, east) = self.board[newRow][newCol]
                        east = 0
                        self.board[newRow][newCol] = (south, east)
                    elif direction == (-1,0): #if NORTH
                        (south, east) = self.board[newRow][newCol]
                        south = 0
                        self.board[newRow][newCol] = (south, east)
                    ###???????????????????
                    self.carvePassagesFrom(newRow, newCol, visited)
                    #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
                    #print(len(visited))
                    
    def wallSprites(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                southWall, eastWall = self.board[row][col]
                if southWall == 1:
                    self.wallGroup.add(Wall(row, col, self.cellSize, "south"))
                if eastWall == 1:
                    self.wallGroup.add(Wall(row, col, self.cellSize, "east"))
        
        for col in range(-1,len(self.board[0])):
            row = -1
            self.wallGroup.add(Wall(row, col, self.cellSize, "south"))
        
        for row in range(-1,len(self.board)):
            col = -1
            self.wallGroup.add(Wall(row, col, self.cellSize, "east"))
    
    def floorSprites(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                self.floorGroup.add(Floor(row, col, self.cellSize))
                            
                    
        
        

# a = MazeNoLoop(18, 32)
# print(a.board)