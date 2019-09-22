import pygame

class Hatch(pygame.sprite.Sprite):
    def __init__(self, row, col, cellSize):
        super().__init__()
        
        self.factor = (cellSize/2)/16 #(cellZise/2) represents the width since all the wall sprites are 16x16 pixels
        hatchImage = pygame.image.load("resources/0x72_DungeonTileset_v1.1_individual_sprites/floor_ladder.png").convert_alpha()
        w, h = hatchImage.get_size()
        hatchImage = pygame.transform.scale(hatchImage, (int(self.factor*w), int(self.factor*h)))
        self.image = hatchImage
        x = (col)*cellSize+cellSize//4
        y = (row)*cellSize+cellSize//4
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