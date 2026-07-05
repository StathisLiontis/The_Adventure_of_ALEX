# import things
from pygame import *
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
        # IMPORTAL FOR USE
        self.y_vel = 0
        self.is_grounded = False
        self.jump_pressed = False
        self.hp = 200
    
    def update(self, keys_pressed, walls_list):
        # PLAYER MOVE LEFT
        if keys_pressed[K_LEFT] and self.rect.x > 3:
            self.rect.x -= self.speed
            for wall in walls_list:
                if self.rect.colliderect(wall.rect):
                    self.rect.left = wall.rect.right
        # PLAYER MOVE RIGHT 
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
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
        # JUMP MECHANIC ???
        if keys_pressed[K_SPACE] or keys_pressed[K_UP] and not self.jump_pressed:
            self.y_vel = -14
            self.is_grounded = False
            self.jump_pressed = True
        if not keys_pressed[K_SPACE] and not keys_pressed[K_UP]:
            self.jump_pressed = False
    # ATTACK HOW PLAYER DO DAMAGE IN ENEMYS WITH BUTTON F
    def attack(self, enemy_sprite, keys_pressed):
        if keys_pressed[K_f]:
            if self.rect.colliderect(enemy_sprite.rect):
                enemy_sprite.hp -= 1
                if enemy_sprite.hp < 0:
                    enemy_sprite.hp = 0

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
    def __init__(self, Bullet_image, x, y, speed, direction):
        super().__init__(Bullet_image, x, y, speed)
        self.image = transform.scale(image.load(Bullet_image), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction
    def update(self):
        self.rect.x += self.speed * self.direction

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
        window.fill((20, 20, 40))
        window.blit(title_game,(90,-85))
        percent_text = f"Loading... {int(progress)}%"
        LOADING_SCREEN_text = style.render(percent_text, True, (225, 225, 225))
        window.blit(LOADING_SCREEN_text, (260, 360))
        draw.rect(window, (80, 80, 100), (200, 410, 300, 20))
        bar_width = int((progress / 100) * 300)
        draw.rect(window, (0, 225, 100), (200, 410, bar_width, 20))
        clock.tick(FPS)
        display.update()

#create game window
window = display.set_mode((700, 500))
display.set_caption('The Adventure of ALEX')
#background and characters
# BACKGROYND, TITLE AND PORTAL 
backgroynd_game = transform.scale(image.load("the_background_of_fight.png"),(700, 500))
title_game = transform.scale(image.load("The_adventure_of_Alex_title.png"),(500, 500))
portal_next_level = transform.scale(image.load("portal_next_level.png"), (120, 135))
# CHARACTERS
player = Player_Role("ALEX_Adventurer.png", 20, 110, 5)
enemy = Enemy_Role("enemy_for_adventures.png", 550, 160, 3)
Enemy_2 = Enemy_Role("enemy_for_adventures.png", 550, 160, 3)
Enemy_3 = Enemy_Role("enemy_for_adventures.png", 400, 310, 3)
bullet = Bullet("bullet.png", 40, 7, 2 , -1)
# FONT FOR TEXTS
font.init()
style = font.SysFont("Arial", 34)
ui_font = font.SysFont("Arial", 24)
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
second_wall = walls(red, green, blue, 150, 150, 30, 280)
trio_wall = walls(red, green, blue, 670, 0, 30, 280)
all_walls_level_1 = [floor, upfloor, Door_wall, first_wall, second_wall, trio_wall]
# level two walls
Door_wall_level_2 =  walls(red_support, blue_support, green_support, 520, 290, 30, 140)
first_wall_level_2 = walls(red, green, blue, 520, 270, 380, 20)
second_wall_level_2 = walls(red, green, blue, 670, 0, 30, 280)
all_walls_level_2 = [floor, upfloor, Door_wall_level_2, first_wall_level_2, second_wall_level_2]
# GLOBAL THINGS
global levels
levels = 0
#music for background
#mixer.init()
#mixer.music.load("")
#mixer.music.play()
#clock for FPS
clock = time.Clock()
FPS = 60  
SHOW_LOADING_SCREEN(5000)
# game worked but now the name is run
run = True
while run:
    window.blit(backgroynd_game,(0,0))
    #levels and items
    #level 0 the menu
    if levels == 0:
        window.blit(title_game,(90,-85))
        keys_pressed = key.get_pressed()
        start_text = style.render('Press S to Start', True, (255, 255, 70))
        window.blit(start_text, (250, 345))
        if keys_pressed[K_s]:
            levels = 1
            SHOW_LOADING_SCREEN(3000)
            
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
            player.attack(enemy, keys_pressed)
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
                enemy_bullets.remove(bullet)
                continue
            # OUT THE WINDOW BULLETS NO NO NO
            if bullet.rect.x < 0 or bullet.rect.x > 700:
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
        window.blit(player_hp_text, (20, 20))
        window.blit(enemy_hp_text, (550, 20))
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
            player.attack(Enemy_2, keys_pressed)
            player.attack(Enemy_3, keys_pressed)
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
                enemy_bullets.remove(bullet)
                continue
            # BULLET OUT THE WINDOW DELETE
            if bullet.rect.x < 0 or bullet.rect.x > 700:
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
        window.blit(player_hp_text, (20, 20))
        window.blit(enemy_2_hp_text, (550, 20))
        window.blit(enemy_3_hp_text, (550, 50))
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
    
    # IMPORTAL THING IS HOW THE GAME CLOSES
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    # THE WINDOW STAY UPDATE!!!!
    clock.tick(FPS)
    display.update() 
