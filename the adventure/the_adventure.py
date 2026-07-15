# import things
from pygame import *
# sure pygame core
init()
# class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (110, 110))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player class to work
class Player_Role(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        
        # fist image
        self.idle_image = self.image
        self.idle_image_left = transform.flip(self.idle_image, True, False)

        self.attack_frames_right = [
            transform.scale(image.load("ALEX_Animation_1.png"), (110, 110)),
            transform.scale(image.load("ALEX_Animation_2.png"), (110, 110)),
            transform.scale(image.load("ALEX_Animation_3.png"), (110, 110)),
            transform.scale(image.load("ALEX_Animation_4.png"), (150, 110))
        ]
        
        self.attack_frames_left = [transform.flip(frame, True, False) for frame in self.attack_frames_right]

        self.facing_right = True

        self.is_attacking = False
        self.attack_frame_index = 0
        self.attack_timer = 0

        # IMPORTAL FOR USE
        self.y_vel = 0
        self.is_grounded = False
        self.jump_pressed = False
        self.hp = 200
    
    def reset(self):
        if self.facing_right:
            window.blit(self.image, (self.rect.x, self.rect.y))
        else:
            if not self.is_attacking:
                window.blit(self.idle_image_left, (self.rect.x, self.rect.y))
            else:
                window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, keys_pressed, walls_list):
        # PLAYER MOVE LEFT
        if keys_pressed[K_LEFT] and self.rect.x > 3:
            self.rect.x -= self.speed
            self.facing_right = False
            if not self.is_attacking:
                self.image = self.idle_image_left
            for wall in walls_list:
                if self.rect.colliderect(wall.rect):
                    self.rect.left = wall.rect.right
        # PLAYER MOVE RIGHT 
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
            self.facing_right = True
            if not self.is_attacking:
                self.image = self.idle_image
            for wall in walls_list:
                if self.rect.colliderect(wall.rect):
                    self.rect.right = wall.rect.left
        self.y_vel += 0.8
        # GRAVITY
        if self.y_vel > 12:
            self.y_vel = 12
        self.rect.y += self.y_vel
        # WHO WALL REACT IN PLAYER
        for wall in walls_list:
            if self.rect.colliderect(wall.rect):
                if self.y_vel > 0:
                    self.rect.bottom = wall.rect.top
                    self.y_vel = 0
                    self.is_grounded = True
                elif self.y_vel < 0:
                    self.rect.top = wall.rect.bottom
                    self.y_vel = 0
        self.rect.y += 1
        self.is_grounded = False
        # WALLS FOR PLAYER
        for wall in walls_list:
            if self.rect.colliderect(wall.rect):
                self.is_grounded = True
        self.rect.y -= 1
        # JUMP MECHANIC 
        if (keys_pressed[K_SPACE] or keys_pressed[K_UP]) and not self.jump_pressed and self.is_grounded:
            self.y_vel = -20
            self.is_grounded = False
            self.jump_pressed = True
        if not keys_pressed[K_SPACE] and not keys_pressed[K_UP]:
            self.jump_pressed = False
    # ATTACK HOW PLAYER DO DAMAGE IN ENEMYS WITH BUTTON F
    def attack(self, enemies_list, keys_pressed):
        if keys_pressed[K_f] and not self.is_attacking:
            self.is_attacking = True
            self.attack_frame_index = 0
            self.attack_timer = time.get_ticks()
            
            if self.facing_right:
                self.image = self.attack_frames_right[0]
            else:
                self.image = self.attack_frames_left[0]
            
            # Damage On Enemy
            for enemy_sprite in enemies_list:
                if enemy_sprite.hp > 0 and self.rect.colliderect(enemy_sprite.rect):
                    enemy_sprite.hp -= 50
                    if enemy_sprite.hp < 0:
                        enemy_sprite.hp = 0
            
        if self.is_attacking:
            now = time.get_ticks()
            if now - self.attack_timer > 120:
                self.attack_frame_index += 1
                self.attack_timer = now
                
                frames_to_use = self.attack_frames_right if self.facing_right else self.attack_frames_left
                
                if self.attack_frame_index < len(frames_to_use):
                    self.image = frames_to_use[self.attack_frame_index]
                else:
                    self.is_attacking = False
                    self.image = self.idle_image if self.facing_right else self.idle_image_left

# Enemy class to work
class Enemy_Role(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.hp = 300
        self.last_shot = time.get_ticks()
    def shoot(self, bullets_list):
        now = time.get_ticks()
        if now - self.last_shot > 2000:
            new_bullet = Bullet("bullet.png", self.rect.x, self.rect.y + 40, 7, -1)
            bullets_list.append(new_bullet)
            self.last_shot = now

# BULLETS CLASS TO WORK
class Bullet(GameSprite):
    raw_bullet_img = None
    def __init__(self, Bullet_image, x, y, speed, direction):
        super().__init__(Bullet_image, x, y, speed)
        if Bullet.raw_bullet_img is None:
            Bullet.raw_bullet_img = image.load(Bullet_image)
        self.image = transform.scale(Bullet.raw_bullet_img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
    def update(self):
        self.rect.x += self.speed * self.direction
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# WALLS CLASS TO WORK AND DRAW AND COLOR AND WIDTH AND LAST HEIGHT
class walls(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

# defs
# LOADING SCREEN
def SHOW_LOADING_SCREEN(duration_ms = 2000):
    start_time = time.get_ticks()
    loading_run = True
    while loading_run:
        for e in event.get():
            if e.type == QUIT:
                global run
                run = False
                loading_run = False
        elapsed_time = time.get_ticks() - start_time
        progress = (elapsed_time / duration_ms) * 100
        if progress >= 100:
            progress = 100
            loading_run = False
        window.blit(loading_image_game, (0, 0))
        window.blit(Loading_title_game,(1,1))
        percent_text = f"Loading... {int(progress)}%"
        LOADING_SCREEN_text = style.render(percent_text, True, (225, 225, 225))
        window.blit(LOADING_SCREEN_text, (260, 360))
        draw.rect(window, (80, 80, 100), (200, 410, 300, 20))
        bar_width = int((progress / 100) * 300)
        draw.rect(window, (0, 225, 100), (200, 410, bar_width, 20))
        clock.tick(FPS)
        display.update()

def reset_game():
    global enemy_bullets
    player.rect.x, player.rect.y = 20, 110
    player.hp = 200
    player.y_vel = 0
    player.is_attacking = False
    player.image = player.idle_image
    enemy.hp = 300
    Enemy_2.hp = 300
    Enemy_3.hp = 300
    enemy_bullets.clear()


#create game window
window = display.set_mode((700, 500))
display.set_caption('The Adventure of ALEX')
#background and characters
# BACKGROYND, TITLE AND PORTAL 
backgroynd_game = transform.scale(image.load("the_background_of_fight.png"),(700, 500))
title_game = transform.scale(image.load("The_adventure_of_Alex_title.png"),(400, 400))
loading_image_game = transform.scale(image.load("Loading_background.png"),(700, 500))
Loading_title_game = transform.scale(image.load("The_adventure_of_Alex_title.png"),(125, 125))
portal_next_level = transform.scale(image.load("portal_next_level.png"), (120, 135))
# CHARACTERS
player = Player_Role("ALEX_Adventurer.png", 20, 110, 5)
enemy = Enemy_Role("enemy_for_adventures.png", 550, 160, 3)
Enemy_2 = Enemy_Role("enemy_for_adventures.png", 550, 160, 3)
Enemy_3 = Enemy_Role("enemy_for_adventures.png", 400, 310, 3)
# FONT FOR TEXTS
font.init()
style = font.SysFont("Arial", 34)
ui_font = font.SysFont("Arial", 24)
small_font = font.SysFont("Arial", 16)
# ENEMY BULLETS
enemy_bullets = []
# PORTAL
portal_rect = portal_next_level.get_rect()
portal_rect.x = 590
portal_rect.y = 290
# COLOR OF WALLS
red = 119
green = 218
blue = 219
# COLOR FOR BASIC THINGS
red_support = 130
blue_support = 57
green_support = 10
# BASIC THINGS FOR ALL LEVELS
floor = walls(red_support, blue_support, green_support, 0, 430, 700, 1)
upfloor = walls(red_support, blue_support, green_support, 0, 0, 700, 1)
#level 1 walls
Door_wall =  walls(red_support, blue_support, green_support, 320, 290, 30, 140)
first_wall = walls(red, green, blue, 320, 270, 380, 20)
second_wall = walls(red, green, blue, 150, 220, 30, 210)
trio_wall = walls(red, green, blue, 670, 0, 30, 280)
all_walls_level_1 = [floor, upfloor, Door_wall, first_wall, second_wall, trio_wall]
# level two walls
Door_wall_level_2 =  walls(red_support, blue_support, green_support, 520, 290, 30, 140)
first_wall_level_2 = walls(red, green, blue, 520, 270, 380, 20)
second_wall_level_2 = walls(red, green, blue, 670, 0, 30, 280)
trio_wall_level_2 = walls(red, green, blue, 200, 230, 30, 200)
four_wall_level_2 = walls(red, green, blue, 370, 0, 30, 210)
all_walls_level_2 = [floor, upfloor, Door_wall_level_2, first_wall_level_2, second_wall_level_2, trio_wall_level_2, four_wall_level_2]
# GLOBAL THINGS
global levels, Coins, Items
levels = 0
Coins = 0
Items = None
previous_level = 0

play_btn_rect = Rect(250, 240, 200, 50)
friends_btn_rect = Rect(250, 310, 200, 50)
settings_btn_rect = Rect(250, 380, 200, 50)

ingame_settings_rect = Rect(15, 455, 80, 30)
back_btn_rect = Rect(140, 380, 160, 45)
quit_rect = Rect(400, 380, 160, 45)
slider_bg_rect = Rect(170, 280, 360, 20)
sound_toggle_rect = Rect(250, 170, 200, 45)
restart_level_rect = Rect(140, 330, 170, 40)
go_to_menu_rect = Rect(400, 330, 170, 40)
level3_menu_rect = Rect(220, 300, 200, 50)

volume = 0.3
sound_enabled = True
dragging_slider = False

#music for background
mixer.init()
current_track = None
#clock for FPS
clock = time.Clock()
FPS = 60  
SHOW_LOADING_SCREEN(5000)
# game worked but now the name is run
run = True
while run:
    window.blit(backgroynd_game,(0,0))
    mx, my = mouse.get_pos()
    
    active_music_context = levels
    if levels == "settings":
        active_music_context = previous_level
    
    if sound_enabled:
        if active_music_context in [0, "friends", 3]:
            if current_track != "menu_track":
                mixer.music.load("jorisvermeer_epic_adventure.mp3")
                mixer.music.play(-1)
                current_track = "menu_track"
            mixer.music.set_volume(volume)

        elif active_music_context in [1, 2]:
            if current_track != "game_track":
                mixer.music.load("gearfive_epic_adventure.mp3")
                mixer.music.play(-1)
                volume = 0.2
                current_track = "game_track"
            mixer.music.set_volume(volume)
        else:
            if mixer.music.get_busy():
                mixer.music.stop()
                current_track = None
    else:
        if mixer.music.get_busy():
            mixer.music.stop()
            current_track = None
    
    # IMPORTAL THING IS HOW THE GAME CLOSES
    for e in event.get():
        if e.type == QUIT:
            print("QUIT FOR QUIT")
            run = False
    
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            if levels == 0:
                if play_btn_rect.collidepoint((mx, my)):
                    mixer.music.stop()
                    levels = 1
                    print("PLAY")
                    SHOW_LOADING_SCREEN(3000)
                elif friends_btn_rect.collidepoint((mx, my)):
                    print("friends")
                    levels = "friends"
                elif settings_btn_rect.collidepoint((mx, my)):
                    previous_level = 0
                    print("Settings")
                    levels = "settings"
            
            elif levels in [1, 2]:
                if ingame_settings_rect.collidepoint((mx, my)):
                    previous_level = levels
                    levels = "settings"
            
            elif levels == "friends":
                if back_btn_rect.collidepoint((mx, my)):
                    levels = 0 
            
            elif levels == "settings":
                if back_btn_rect.collidepoint((mx, my)):
                    levels = previous_level
                elif sound_toggle_rect.collidepoint((mx, my)):
                    sound_enabled = not sound_enabled
                    if not sound_enabled:
                        mixer.music.stop()
                    else:
                        mixer.music.play(-1)
                        mixer.music.set_volume(volume)
                elif quit_rect.collidepoint((mx, my)):
                    print("QUIT THE GAME FOR SETTINGS")
                    run = False
                elif slider_bg_rect.collidepoint((mx, my)):
                    if sound_enabled:
                        dragging_slider = True
                        mx_clamped = max(slider_bg_rect.x, min(mx, slider_bg_rect.x + slider_bg_rect.width))
                        volume = (mx_clamped - slider_bg_rect.x) / slider_bg_rect.width
                        mixer.music.set_volume(volume)
                elif previous_level in [1, 2] and restart_level_rect.collidepoint((mx, my)):
                    reset_game()
                    levels = previous_level
                    SHOW_LOADING_SCREEN(1500)
                
                elif previous_level in [1, 2] and go_to_menu_rect.collidepoint((mx, my)):
                    reset_game()
                    levels = 0
                    SHOW_LOADING_SCREEN(1500)
            elif levels == 3:
                if level3_menu_rect.collidepoint((mx, my)):
                    reset_game()
                    levels = 0
                    SHOW_LOADING_SCREEN(1500)
        if e.type == MOUSEBUTTONUP and e.button == 1:
            dragging_slider = False
    
    if levels == "settings" and dragging_slider and sound_enabled:
        mx_clamped = max(slider_bg_rect.x, min(mx, slider_bg_rect.x + slider_bg_rect.width))
        volume = (mx_clamped - slider_bg_rect.x) / slider_bg_rect.width
        mixer.music.set_volume(volume)
    #levels and items
    #level 0 the menu
    if levels == 0:
        window.blit(title_game,(140,-100))

        draw.rect(window, (253, 107, 0) if play_btn_rect.collidepoint((mx, my)) else (169, 231, 231), play_btn_rect)
        window.blit(style.render('PLAY', True, (255, 255, 255)), (play_btn_rect.x + 60, play_btn_rect.y + 5))

        draw.rect(window, (253, 107, 0) if friends_btn_rect.collidepoint((mx, my)) else (169, 231, 231), friends_btn_rect)
        window.blit(style.render("1V1 FRIENDS", True, (255, 255, 255)), (friends_btn_rect.x + 15, friends_btn_rect.y + 10))

        draw.rect(window, (253, 107, 0) if settings_btn_rect.collidepoint((mx, my)) else (169, 231, 231), settings_btn_rect)
        window.blit(style.render("SETTINGS", True, (255, 255, 255)), (settings_btn_rect.x + 25, settings_btn_rect.y + 5))
       
    elif levels == "friends":
        panel = Surface((500, 320))
        panel.fill((40, 40, 40))
        window.blit(panel, (100, 90))

        coming_soon_text = style.render("1v1 FRIENDS COMING SOON!", True, (255, 50, 50))
        window.blit(coming_soon_text, (150, 180))

        draw.rect(window, (150, 150, 150) if back_btn_rect.collidepoint((mx, my)) else (100, 100, 100), back_btn_rect)
        window.blit(style.render("BACK", True, (255, 255, 255)), (back_btn_rect.x + 35, back_btn_rect.y + 5))
    
    elif levels == "settings":
        settings_panel = Surface((500, 360))
        settings_panel.fill((40, 40, 40))
        window.blit(settings_panel, (100, 90))
        window.blit(style.render("SETTINGS", True, (255, 255, 255)), (280, 105))

        sound_btn_color = (0, 180, 50) if sound_enabled else (180, 40, 40)
        draw.rect(window, sound_btn_color, sound_toggle_rect)
        sound_status_text = "SOUND: ON" if sound_enabled else "SOUND: OFF"
        window.blit(style.render(sound_status_text, True, (255, 255, 255)), (sound_toggle_rect.x + 15, sound_toggle_rect.y + 5))

        slider_color = (70, 70, 70) if sound_enabled else (50, 50, 50)
        draw.rect(window, slider_color, slider_bg_rect)

        if sound_enabled:
            slider_handle_x = slider_bg_rect.x + int(volume * slider_bg_rect.width)
            draw.rect(window, (200, 50, 50), (slider_handle_x - 10, slider_bg_rect.y - 10, 20, 40))
            vol_text = f"VOLUME OF MUSIC: {int(volume * 100)}%"
        else:
            vol_text = "VOLUME OF MUSIC: MUTED"
        
        window.blit(style.render(vol_text, True, (255, 255, 255) if sound_enabled else (150, 150, 150)), (slider_bg_rect.x + 1, slider_bg_rect.y - 50))

        if previous_level in [1, 2]:
            restart_color = (230, 140, 10) if restart_level_rect.collidepoint((mx, my)) else (180, 110, 10)
            draw.rect(window, restart_color, restart_level_rect)
            window.blit(ui_font.render("RESTART LEVEL", True, (255, 255, 255)), (restart_level_rect.x + 10, restart_level_rect.y + 7))

            menu_btn_color = (130, 40, 180) if go_to_menu_rect.collidepoint((mx, my)) else (90, 30, 130)
            draw.rect(window, menu_btn_color, go_to_menu_rect)
            window.blit(ui_font.render("MAIN MENU", True, (255, 255, 255)), (go_to_menu_rect.x + 30, go_to_menu_rect.y + 7))
        
        draw.rect(window, (150, 150, 150) if back_btn_rect.collidepoint((mx, my)) else (100, 100, 100), back_btn_rect)
        window.blit(style.render("BACK", True, (255, 255, 255)), (back_btn_rect.x + 40, back_btn_rect.y + 5))

        draw.rect(window, (200, 50, 50) if quit_rect.collidepoint((mx, my)) else (100, 100, 100), quit_rect)
        window.blit(style.render("QUIT", True, (255, 255, 255)), (quit_rect.x + 40, quit_rect.y + 5))

    # level 1 the fist adventure
    if levels == 1:
        keys_pressed = key.get_pressed()
        # ACTIVE WALLS AFTER DEFEAT ENEMYS
        active_walls = []
        for wall in all_walls_level_1:
            if wall == Door_wall and enemy.hp <= 0:
                continue
            active_walls.append(wall)
        # PLAYER WORK IN GAME
        if player.hp > 0:
            player.reset()
            player.update(keys_pressed, active_walls)
            player.attack([enemy], keys_pressed)
        # ENEMY WORK IN GAME
        if enemy.hp > 0:
            enemy.reset()
            enemy.shoot(enemy_bullets)
        # BULLETS USE
        for bullet in enemy_bullets[:]:
            if enemy.hp <= 0:
                enemy_bullets.clear()
                break
            bullet.update()
            bullet.reset()
            # DAMAGE PLAYER GET FOR BULLETS
            if bullet.rect.colliderect(player.rect) and player.hp > 0:
                player.hp -= 30
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
                if player.hp < 0: player.hp = 0
                continue
            # HIT WALLS THE BULLETS 
            hit_wall = False
            for wall in active_walls:
                if bullet.rect.colliderect(wall.rect):
                    hit_wall = True
                    break
            # USE HIT WALLS
            if hit_wall:
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
                continue
            # OUT THE WINDOW BULLETS NO NO NO
            if bullet.rect.x < 0 or bullet.rect.x > 700:
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
        # WALLS SHOW
        for wall in active_walls:
            wall.draw_wall()
        # PORTAL SAW
        window.blit(portal_next_level, (portal_rect.x, portal_rect.y))
        # NEXT LEVEL (LEVEL 1 -> LEVEL 2)
        if enemy.hp <= 0 and player.rect.colliderect(portal_rect):
            levels = 2
            enemy_bullets.clear()
            player.rect.x = 20
            player.rect.y = 110
            player.hp = 200
            SHOW_LOADING_SCREEN(3000)
            
        # HP HEALTH BARS
        player_hp_text = ui_font.render(f"Alex HP: {player.hp}", True, (255, 255, 255))
        enemy_hp_text = ui_font.render(f"Enemy HP: {enemy.hp}", True, (225, 100, 100))
        items_text = ui_font.render(f"ITEMS: {Items}", True, (155, 132, 255))
        Coin_text = ui_font.render(f"COIN: {Coins}", True, (255, 255, 30))
        window.blit(player_hp_text, (20, 20))
        window.blit(enemy_hp_text, (530, 20))
        window.blit(items_text, (100, 450))
        window.blit(Coin_text, (100, 470))
        
        btn_color = (253, 107, 0) if ingame_settings_rect.collidepoint((mx, my)) else (100, 100, 100)
        draw.rect(window, btn_color, ingame_settings_rect)
        window.blit(small_font.render("SETTINGS", True, (255, 255, 255)), (ingame_settings_rect.x + 8, ingame_settings_rect.y + 5))
        
        # LOSE TEXT 
        if player.hp <= 0:
            lost_text = style.render("GAME OVER", True, (255, 0, 0))
            window.blit(lost_text, (280, 200))
            enemy_bullets.clear()
        # DOOR OPEN AND SMALL WIN TEXT
        elif enemy.hp <= 0:
            win_text = style.render("DOOR OPEN! Reach the portal on the right", True, (0, 255, 0))
            window.blit(win_text, (90, 90))
    
    # LEVEL 2 THE SECOND ADVENTURE
    if levels == 2:
        keys_pressed = key.get_pressed()
        # ACTIVE WALLS FOR LEVEL 2 
        active_walls_2 = []
        for wall in all_walls_level_2:
            if wall == Door_wall_level_2 and Enemy_2.hp <= 0 and Enemy_3.hp <= 0:
                continue
            active_walls_2.append(wall)
        # PLAYER WORK IN THIS LEVEL
        if player.hp > 0:
            player.reset()
            player.update(keys_pressed, active_walls_2)
            player.attack([Enemy_2, Enemy_3], keys_pressed)
        # FIST ENEMY IN LEVEL 2 WORK
        if Enemy_2.hp > 0:
            Enemy_2.reset()
            Enemy_2.shoot(enemy_bullets)
        # SECOND ENEMY IN LEVEL 2 WORK
        if Enemy_3.hp > 0:
            Enemy_3.reset()
            Enemy_3.shoot(enemy_bullets)
        # PORTAL SAW IN LEVEL 2
        window.blit(portal_next_level, (portal_rect.x, portal_rect.y))
        # BULLETS WHEN ENEMYS LOSE
        for bullet in enemy_bullets[:]:
            if Enemy_2.hp <= 0 and Enemy_3.hp <= 0:
                enemy_bullets.clear()
                break
            bullet.update()
            bullet.reset()
            # DAMAGE FOR BULLETS TO PLAYER
            if bullet.rect.colliderect(player.rect) and player.hp > 0:
                player.hp -= 30
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
                if player.hp < 0: player.hp = 0
                continue
            # HIT WALL 
            hit_wall_2 = False
            for wall in active_walls_2:
                if bullet.rect.colliderect(wall.rect):
                    hit_wall_2 = True
                    break
            # WORK HIT WALL
            if hit_wall_2:
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
                continue
            # BULLET OUT THE WINDOW DELETE
            if bullet.rect.x < 0 or bullet.rect.x > 700:
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
        # DRAW WALLS
        for wall in active_walls_2:
            wall.draw_wall()
        # LEVEL 3 (LEVEL 2 -> LEVEL 3)
        if Enemy_2.hp <= 0 and Enemy_3.hp <= 0 and player.rect.colliderect(portal_rect):
            levels = 3
            enemy_bullets.clear()
            player.rect.x = 20
            player.rect.y = 110
            SHOW_LOADING_SCREEN(2000)
        # HP BARS FOR PLAYER AND ENEMYS
        player_hp_text = ui_font.render(f"Alex HP: {player.hp}", True, (255, 255, 255))
        enemy_2_hp_text = ui_font.render(f"Enemy1 HP: {Enemy_2.hp}", True, (225, 100, 100))
        enemy_3_hp_text = ui_font.render(f"Enemy2 HP: {Enemy_3.hp}", True, (225, 100, 100))
        items_text = ui_font.render(f"ITEMS: {Items}", True, (155, 132, 255))
        Coin_text = ui_font.render(f"COIN: {Coins}", True, (255, 255, 30))
        window.blit(player_hp_text, (20, 20))
        window.blit(enemy_2_hp_text, (520, 20))
        window.blit(enemy_3_hp_text, (520, 50))
        window.blit(items_text, (100, 450))
        window.blit(Coin_text, (100, 470))
        
        btn_color = (253, 107, 0) if ingame_settings_rect.collidepoint((mx, my)) else (100, 100, 100)
        draw.rect(window, btn_color, ingame_settings_rect)
        window.blit(small_font.render("SETTINGS", True, (255, 255, 255)), (ingame_settings_rect.x + 8, ingame_settings_rect.y + 5))
        
        # LOSE FOR PLAYER 
        if player.hp <= 0:
            lost_text = style.render("GAME OVER", True, (255, 0, 0))
            window.blit(lost_text, (280, 200))
            enemy_bullets.clear()
        # DOOR OPEN AND A SMALL WIN
        elif Enemy_2.hp <= 0 and Enemy_3.hp <= 0:
            win_text = style.render("DOOR OPEN! Reach the portal on the right", True, (0, 255, 0))
            window.blit(win_text, (90, 90))
    
    # LEVEL 3, TRIO ADVENTURE OF ALEX
    if levels == 3:
        window.fill((20, 20, 40))
        end_text = style.render("LEVEL 3 COMING SOON!", True, (225, 225, 225))
        window.blit(end_text, (180, 220))

        menu_btn_color_3 = (253, 107, 0) if level3_menu_rect.collidepoint((mx, my)) else (100, 100, 100)
        draw.rect(window, menu_btn_color_3, level3_menu_rect)
        window.blit(style.render("MAIN MENU", True, (255, 255, 255)), (level3_menu_rect.x + 20, level3_menu_rect.y + 5))
    
    # THE WINDOW STAY UPDATE!!!!
    clock.tick(FPS)
    display.update()
quit() 
