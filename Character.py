import pygame
from pygamegame import PygameGame

class Character(pygame.sprite.Sprite):
    
    #remember to implement a sprint mechanic (2 speeds, stamina bar)
    
    
    def __init__(self, row , col, size):
        super().__init__()
        self.cellSize = size
        self.x = col*size+size/2
        self.y = row*size+size/2
        # self.size = 40
        # self.color = (66,244,229)
        
        self.idleSpeed = 2
        self.runSpeed = 3
        self.speed = self.idleSpeed
        self.timeCounter = 0
        
        # self.image = pygame.Surface((40, 40))
        # self.rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2,
        #                         self.size, self.size)
        # pygame.draw.rect(self.image, self.color, (0,0,self.size,self.size))
        
        self.idleAnims = []
        self.runAnims = []
        for i in range(4):
            self.idleAnims.append(pygame.image.load("resources/0x72_DungeonTileset_v1.1_individual_sprites/knight_m_idle_anim_f"+str(i)+".png").convert_alpha())
            self.runAnims.append(pygame.image.load("resources/0x72_DungeonTileset_v1.1_individual_sprites/knight_m_run_anim_f"+str(i)+".png").convert_alpha())
        
        #for scaling
        
        for i in range(4):
            w, h = self.idleAnims[i].get_size()
            factor = size/max(w, h)*0.50
            print(factor)
            self.idleAnims[i] = pygame.transform.scale(self.idleAnims[i], (int(factor*w), int(factor*h)))
            w, h = self.runAnims[i].get_size()
            factor = size/max(w, h)*0.50
            self.runAnims[i] = pygame.transform.scale(self.runAnims[i], (int(factor*w), int(factor*h)))
        
            
        self.animIndex = 0
        self.mode = "idle"
        
        self.image = self.idleAnims[self.animIndex]
        
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        #self.updateRect()
        
    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)
        
        
    # def updateRect(self):
    #     self.rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2,
    #                             self.size, 2 * self.size)
    
    def isColliding(self, wallGroup):
        for wall in wallGroup:
            if self.rect.colliderect(wall.rect):
                return True
        return False
        
    ### Any code related to collision below is inspired from https://www.pygame.org/project-Rect+Collision+Response-1061-.html
    
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
    
    def getCoords(self):
        col = int(self.x//self.cellSize)
        row = int(self.y//self.cellSize)
        return (row, col)
    
                                
    def update(self, keysDown, screenWidth, screenHeight, wallGroup):
        if keysDown(pygame.K_LSHIFT):
            self.speed = self.runSpeed
            self.mode = "run"
        else:
            self.speed = self.idleSpeed
            self.mode = "idle"
        originalX = self.x
        originalY = self.y    
        # if keysDown(pygame.K_a):
        #     if not self.isColliding(wallGroup):
        #         self.x -= self.speed
        # if keysDown(pygame.K_d):
        #     if not self.isColliding(wallGroup):
        #         self.x += self.speed
        # if keysDown(pygame.K_w):
        #     if not self.isColliding(wallGroup):
        #         self.y -= self.speed
        # if keysDown(pygame.K_s):
        #     if not self.isColliding(wallGroup):
        #         self.y += self.speed
        
        # if keysDown(pygame.K_a):
        #     self.x -= self.speed
        # if keysDown(pygame.K_d):
        #     self.x += self.speed
        # if keysDown(pygame.K_w):
        #     self.y -= self.speed
        # if keysDown(pygame.K_s):
        #     self.y += self.speed
        
        
        ###
        if keysDown(pygame.K_a):
            self.move(-self.speed, 0, wallGroup)
        if keysDown(pygame.K_d):
            self.move(self.speed, 0, wallGroup)
        if keysDown(pygame.K_w):
            self.move(0, -self.speed, wallGroup)
        if keysDown(pygame.K_s):
            self.move(0, self.speed, wallGroup)
        
                
        # dx = self.x - originalX
        # dy = self.y - originalY
        
        
            
        #for collisions with walls in wallGroup
        #inspired by code in https://www.pygame.org/project-Rect+Collision+Response-1061-.html
        # w, h = self.image.get_size()
        # for wall in wallGroup:
        #     if self.rect.colliderect(wall.rect):
        #         print("Colliding")
        #         if dx < 0:
        #             print("a")
        #             
        #             self.rect.left = wall.rect.right
        #             #self.x = self.rect.left+w/2
        #         if dx > 0:
        #             print("d")
        #             self.rect.right = wall.rect.left
        #             #self.x = self.rect.right-w/2
        #         if dy < 0:
        #             print("w")
        #             self.rect.top = wall.rect.bottom
        #             #self.y = self.rect.top+h/2
        #         if dy > 0:
        #             print("s")
        #             self.rect.bottom = wall.rect.top
        #             #self.y = self.rect.bottom-h/2
            
        
        #for sprite animation
        self.timeCounter += 1
        if self.timeCounter%6 == 0:
            self.animIndex += 1
            self.animIndex = self.animIndex%4
        if self.mode == "run":
            self.image = self.runAnims[self.animIndex]
        elif self.mode == "idle":
            self.image = self.idleAnims[self.animIndex]
            
            
            
        self.updateRect()
                                
    
        
    