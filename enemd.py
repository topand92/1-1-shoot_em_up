import math
import os
import pygame
from defmd import *

##############################보스 클래스#######################################
            
class Boss(pygame.sprite.Sprite):
    def __init__(self, hp, xpos, ypos, address):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, address)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (500, 350))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.hp = hp
        self.dx = 0
        self.dy = 0
        self.sx, self.sy = self.image.get_size()
        
    def update(self):
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def crash(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite
      
##############################적 객체#######################################
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, hp, xsize, ysize, xpos, ypos, speed, address):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(os.path.join(image_path, address)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (xsize, ysize))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.sx = xsize
        self.sy = ysize
        self.speed = speed
        self.hp = hp
        self.orig_image = self.image
        
    def update(self, x, y):
        self.orig_center = self.rect.center
        self.image = pygame.transform.rotate(self.orig_image, catchangle(self.rect.x + self.sx/2, self.rect.y + self.sy/2, x, y))
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
    def out_of_screen(self):
        if self.rect.y < 0 or self.rect.y > WINDOW_HEIGHT:
            return True
            
    def draw(self, screen):
        self.rect = self.image.get_rect(self.orig_center)
        screen.blit(self.image, self.rect)
        
    def crash(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite
            
##############################적 무기 객체#######################################
        
class Enemy_Weapon(pygame.sprite.Sprite):
    def __init__(self, xsize, ysize, xpos, ypos, speed, x, y, address):
        super(Enemy_Weapon, self).__init__()
        self.image = pygame.image.load(os.path.join(image_path, address)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (xsize, ysize))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.sx = xsize
        self.sy = ysize
        self.speed = speed
        self.orig_image = self.image
        self.orig_center = self.rect.center
        self.image = pygame.transform.rotate(self.orig_image, catchangle(self.rect.x + self.sx/2, self.rect.y + self.sy/2, x, y))
        self.degrees = math.atan2(y - self.rect.y, x - self.rect.x)
        
    def update(self, x, y):
        self.rect.x += math.cos(self.degrees) * self.speed
        self.rect.y += math.sin(self.degrees) * self.speed
        if self.rect.x + WINDOW_WIDTH < 0 or self.rect.x > WINDOW_WIDTH:
            self.kill()
        if self.rect.y + WINDOW_HEIGHT < 0 or self.rect.y > WINDOW_HEIGHT:
            self.kill()
    
    def out_of_screen(self):
        if self.rect.x + WINDOW_WIDTH < 0 or self.rect.x > WINDOW_WIDTH:
            return True
        if self.rect.y + WINDOW_HEIGHT < 0 or self.rect.y > WINDOW_HEIGHT:
            return True
            
    def draw(self, screen):
        self.rect = self.image.get_rect(self.orig_center)
        screen.blit(self.image, self.rect)
        
    def crash(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite

##############################각도 구하는 함수#######################################
        
def catchangle(x1, y1, x2, y2):
    y = y1 - y2
    x = x1 - x2
    angle = math.atan2(y, x)
    angle = angle * (180/math.pi)
    angle = -(angle + 90) % 360
    return angle