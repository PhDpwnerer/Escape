import pygame
import random

from pygamegame import PygameGame
from Character import *
from Maze import *
from Wall import *
from Floor import *
from Psycopath import *


class Demo(PygameGame):
    def init(self):
        self.mode = "mainMenu"
        
        #font is from https://fontzone.net/font-details/diablo-heavy
        self.font = pygame.font.Font('Resources/diablo_h.ttf', 48)
        self.fontBig = pygame.font.Font('Resources/diablo_h.ttf', 96)
        
        #image is from https://rpg.ambient-mixer.com/creepy-dungeon
        self.backgroundImage = pygame.image.load("Resources/Background.jpg").convert_alpha()
        w, h = self.backgroundImage.get_size()
        factor = max(1280/w, 720/h)
        self.backgroundImage = pygame.transform.scale(self.backgroundImage, (int(factor*w), int(factor*h)))
        self.backgroundImageRect = (0,0)
        
        
        #music is from https://tabletopaudio.com/
        pygame.mixer.music.load("Resources/65_Dungeon_I.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        
        
        if self.mode == "mainMenu":
            self.mainMenuInit()
        
        if self.mode == "controls":
            self.controlsInit()
        
        if self.mode == "singlePlayer":
            self.singlePlayerInit()
            
        if self.mode == "multiPlayer":
            self.multiPlayerInit()
            
        if self.mode == "gameOver":
            self.gameOverInit()    
    
    def mainMenuInit(self):
        self.score = -1
        
        
        #self.titleSurface = pygame.Surface((640, 120))
        self.titleText = self.fontBig.render("ESCAPE", True, (255, 255, 255))
        #self.titleSurface.blit(self.titleText, (120, 12))
        self.titleSurfaceRect = (440, 60)
        
        self.singlePlayerSurface = pygame.Surface((640, 60))
        self.multiPlayerSurface = pygame.Surface((640, 60))
        self.singlePlayerText = self.font.render('Single Player Mode', True, (255,255,255))
        self.multiPlayerText = self.font.render('Multiplayer Mode', True, (255,255,255))
        pygame.draw.rect(self.singlePlayerSurface, (255, 255, 255), (0,0,640,60), 5)
        pygame.draw.rect(self.multiPlayerSurface, (255, 255, 255), (0,0,640,60), 5)
        self.singlePlayerSurface.blit(self.singlePlayerText, (30, 6))
        self.multiPlayerSurface.blit(self.multiPlayerText, (42, 6))
        
        self.controlsSurface = pygame.Surface((640, 60))
        self.controlsText = self.font.render("Controls", True, (255, 255, 255))
        pygame.draw.rect(self.controlsSurface, (255, 255, 255), (0,0,640,60), 5)
        self.controlsSurface.blit(self.controlsText, (170, 6))
        
        
        self.singlePlayerSurfaceRect = (320, 240, 640, 60)
        self.multiPlayerSurfaceRect = (320, 360, 640, 60)
        self.controlsSurfaceRect = (320, 480, 640, 60)
        
        
    def controlsInit(self):
        self.controlsTitleText = self.fontBig.render("CONTROLS", True, (255, 255, 255))
        self.controlsTitleTextRect = (320, 60)
        
        self.singleControlTitle = self.font.render("Single Player:", True, (255, 255, 255))
        self.singleControlPlayer = self.font.render("Movement - W,A,S,D", True, (255, 255, 255))
        
        self.singleControlTitleRect = (320, 240, 640, 60)
        self.singleControlPlayerRect = (320, 300, 640, 60)
        
        
        self.multiControlTitle = self.font.render("Multiplayer:", True, (255, 255, 255))
        self.multiControlPlayer = self.font.render("Movement - W,A,S,D", True, (255, 255, 255))
        self.multiControlPsycopath = self.font.render("Movement - Arrow Keys", True, (255, 255, 255))
        
        self.multiControlTitleRect = (320, 420, 640, 60)
        self.multiControlPlayerRect = (320, 480, 640, 60)
        self.multiControlPsycopathRect = (320, 540, 640, 60)
        
        
        self.backSurface = pygame.Surface((200, 60))
        pygame.draw.rect(self.backSurface, (255, 255, 255), (0,0,200,60), 2)
        self.backText = self.font.render("Back", True, (255, 255, 255))
        self.backSurface.blit(self.backText, (30, 6))
        self.backSurfaceRect = (1030, 630)
        
        
        
        
    def singlePlayerInit(self):
        self.score += 1
        self.scoreText = self.font.render("Score: "+str(self.score), True, (255, 255, 255))
        # self.scoreSurface = pygame.Surface((280, 60))
        # pygame.draw.rect(self.scoreSurface, (255, 255, 255), (0,0,280,60), 2)
        # self.scoreSurface.blit(self.scoreText, (6, 6))
        self.scoreSurfaceRect = (1000, 600)
        
        
        self.maze = MazeRecursive(9,16)
        row = random.randint(0,len(self.maze.board)-1)
        col = random.randint(0,len(self.maze.board[0])-1)

        
        self.player = Character(row, col, self.maze.cellSize)
        self.playerGroup = pygame.sprite.GroupSingle(self.player)
        
        rowPsyco = random.randint(0,len(self.maze.board)-1)
        colPsyco = random.randint(0,len(self.maze.board[0])-1)
        
        self.psycopath = Psycopath(rowPsyco, colPsyco, self.maze.cellSize, self.player, self.maze, "singlePlayer")
        self.psycopathGroup = pygame.sprite.GroupSingle(self.psycopath)
        
        self.darknessOn = True
        self.darkness = pygame.image.load("Resources/Darkness.png")
        w, h = self.darkness.get_size()
        self.darkness = pygame.transform.scale(self.darkness, (w*2, h*2))
        self.darknessRect = None
        self.darknessRectUpdate()
    
    def darknessRectUpdate(self):
        x, y = self.player.x, self.player.y
        darknessX = x-1280
        darknessY = y-720
        self.darknessRect = (darknessX, darknessY)
        
        
        
        
    def multiPlayerInit(self):
        self.score += 1
        self.scoreText = self.font.render("Score: "+str(self.score), True, (255, 255, 255))
        # self.scoreSurface = pygame.Surface((280, 60))
        # pygame.draw.rect(self.scoreSurface, (255, 255, 255), (0,0,280,60), 2)
        # self.scoreSurface.blit(self.scoreText, (6, 6))
        self.scoreSurfaceRect = (1000, 600)
        
        self.maze = MazeRecursive(9,16)
        row = random.randint(0,len(self.maze.board)-1)
        col = random.randint(0,len(self.maze.board[0])-1)

        
        self.player = Character(row, col, self.maze.cellSize)
        self.playerGroup = pygame.sprite.GroupSingle(self.player)
        
        rowPsyco = random.randint(0,len(self.maze.board)-1)
        colPsyco = random.randint(0,len(self.maze.board[0])-1)
        
        self.psycopath = Psycopath(rowPsyco, colPsyco, self.maze.cellSize, self.player, self.maze, "multiPlayer")
        self.psycopathGroup = pygame.sprite.GroupSingle(self.psycopath)
        
    def gameOverInit(self):
        self.gameOverText = self.fontBig.render('GAME OVER', True, (255, 255, 255))
        self.gameOverTextRect = (320, 60)
        #score Text is already created elsewhere
        self.exitText = self.font.render("Press ESC to return to Main Menu", True, (255, 255, 255))
        self.scoreTextRect = (520, 240)
        self.exitTextRect =  (120, 480)
    
    
    
    
    def mousePressed(self, x, y):
        if self.mode == "mainMenu":
            print("I am clicking")
            print(x,y)
            print(self.mode)
            if (320 <= x <= 960) and (240 <= y <= 300):
                self.mode = "singlePlayer"
                self.singlePlayerInit()
            elif (320 <= x <= 960) and (360 <= y <= 420):
                self.mode = "multiPlayer"
                self.multiPlayerInit()
            elif (320 <= x <= 960) and (480 <= y <= 540):
                self.mode = "controls"
                self.controlsInit()
        elif self.mode == "controls":
            print("I am clicking")
            print(x,y)
            print(self.mode)
            if (1030 <= x <= 1270) and (630 <= y <= 690):
                self.mode = "mainMenu"
                self.mainMenuInit()

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        # if keyCode == pygame.K_a:
        #     self.player.x -= self.player.speed
        # elif keyCode == pygame.K_d:
        #     self.player.x += self.player.speed
        # elif keyCode == pygame.K_w:
        #     self.player.y -= self.player.speed
        # elif keyCode == pygame.K_s:
        #     self.player.y += self.player.speed
        # self.player.updateRect()
        
        # if keyCode == pygame.K_z:
        #     self.mode = "sprites"
        # elif keyCode == pygame.K_x:
        #     self.mode = "lines"
        # elif keyCode == pygame.K_r:
        #     self.init()
        # elif keyCode == pygame.K_p:
        #     print(self.player.getCoords())
        #     print(self.psycopath.getCoords())
        #     print(self.psycopath.path)
        #     print(self.psycopath.destNode)
        
        if self.mode == "gameOver":
            if keyCode == pygame.K_ESCAPE:
                self.mode = "mainMenu"
                self.mainMenuInit()
        elif self.mode == "singlePlayer":
            if keyCode == pygame.K_p:
                if self.darknessOn:
                    self.darknessOn = False
                else:
                    self.darknessOn = True
        
    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        if self.mode == "singlePlayer" or self.mode == "multiPlayer":
            self.playerGroup.update(self.isKeyPressed, self.width, self.height, self.maze.wallGroup)
            self.psycopathGroup.update(self.isKeyPressed, self.width, self.height, self.maze, self.player) #changed the parameter for this one (self.maze)
        
        if self.mode == "singlePlayer":
            if self.darknessOn:
                self.darknessRectUpdate()
            for hatch in self.maze.hatchGroup:
                if pygame.sprite.collide_rect(self.player, hatch):
                    #self.score += 1
                    self.singlePlayerInit()
                    
            if pygame.sprite.collide_rect(self.player, self.psycopath):
                self.mode = "gameOver"
                self.gameOverInit()
        
        if self.mode == "multiPlayer":
            for hatch in self.maze.hatchGroup:
                if pygame.sprite.collide_rect(self.player, hatch):
                    #self.score += 1
                    self.multiPlayerInit()
            if pygame.sprite.collide_rect(self.player, self.psycopath):
                self.mode = "gameOver"
                self.gameOverInit()

    def redrawAll(self, screen):
        
        ### For testing out the maze generation code
        # if self.mode == "lines":            
        #     width = self.maze.cellSize//2
        #     for row in range(len(self.maze.board)):
        #         for col in range(len(self.maze.board[0])):
        #             southWall, eastWall = self.maze.board[row][col]
        #             if southWall == 1:
        #                 pygame.draw.line(screen, (0,0,0), (col*self.maze.cellSize-(width/2-1), (row+1)*self.maze.cellSize), ((col+1)*self.maze.cellSize+(width/2-1), (row+1)*self.maze.cellSize), width)
        #             if eastWall == 1:
        #                 pygame.draw.line(screen, (0,0,0), ((col+1)*self.maze.cellSize, row*self.maze.cellSize-(width/2-1)), ((col+1)*self.maze.cellSize, (row+1)*self.maze.cellSize+(width/2-1)), width)
        
        
        ### for mainMenu display
        
        if self.mode == "mainMenu":
            screen.blit(self.backgroundImage, self.backgroundImageRect)
            screen.blit(self.singlePlayerSurface, self.singlePlayerSurfaceRect)
            screen.blit(self.multiPlayerSurface, self.multiPlayerSurfaceRect)
            screen.blit(self.titleText, self.titleSurfaceRect)
            screen.blit(self.controlsSurface, self.controlsSurfaceRect)
            
        ### for controls display
        
        if self.mode == "controls":
            screen.blit(self.backgroundImage, self.backgroundImageRect)
            screen.blit(self.controlsTitleText, self.controlsTitleTextRect)
            screen.blit(self.singleControlTitle, self.singleControlTitleRect)
            screen.blit(self.singleControlPlayer, self.singleControlPlayerRect)
            screen.blit(self.multiControlTitle, self.multiControlTitleRect)
            screen.blit(self.multiControlPlayer, self.multiControlPlayerRect)
            screen.blit(self.multiControlPsycopath, self.multiControlPsycopathRect)
            screen.blit(self.backSurface, self.backSurfaceRect)
            
        ### for gameOver display
        
        if self.mode == "gameOver":
            screen.blit(self.backgroundImage, self.backgroundImageRect)
            screen.blit(self.gameOverText, self.gameOverTextRect)
            screen.blit(self.scoreText, self.scoreTextRect)
            screen.blit(self.exitText, self.exitTextRect)
        
        ### for singlePlayer and multiPlayer game modes
        if self.mode == "singlePlayer":
            self.maze.floorGroup.draw(screen)
            self.maze.wallGroup.draw(screen)
            self.maze.hatchGroup.draw(screen)
            
            
            self.playerGroup.draw(screen)
            self.psycopathGroup.draw(screen)
            
            screen.blit(self.scoreText, self.scoreSurfaceRect)
            if self.darknessOn:
                screen.blit(self.darkness, self.darknessRect)
            
        if self.mode == "multiPlayer":
            self.maze.floorGroup.draw(screen)
            self.maze.wallGroup.draw(screen)
            self.maze.hatchGroup.draw(screen)
            
            self.playerGroup.draw(screen)
            self.psycopathGroup.draw(screen) 
            
            screen.blit(self.scoreText, self.scoreSurfaceRect)
        
        
            
                    
        
def main():
    game = Demo()
    game.run()

if __name__ == '__main__':
    main()