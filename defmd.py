import os
import pygame

########################기본 색깔, 화면 크기, FPS 설정#################

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (250,250,50)
RED = (250,50,50)

FPS = 60

########################파일 경로 불러오기#############################

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")
sound_path = os.path.join(current_path, "sounds")
music_path = os.path.join(current_path, "musics")

##############################아이템 객체#######################################
            
class Item(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, address):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(image_path, address)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.speed = 1
        self.sx, self.sy = self.image.get_size()
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.y + self.rect.height < 0:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
            
    def crash(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite
      
##############################텍스트 그리는 함수#######################################

def draw_text(text, font, surface, x, y, main_color):
    text_obj = font.render(text, True, main_color)
    text_rect = text_obj.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surface.blit(text_obj, text_rect)
    
##############################폭발 효과 함수#######################################
    
def occur_explosion(surface, x, y, xsize, ysize):
    explosion_images = pygame.image.load(os.path.join(image_path, "폭발 이미지.png")).convert_alpha()     
    explosion_images = pygame.transform.scale(explosion_images, (xsize, ysize))
    explosion_rect = explosion_images.get_rect()
    explosion_rect.x = x
    explosion_rect.y = y
    surface.blit(explosion_images, explosion_rect)    
    explosion_sound = pygame.mixer.Sound(os.path.join(sound_path, "폭발 효과음.wav"))
    explosion_sound.play()
    
##############################아이템 획득 효과 함수#######################################

def occur_get_item():
    get_item_sound = pygame.mixer.Sound(os.path.join(sound_path, "아이템 획득 효과음.wav"))
    get_item_sound.play()