##############################모듈 불러오기############################
from datetime import datetime
import os
import pygame
import random
import time

from defmd import *
from plymd import *
from enemd import *

##############################게임루프 함수#######################################
def game_loop():
    
    #####디폴트 폰트, 배경이미지, 게임클리어 사운드, 게임오버 사운드, FPS클락 설정######
    default_font = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 20)
    background_image = pygame.image.load(os.path.join(image_path, "배경이미지.png")).convert_alpha()
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))    
    gameover_sound = pygame.mixer.Sound(os.path.join(sound_path, "게임오버 효과음.wav"))
    gameclear_sound = pygame.mixer.Sound(os.path.join(sound_path, "게임 클리어 효과음.wav"))
    pygame.mixer.music.load(os.path.join(music_path, "배경음악.wav"))
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    
    #####(보스와 플레이어 생성), (플레이어 무기, 적들, 적 무기 각각의 스프라이트를 그룹화)######
    boss = Boss(5000, round(WINDOW_WIDTH * 1/2 - 250), 0, "boss.png")
                
    player1 = Player(round(WINDOW_WIDTH * 2/3 - 25), WINDOW_HEIGHT - 80, "player1.png")
    player2 = Player(round(WINDOW_WIDTH * 1/3 - 25), WINDOW_HEIGHT - 80, "player2.png")

    player1_weapons = pygame.sprite.Group()
    player2_weapons = pygame.sprite.Group()
    
    enemy1s = pygame.sprite.Group()
    enemy2s = pygame.sprite.Group()
    
    enemy1_weapons = pygame.sprite.Group()
    enemy2_weapons = pygame.sprite.Group()
    
    weapon_power_items = pygame.sprite.Group()
    weapon_speed_items = pygame.sprite.Group()
    weapon_number_items = pygame.sprite.Group()
    heal_items = pygame.sprite.Group()
    
    #####기본적인 설정######
    occur_prob = 100
    shot_count = 0
    count_missed = 0
    
    players_hp = 300
    
    player1_attack_go1 = False
    player1_attack_go2 = False
    player1_k = 0
    player1_attack_k = 26
    player1_weapon_speed_level = 1
    player1_weapon_power_level = 1
    player1_weapon_number_level = 1
    
    player2_attack_go1 = False
    player2_attack_go2 = False
    player2_k = 0
    player2_attack_k = 26
    player2_weapon_speed_level = 1
    player2_weapon_power_level = 1
    player2_weapon_number_level = 1
    
    enemy_level = 1
    enemy_attack_k = 0
    
    rundic = {4950 : 0, 4900 : 0, 4850 : 0, 4750 : 0, 4650 : 0, 4550 : 0, 4350 : 0, 4050 : 0, 3750 : 0, 3350 : 0, 2950 : 0, 2450 : 0, 1950 : 0, 1450 : 0, 950 : 0}
    
    #####시간 설정######
    start = datetime.now()
    start_time = start.replace(microsecond=0)

    #####반복문######
    done = False
    while not done:
        #####시간표현######
        now = datetime.now()
        now_time = now.replace(microsecond=0)
        delta_time = now_time - start_time
        delta_time_second = round((now - start).total_seconds())
        
        #####입력장치######
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player1.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    player1.dx += 5
                elif event.key == pygame.K_UP:
                    player1.dy -= 5
                elif event.key == pygame.K_DOWN:
                    player1.dy += 5
                elif event.key == pygame.K_KP0:
                    player1_attack_go1 = True
                    player1_k = 0
                    if player1_attack_k - (26 - player1_weapon_speed_level * 3) >= 0 :
                        player1_attack_go2 = True
                        player1_attack_k = 0
                            
                if event.key == pygame.K_a:
                    player2.dx -= 5
                elif event.key == pygame.K_d:
                    player2.dx += 5
                elif event.key == pygame.K_w:
                    player2.dy -= 5
                elif event.key == pygame.K_s:
                    player2.dy += 5
                elif event.key == pygame.K_SPACE:
                    player2_attack_go1 = True
                    player2_k = 0
                    if player2_attack_k - (26 - player2_weapon_speed_level * 3) >= 0 :
                        player2_attack_go2 = True
                        player2_attack_k = 0
    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player1.dx = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player1.dy = 0
                elif event.key == pygame.K_KP0:
                    player1_attack_go1 = False
                    player1_attack_go2 = False
                        
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player2.dx = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    player2.dy = 0
                elif event.key == pygame.K_SPACE:
                    player2_attack_go1 = False
                    player2_attack_go2 = False
                    
        #####플레이어1의 공격######
        if (player1_attack_go1 == True and player1_k % (26 - player1_weapon_speed_level * 3) == 0) and player1_attack_go2 == True :
            if player1_weapon_number_level == 1:
                player1_weapon = Player_Weapon(10, 40, player1.rect.centerx - 5, player1.rect.centery - 40, 15, "총알 {}.png".format(player1_weapon_power_level))
                player1_weapon.launch()
                player1_weapons.add(player1_weapon)
            if player1_weapon_number_level == 2:
                for i in range (player1_weapon_number_level):
                    player1_weapon = Player_Weapon(10, 40, player1.rect.x + player1.sx/4 * (2*i + 1) - 5, player1.rect.centery - 40, 15, "총알 {}.png".format(player1_weapon_power_level))
                    player1_weapon.launch()
                    player1_weapons.add(player1_weapon)
            if player1_weapon_number_level == 3:
                for i in range (player1_weapon_number_level + 1):
                    player1_weapon = Player_Weapon(10, 40, player1.rect.x + player1.sx/3 * i - 5, player1.rect.centery - 40, 15, "총알 {}.png".format(player1_weapon_power_level))
                    player1_weapon.launch()
                    player1_weapons.add(player1_weapon)
            if player1_weapon_number_level == 4:
                for i in range (player1_weapon_number_level + 1):
                    player1_weapon = Player_Weapon(10, 40, player1.rect.x + player1.sx/4 * i - 5, player1.rect.centery - 40, 15, "총알 {}.png".format(player1_weapon_power_level))
                    player1_weapon.launch()
                    player1_weapons.add(player1_weapon)
                    
        #####플레이어2의 공격######
        if (player2_attack_go1 == True and player2_k % (26 - player2_weapon_speed_level * 3) == 0) and player2_attack_go2 == True :
            if player2_weapon_number_level == 1:
                player2_weapon = Player_Weapon(10, 40, player2.rect.centerx - 5, player2.rect.centery - 40, 15, "총알 {}.png".format(player2_weapon_power_level))
                player2_weapon.launch()
                player2_weapons.add(player2_weapon)
            if player2_weapon_number_level == 2:
                for i in range (player2_weapon_number_level):
                    player2_weapon = Player_Weapon(10, 40, player2.rect.x + player2.sx/4 * (2*i + 1) - 5, player2.rect.centery - 40, 15, "총알 {}.png".format(player2_weapon_power_level))
                    player2_weapon.launch()
                    player2_weapons.add(player2_weapon)
            if player2_weapon_number_level == 3:
                for i in range (player2_weapon_number_level + 1):
                    player2_weapon = Player_Weapon(10, 40, player2.rect.x + player2.sx/3 * i - 5, player2.rect.centery - 40, 15, "총알 {}.png".format(player2_weapon_power_level))
                    player2_weapon.launch()
                    player2_weapons.add(player2_weapon)
            if player2_weapon_number_level == 4:
                for i in range (player2_weapon_number_level + 1):
                    player2_weapon = Player_Weapon(10, 40, player2.rect.x + player2.sx/4 * i - 5, player2.rect.centery - 40, 15, "총알 {}.png".format(player2_weapon_power_level))
                    player2_weapon.launch()
                    player2_weapons.add(player2_weapon)
            
        player1_k += 1
        player1_attack_k += 1
        player2_k += 1
        player2_attack_k += 1
        
        ##################배경이미지 그리기#######################        
        screen.blit(background_image, background_image.get_rect())
        
        ##################적들 생성을 위한 설정#######################
        occur_of_enemys = 1 + int(shot_count / 300)
        min_enemy_speed = 1 + int(shot_count / 200)
        max_enemy_speed = 1 + int(shot_count / 100)
        
        ##################적들 생성#######################
        if random.randint(1, occur_prob) == 1:
            for i in range(occur_of_enemys):
                speed = random.randint(min_enemy_speed, max_enemy_speed)
                enemy1 = Enemy(1 * enemy_level, 50, 50, random.randint(0, WINDOW_HEIGHT - 50), 5, speed, "적1.png")
                enemy1s.add(enemy1)
                
                enemy2 = Enemy(1 * enemy_level, 50, 50, random.randint(0, WINDOW_HEIGHT - 50), 5, speed, "적1.png")
                enemy2s.add(enemy2)

        ##################처치한 적들, 놓친 적들, 플레이어 체력, 보스체력 나타내기#######################
        draw_text("kill: {}".format(shot_count), default_font, screen, 50, 20, YELLOW)
        draw_text("loss: {}".format(count_missed), default_font, screen, 50, 50, RED)
        draw_text("time: {}".format(delta_time), default_font, screen, 80, 80, WHITE)
        draw_text("players hp: {}".format(players_hp), default_font, screen, 920, 20, WHITE)
        draw_text("boss hp: {}".format(boss.hp), default_font, screen, 920, 50, WHITE)
        draw_text("enemy level: {}".format(enemy_level), default_font, screen, 915, 80, WHITE)
        
        ##################아이템 생성#######################
        for i in (4950, 4900, 4850, 4750, 4650, 4550, 4350, 4050, 3750, 3350, 2950, 2450, 1950, 1450, 950):

            if boss.hp <= i and rundic[i] == 0:
                heal_item = Item(random.randrange(0, WINDOW_WIDTH - 40), 10, "힐아이템.png")
                heal_items.add(heal_item)
                a = random.randint(1, 3)
                if a == 1:
                    weapon_power_item = Item(random.randrange(0, WINDOW_WIDTH - 40), 10, "파워아이템.png")
                    weapon_power_items.add(weapon_power_item)
                    weapon_speed_item = Item(random.randrange(0, WINDOW_WIDTH - 40), 10, "공속아이템.png")
                    weapon_speed_items.add(weapon_speed_item)
                if a == 2:
                    weapon_speed_item = Item(random.randrange(0, WINDOW_WIDTH - 40), 10, "공속아이템.png")
                    weapon_speed_items.add(weapon_speed_item)
                    weapon_number_item = Item(random.randrange(0, WINDOW_WIDTH - 40), 10, "무기갯수증가아이템.png")
                    weapon_number_items.add(weapon_number_item)
                if a == 3:
                    weapon_power_item = Item(random.randrange(0, WINDOW_WIDTH - 40), 10, "파워아이템.png")
                    weapon_power_items.add(weapon_power_item)
                    weapon_number_item = Item(random.randrange(0, WINDOW_WIDTH - 40), 10, "무기갯수증가아이템.png")
                    weapon_number_items.add(weapon_number_item)
                enemy_level += 1
                rundic[i] = 1

        ##################플레이어가 쏘는 무기와 적들 간의 충돌#######################
        for player1_weapon in player1_weapons:
            enemy1 = player1_weapon.crash(enemy1s)
            enemy2 = player1_weapon.crash(enemy2s)
            if enemy1:
                player1_weapon.kill()
                enemy1.hp -= player1_weapon_power_level
                if enemy1.hp <= 0:
                    enemy1.kill()
                    occur_explosion(screen, enemy1.rect.x, enemy1.rect.y, 40, 40)
                    shot_count += 1
            if enemy2:
                player1_weapon.kill()
                enemy2.hp -= player1_weapon_power_level
                if enemy2.hp <= 0:
                    enemy2.kill()
                    occur_explosion(screen, enemy2.rect.x, enemy2.rect.y, 40, 40)
                    shot_count += 1
                    
        for player2_weapon in player2_weapons:
            enemy1 = player2_weapon.crash(enemy1s)
            enemy2 = player2_weapon.crash(enemy2s)
            if enemy1:
                player2_weapon.kill()
                enemy1.hp -= player2_weapon_power_level
                if enemy1.hp <= 0:
                    enemy1.kill()
                    occur_explosion(screen, enemy1.rect.x, enemy1.rect.y, 40, 40)
                    shot_count += 1
            if enemy2:
                player2_weapon.kill()
                enemy2.hp -= player2_weapon_power_level
                if enemy2.hp <= 0:
                    enemy2.kill()
                    occur_explosion(screen, enemy2.rect.x, enemy2.rect.y, 40, 40)
                    shot_count += 1
                    
        ##################플레이어가 놓친 적들, 적들이 쏘는 무기#######################
        for enemy1 in enemy1s:
            if enemy1.out_of_screen():
                enemy1.kill()
                count_missed += 1
            if enemy_attack_k % 100 == 0:
                enemy1_weapon = Enemy_Weapon(10, 40, enemy1.rect.centerx - 5, enemy1.rect.centery, 5, player1.rect.x + player1.sx/2, player1.rect.y + player1.sy/2, "적1총알.png")
                enemy1_weapons.add(enemy1_weapon)
            
        for enemy2 in enemy2s:
            if enemy2.out_of_screen():
                enemy2.kill()
                count_missed += 1                
            if enemy_attack_k % 100 == 0:
                enemy2_weapon = Enemy_Weapon(10, 40, enemy2.rect.centerx - 5, enemy2.rect.centery, 5, player2.rect.x + player2.sx/2, player1.rect.y + player2.sy/2, "적1총알.png")
                enemy2_weapons.add(enemy2_weapon)
                
        ##################적들이 쏘는 무기가 적중하지 않아 화면 밖으로 나가는 경우#######################
        for enemy1_weapon in enemy1_weapons:
            if enemy1_weapon.out_of_screen():
                enemy1_weapon.kill()
                
        for enemy2_weapon in enemy2_weapons:
            if enemy2_weapon.out_of_screen():
                enemy2_weapon.kill()
                
        ##################적들 공격속도 보정#######################
        enemy_attack_k += 1
        
        ##################적들, 플레이어, 보스, 각종 무기들, 아이템들 업데이트와 그리기#######################
        enemy1s.update(player1.rect.x + player1.sx/2, player1.rect.y + player1.sy/2)
        enemy1s.draw(screen)
        enemy2s.update(player2.rect.x + player2.sx/2, player2.rect.y + player2.sy/2)
        enemy2s.draw(screen)
        
        enemy1_weapons.update(player1.rect.x + player1.sx/2, player1.rect.y + player1.sy/2)
        enemy1_weapons.draw(screen)
        enemy2_weapons.update(player2.rect.x + player2.sx/2, player2.rect.y + player2.sy/2)
        enemy2_weapons.draw(screen)
        
        player1_weapons.update()
        player1_weapons.draw(screen)
        player2_weapons.update()
        player2_weapons.draw(screen)
        
        player1.update()        
        player1.draw(screen)
        player2.update()
        player2.draw(screen)
        
        boss.update()
        boss.draw(screen)
        
        weapon_number_items.update()
        weapon_number_items.draw(screen)
        weapon_speed_items.update()
        weapon_speed_items.draw(screen)
        weapon_power_items.update()
        weapon_power_items.draw(screen)
        heal_items.update()
        heal_items.draw(screen)
        
        pygame.display.flip()
        
        ##################충돌 처리#######################
        if player1.crash(enemy1s) or player1.crash(enemy2s):
            players_hp -= enemy_level
            occur_explosion(screen, player1.rect.x, player1.rect.y, 50, 50)
            pygame.display.update()
            
        if player2.crash(enemy1s) or player2.crash(enemy2s):
            players_hp -= enemy_level
            occur_explosion(screen, player2.rect.x, player2.rect.y, 50, 50)
            pygame.display.update()
            
        if player1.crash(enemy1_weapons) or player1.crash(enemy2_weapons):
            players_hp -= enemy_level
            occur_explosion(screen, player1.rect.x, player1.rect.y, 50, 50)
            pygame.display.update()
            
        if player2.crash(enemy1_weapons) or player2.crash(enemy2_weapons):
            players_hp -= enemy_level
            occur_explosion(screen, player2.rect.x, player2.rect.y, 50, 50)
            pygame.display.update()

        if boss.crash(player1_weapons):
            boss.hp -= player1_weapon_power_level
            occur_explosion(screen, boss.rect.x + 50, boss.rect.y + 100, 400, 300)
            pygame.display.update()
            
        if boss.crash(player2_weapons):
            boss.hp -= player2_weapon_power_level
            occur_explosion(screen, boss.rect.x + 50, boss.rect.y + 100, 400, 300)
            pygame.display.update()

        if player1.crash(weapon_number_items):
            player1_weapon_number_level += 1
            occur_get_item()
            pygame.display.update()
            
        if player2.crash(weapon_number_items):
            player2_weapon_number_level += 1
            occur_get_item()
            pygame.display.update()
            
        if player1.crash(weapon_power_items):
            player1_weapon_power_level += 1
            occur_get_item()
            pygame.display.update()
            
        if player2.crash(weapon_power_items):
            player2_weapon_power_level += 1
            occur_get_item()
            pygame.display.update()
            
        if player1.crash(weapon_speed_items):
            player1_weapon_speed_level += 1
            occur_get_item()
            pygame.display.update()
            
        if player2.crash(weapon_speed_items):
            player2_weapon_speed_level += 1
            occur_get_item()
            pygame.display.update()
            
        if player1.crash(heal_items) or player2.crash(heal_items):
            players_hp += 20
            occur_get_item()
            pygame.display.update()
            
        ##################플레이어 무기 MAX레벨 설정#######################
        if player1_weapon_number_level >= 4:
            player1_weapon_number_level = 4
        if player1_weapon_power_level >= 5:
            player1_weapon_power_level = 5
        if player1_weapon_speed_level >= 5:
            player1_weapon_speed_level = 5
        if player2_weapon_number_level >= 4:
            player2_weapon_number_level = 4
        if player2_weapon_power_level >= 5:
            player2_weapon_power_level = 5
        if player2_weapon_speed_level >= 5:
            player2_weapon_speed_level = 5
            
        ##################충돌한 스프라이트 제거#######################   
        pygame.sprite.spritecollide(player1,enemy1s,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player1,enemy2s,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,enemy1s,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,enemy2s,True,pygame.sprite.collide_mask)
        
        pygame.sprite.spritecollide(player1,enemy1_weapons,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player1,enemy2_weapons,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,enemy1_weapons,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,enemy2_weapons,True,pygame.sprite.collide_mask)
        
        pygame.sprite.spritecollide(boss,player1_weapons,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(boss,player2_weapons,True,pygame.sprite.collide_mask)
        
        pygame.sprite.spritecollide(player1,weapon_power_items,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player1,weapon_number_items,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,weapon_power_items,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,weapon_number_items,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player1,weapon_speed_items,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,weapon_speed_items,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player1,heal_items,True,pygame.sprite.collide_mask)
        pygame.sprite.spritecollide(player2,heal_items,True,pygame.sprite.collide_mask)
        
        ##################게임 종료 조건#######################
        if players_hp <= 0:
            players_hp = 0
            
        if boss.hp <= 0:
            boss.hp = 0

        if players_hp == 0:
            pygame.mixer_music.stop()
            pygame.display.update()
            gameover_sound.play()
            time.sleep(1)
            done = True

        if boss.hp == 0:
            pygame.mixer_music.stop()
            pygame.display.update()
            gameclear_sound.play()
            time.sleep(1)
            done = True            
            
        ##################FPS#######################
        clock.tick(FPS)
        
    return "game_menu"

##############################게임 메뉴 함수#######################################
def game_menu():
    start_image = pygame.image.load(os.path.join(image_path, "배경이미지.png")).convert_alpha()
    start_image = pygame.transform.scale(start_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(start_image, [0,0])
    draw_x = int(WINDOW_WIDTH / 4)
    draw_y = int(WINDOW_HEIGHT / 4)
    font_70 = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 70)
    font_40 = pygame.font.Font("C:/Windows/Fonts/ariblk.ttf", 40)
    
    draw_text("STRIKERS 2022", font_70, screen, draw_x + 250, draw_y, YELLOW)
    draw_text("PRESS ENTER KEY", font_40, screen, draw_x + 150, draw_y + 200, WHITE)
    draw_text("TO START THE GAME.", font_40, screen, draw_x + 150, draw_y + 250, WHITE)
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "play"
        if event.type == pygame.QUIT:
            return "quit"

    return "game_menu"

##############################메인 함수#######################################
def main():
    global screen

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("STRIKERS 2022")
    
    action = "game_menu"
    while action != "quit":
        if action == "game_menu":
            action = game_menu()
        elif action == "play":
            action = game_loop()
            
    pygame.quit()

##################################################
if __name__ == "__main__":
    main()