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

class Player_Role(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.y_vel = 0
        self.is_grounded = False
        self.jump_pressed = False
        self.hp = 200
    
    def update(self, keys_pressed, walls_list):
        if keys_pressed[K_LEFT] and self.rect.x > 3:
            self.rect.x -= self.speed
            for wall in walls_list:
                if self.rect.colliderect(wall.rect):
                    self.rect.left = wall.rect.right
        
        if keys_pressed[K_RIGHT]:
            self.rect.x += self.speed
            for wall in walls_list:
                if self.rect.colliderect(wall.rect):
                    self.rect.right = wall.rect.left
        self.y_vel += 0.8
        if self.y_vel > 12:
            self.y_vel = 12
        self.rect.y += self.y_vel
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
        for wall in walls_list:
            if self.rect.colliderect(wall.rect):
                self.is_grounded = True
        self.rect.y -= 1
        if keys_pressed[K_SPACE] or keys_pressed[K_UP] and not self.jump_pressed:
            self.y_vel = -14
            self.is_grounded = False
        else:
            self.jump_pressed = False
    
    def attack(self, enemy_sprite, keys_pressed):
        if keys_pressed[K_f]:
            if self.rect.colliderect(enemy_sprite.rect):
                enemy_sprite.hp -= 1
                if enemy_sprite.hp < 0:
                    enemy_sprite.hp = 0

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

#create game window
window = display.set_mode((700, 500))
display.set_caption('The Adventure of ALEX')
#background and characters
backgroynd_game = transform.scale(image.load("the_background_of_fight.png"),(700, 500))
title_game = transform.scale(image.load("The_adventure_of_Alex_title.png"),(500, 500))
portal_next_level = transform.scale(image.load("portal_next_level.png"), (120, 135))
player = Player_Role("ALEX_Adventurer.png", 20, 110, 5)
enemy = Enemy_Role("enemy_for_adventures.png", 550, 155, 3)
bullet = Bullet("bullet.png", 40, 7, 2 , -1)
font.init()
style = font.SysFont("Arial", 34)
ui_font = font.SysFont("Arial", 24)
enemy_bullets = []
portal_rect = portal_next_level.get_rect()
portal_rect.x = 590
portal_rect.y = 290
red = 119
green = 218
blue = 219
red_support = 130
blue_support = 57
green_support = 10
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
all_walls_level_2 = [floor, upfloor, Door_wall_level_2, first_wall_level_2]
global levels
levels = 0
#music for background
#mixer.init()
#mixer.music.load("")
#mixer.music.play()
#clock for FPS
clock = time.Clock()
FPS = 60  
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
            
    # level 1 the fist adventure
    if levels == 1:
        keys_pressed = key.get_pressed()
        
        active_walls = []
        for wall in all_walls_level_1:
            if wall == Door_wall and enemy.hp <= 0:
                continue
            active_walls.append(wall)
        
        if player.hp > 0:
            player.reset()
            player.update(keys_pressed, active_walls)
            player.attack(enemy, keys_pressed)
        if enemy.hp > 0:
            enemy.reset()
            enemy.shoot(enemy_bullets)
        
        for bullet in enemy_bullets[:]:
            if enemy.hp <= 0:
                enemy_bullets.clear()
                break
            bullet.update()
            bullet.reset()
        
            if bullet.rect.colliderect(player.rect) and player.hp > 0:
                player.hp -= 30
                enemy_bullets.remove(bullet)
                if player.hp < 0: player.hp = 0
                continue
            
            hit_wall = False
            for wall in active_walls:
                if bullet.rect.colliderect(wall.rect):
                    hit_wall = True
                    break

            if hit_wall:
                enemy_bullets.remove(bullet)
                continue

            if bullet.rect.x < 0 or bullet.rect.x > 700:
                enemy_bullets.remove(bullet)
        
        for wall in active_walls:
            wall.draw_wall()
        
        window.blit(portal_next_level, (portal_rect.x, portal_rect.y))
        if enemy.hp <= 0 and player.rect.colliderect(portal_rect):
            levels = 2
            player.rect.x = 20
            player.rect.y = 110

        player_hp_text = ui_font.render(f"Alex HP: {player.hp}", True, (255, 255, 255))
        enemy_hp_text = ui_font.render(f"Enemy HP: {enemy.hp}", True, (225, 100, 100))
        window.blit(player_hp_text, (20, 20))
        window.blit(enemy_hp_text, (550, 20))
        
        if player.hp <= 0:
            lost_text = style.render("GAME OVER", True, (255, 0, 0))
            window.blit(lost_text, (280, 200))
        
        elif enemy.hp <= 0:
            win_text = style.render("DOOR OPEN! Reach the portal on the right", True, (0, 255, 0))
            window.blit(win_text, (90, 90))
    
    
    if levels == 2:
        keys_pressed = key.get_pressed()
        player.reset()
        player.update(keys_pressed, all_walls_level_2)
        for wall in all_walls_level_2:
            wall.draw_wall()
    
    if levels == 3:
        pass
    
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    
    clock.tick(FPS)
    display.update()