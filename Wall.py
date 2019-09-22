import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, row, col, cellSize, orientation):
        super().__init__()
        
        self.factor = (cellSize/2)/16 #(cellZise/2) represents the width since all the wall sprites are 16x16 pixels
        wallImage = pygame.image.load("resources/0x72_DungeonTileset_v1.1_individual_sprites/wall_mid.png").convert_alpha()
        w, h = wallImage.get_size()
        wallImage = pygame.transform.scale(wallImage, (int(self.factor*w), int(self.factor*h)))
        
        
        if orientation == "south":
            #want to make two wall blocks for the self.image
            #reminder: Surface((width, height))
            #reminder: blit(source, dest, area=None, special_flags = 0)
            self.image = pygame.Surface(((cellSize//2)*3, cellSize//2))
            self.image.blit(wallImage, (0,0))
            self.image.blit(wallImage, ((cellSize//2), 0))
            self.image.blit(wallImage, ((cellSize//2)*2, 0))
            x = (col)*cellSize-cellSize//4
            y = (row+1)*cellSize-cellSize//4
            w, h = self.image.get_size()
            self.rect = pygame.Rect(x, y, w, h*.80) #multiply by 0.80 because of sprite whitespace
        elif orientation == "east":
            self.image = pygame.Surface((cellSize//2, cellSize//2*3))
            self.image.blit(wallImage, (0,0))
            self.image.blit(wallImage, (0, (cellSize//2)))
            self.image.blit(wallImage, (0, (cellSize//2)*2))
            x = (col+1)*cellSize-cellSize//4
            y = (row)*cellSize-cellSize//4
            w, h = self.image.get_size()
            self.rect = pygame.Rect(x, y, w, h*.80)
            
        
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