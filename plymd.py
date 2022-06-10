import os
import pygame
from defmd import *

########################게임 플레이어 클래스#############################

class Player(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, address):
        super(Player, self).__init__()
        self.image = pygame.image.load(os.path.join(image_path, address)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = xpos
        self.rect.y = ypos
        self.sx = 50
        self.sy = 80
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if self.rect.x < 0 or self.rect.x + self.rect.width > WINDOW_WIDTH:
            self.rect.x -= self.dx
            
        if self.rect.y < 0 or self.rect.y + self.rect.height > WINDOW_HEIGHT:
            self.rect.y -= self.dy

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def crash(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite

##############################플레이어 무기 클래스#######################################
            
class Player_Weapon(pygame.sprite.Sprite):
    def __init__(self, xsize, ysize, xpos, ypos, speed, address):
        super(Player_Weapon, self).__init__()
        self.image = pygame.image.load(os.path.join(image_path, address)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (xsize, ysize))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = speed
        self.sound = pygame.mixer.Sound(os.path.join(sound_path, "플레이어 총알 발사 효과음.wav"))
        
    def launch(self):
        self.sound.play()
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
            
    def crash(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite