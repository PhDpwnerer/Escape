import pygame
import random

class Floor(pygame.sprite.Sprite):
    def __init__(self, row, col, cellSize):
        super().__init__()
        self.image = pygame.Surface((cellSize*3//2, cellSize*3//2))
        
        self.factor = (cellSize/2)/16 #(cellSize/2) represents the width since all the wall sprites are 16x16 pixels
        
        #separating floor_1.png to make floor look less weird
        self.normalTile = pygame.image.load("resources/0x72_DungeonTileset_v1.1_individual_sprites/floor_1.png").convert_alpha()
        w, h = self.normalTile.get_size()
        self.normalTile = pygame.transform.scale(self.normalTile, (int(self.factor*w), int(self.factor*h)))
        
        
        
        self.specialTiles = []
        for i in range (2, 9):
            tile = pygame.image.load("resources/0x72_DungeonTileset_v1.1_individual_sprites/floor_"+str(i)+".png").convert_alpha()
            w, h = tile.get_size()
            tile = pygame.transform.scale(tile, (int(self.factor*w), int(self.factor*h)))
            self.specialTiles.append(tile)
            
        for i in range(1,7):    
            rectCol = (i-1)%3
            rectRow = (i-1)//3
            chance = random.randint(1,10)
            #so that 9 times out of ten, it's the normal tile
            if chance == 1:
                self.image.blit(random.choice(self.specialTiles), (rectCol*cellSize//2, rectRow*cellSize//2))
            else:
                self.image.blit(self.normalTile,  (rectCol*cellSize//2, rectRow*cellSize//2))
        
        x = (col)*cellSize-cellSize//4
        y = (row)*cellSize-cellSize//4
        w, h = self.image.get_size()
        self.rect = pygame.Rect(x, y, w, h)
        
    # def updateRect(self):
    #     self.rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2,
    #                             self.size, 2 * self.size)
                                
    # def update(self, keysDown, screenWidth, screenHeight):
    #     # if keysDown(pygame.K_a):
    #     #     self.x -= self.speed
    #     # if keysDown(pygame.K_d):
    #     #     self.x += self.speed
    #     # if keysDown(pygame.K_w):
    #     #     self.y -= self.speed
    #     # if keysDown(pygame.K_s):
    #     #     self.y += self.speed
    #     self.updateRect()