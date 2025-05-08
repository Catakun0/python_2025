import pygame
import random
import os
pygame.init()

clock = pygame.time.Clock()

resolution_x = 800
resolution_y = 600
screen = pygame.display.set_mode((resolution_x, resolution_y))

pygame.display.set_caption("Jumm")
icon = pygame.image.load('resurces/img/ico.png')
pygame.display.set_icon(icon)

main_bg = pygame.image.load('resurces/img/main_bg.png')

# load animations
def load_animation(scale, folder1, folder2, filename_prefix, frame_count=8):
    path = os.path.join("resurces", "animation", folder1, folder2)
    frames = []
    for i in range(1, frame_count + 1):
        frame_path = os.path.join(path, f"{filename_prefix}_{i}.png")
        image = pygame.image.load(frame_path).convert_alpha()
        scaled = pygame.transform.scale(image, (scale, scale))
        frames.append(scaled)
    return frames



# all sound effect
sound_fire = pygame.mixer.Sound('resurces/sound_effect/fire.mp3')
sound_fire.set_volume(0.4)
sound_spaceship = pygame.mixer.Sound('resurces/sound_effect/spaceship.mp3')
volume_for_sound_spaceship = 0.2
save_volume_for_sound_spaceship = volume_for_sound_spaceship
sound_spaceship.set_volume(volume_for_sound_spaceship)
sound_ghost_spawn = pygame.mixer.Sound('resurces/sound_effect/spawn_ghost.mp3')
sound_ghost_spawn.set_volume(0.35)
sound_death = pygame.mixer.Sound('resurces/sound_effect/death_enemy.mp3')
sound_death.set_volume(0.4)
sound_take_dmg = pygame.mixer.Sound('resurces/sound_effect/take_dmg.mp3')
sound_take_dmg.set_volume(0.4)
sound_click_button = pygame.mixer.Sound('resurces/sound_effect/click_button.mp3')
sound_click_button.set_volume(1)
sound_select_button = pygame.mixer.Sound('resurces/sound_effect/select_button.mp3')
sound_select_button.set_volume(1)

# ghost_enemy
enemy_ghost = load_animation(64,"enemy", "walk", "ghost_walk", 6)
max_enemy = 6
all_ghostEnemy = []
save_cooldown_for_spawn_enemy = 3
cooldown_for_spawn_enemy = save_cooldown_for_spawn_enemy

class the_ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.enemy_dmg = random.randint(5, 20)
        self.speed = random.uniform(1, 2)
        self.frames = enemy_ghost
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.2
        self.image = self.frames[0]

    def update(self):
        self.y += self.speed
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self):
        return self.y > resolution_y + 30

    def colision(self):
        global all_bullet
        the_range = 20
        for the_bullet in all_bullet:
            if (self.x - the_range <= the_bullet.x <= self.x + the_range and
                self.y - the_range <= the_bullet.y <= self.y + the_range):
                all_bullet.remove(the_bullet)
                spawn_explosion(self.x, self.y, explosion_1)
                kill_enemy()
                return True
        if (self.x - the_range <= player_x <= self.x + the_range and
                self.y - the_range <= player_y <= self.y + the_range):
            player_get_DMG(self.enemy_dmg)
            return True



# player
the_player = load_animation(150,"player", "idle", "sprite", 6)
player_x = resolution_x / 2 - 50
player_y = resolution_y - 200
save_player_speed = 2
player_speed = save_player_speed
player_x_add = 0
player_x_subtract = 0
save_player_HP = 100
player_HP = save_player_HP
player_score = 0
player_score_necesary = 1
player_boost_speed = 5
player_timer_for_boost = 100
save_timer_for_boost = player_timer_for_boost
displey_timer_for_boost = 100
player_boost_stat = "off"

# bullet
bullet_frames = load_animation(35,"monition", "gun", "bullet_sprite", 6)
scale = 0.7
save_cooldown_for_fire = 0.6
cooldown_for_fire = save_cooldown_for_fire

# main_level
main_level = 1
select_skill_now = False

class the_bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.frames = bullet_frames
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.2
        self.image = self.frames[0]

    def update(self):
        self.y -= self.speed
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self):
        screen.blit(self.image, (self.x + 14, self.y))


    def is_off_screen(self):
        return self.y < -25

# spawn new enemy
def spawn_enemy():
    global player_HP
    if player_HP <= 0:
        return
    global cooldown_for_spawn_enemy, save_cooldown_for_spawn_enemy, main_level
    save_cooldown_for_spawn_enemy = max(1, 3 - main_level * 0.2)
    cooldown_for_spawn_enemy = random.uniform(save_cooldown_for_spawn_enemy * 0.4, save_cooldown_for_spawn_enemy)
    x = random.uniform(50, resolution_x - 50)
    new_enemy = the_ghost(x, -30)
    all_ghostEnemy.append(new_enemy)
    sound_ghost_spawn.play()

# draw spaceship
current_frame = 0
frame_timer = 0
frame_speed = 0.15  
def void_player(x, y):
    global current_frame, frame_timer
    frame_timer += frame_speed
    if frame_timer >= 1:
        frame_timer = 0
        current_frame = (current_frame + 1) % len(the_player)
    screen.blit(the_player[current_frame], (x - 35, y))

# draw bullets
all_bullet = []
def fire_bullet(x, y):
    global player_HP
    if player_HP <= 0:
        return
    global cooldown_for_fire, save_cooldown_for_fire
    cooldown_for_fire = save_cooldown_for_fire
    new_bullet = the_bullet(x, y)
    all_bullet.append(new_bullet)
    sound_fire.play()
       

def kill_enemy():
    global player_score, player_score_necesary
    player_score += 1
    if player_score == player_score_necesary:
        level_up()
    sound_death.play()

def player_get_DMG(the_dmg):
    global player_HP
    if player_HP <= 0:
        return
    player_HP -= the_dmg
    spawn_explosion(player_x + 3, player_y + 20, explosion_2)
    if player_HP <= 0:
        player_death()
        player_HP = 0
    sound_take_dmg.play()

def player_death():
    print("player die")

def level_up():
    global main_level, player_score_necesary, select_skill_now
    main_level += 1
    player_score_necesary += player_score_necesary * 2
    select_skill_now = True

# all particles
explosion_1 = load_animation(70,"particle", "explosion", "explosion", 6)
explosion_2 = load_animation(70,"particle", "explosion_2", "explosion", 6)
all_particle = []
class the_explosion:
    def __init__(self, x, y, select_explosion):
        self.x = x
        self.y = y
        self.frames = select_explosion
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.3
        self.image = self.frames[0]

    def update(self):
        if self.current_frame < len(self.frames) - 1:
            self.frame_timer += self.frame_speed
            if self.frame_timer >= 1:
                self.frame_timer = 0
                self.current_frame += 1
                self.image = self.frames[self.current_frame]
        else:
             all_particle.remove(self)


    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def spawn_explosion(x, y, select_explosion):
    new_explosion = the_explosion(x, y, select_explosion)
    all_particle.append(new_explosion)

# savde_data
saveData_player_x = saveData_player_y = saveData_player_HP = saveData_player_boost = saveData_player_speed = 0
def save_game():
    global saveData_player_x, saveData_player_y, saveData_player_HP, saveData_player_boost, player_y, player_x, player_HP, player_timer_for_boost, saveData_player_speed
    saveData_player_x = player_x
    saveData_player_y = player_y
    saveData_player_HP = player_HP
    saveData_player_boost = player_timer_for_boost
    saveData_player_speed = player_speed

#HUD
main_font = pygame.font.SysFont("Impact", 20)
display_score = main_font.render(f"SCORE: {player_score}", True, (255, 255, 255), (0, 0 ,0))
display_player_HP = main_font.render(f"HP: {player_HP}", True, (255, 0, 0), (0, 0 ,0))
display_level = main_font.render(f"LEVEL: {main_level}", True, (0, 0, 255), (0, 0 ,0))
display_timerBoost = main_font.render(f"BOOST: {displey_timer_for_boost}", True, (255, 255, 255), (0, 0 ,0))
display_timerBoost_rect = display_timerBoost.get_rect()
display_level_rect = display_level.get_rect()
display_score_rect = display_score.get_rect()
display_player_HP_rect = display_player_HP.get_rect()
display_level_rect.center = (resolution_x / 2, 10)
display_score_rect.topleft = (20, 10)
display_player_HP_rect.center = (resolution_x - 40, 10)
display_timerBoost_rect = (resolution_x / 2 - 55, resolution_y - 30)

running = True
pause_game = True

#buttons
default_position_for_buttons = 200
# start_game
startGame_button = pygame.Rect(resolution_x / 2 - 90, default_position_for_buttons, 200, 35)
start_button_text = main_font.render("Start Game", True, (0, 0, 0))
# restart_game
restartGame_button = pygame.Rect(resolution_x / 2 - 90, default_position_for_buttons + 50, 200, 35)
restart_button_text = main_font.render("Restart", True, (0, 0, 0))
# quit_game
quitGame_button = pygame.Rect(resolution_x / 2 - 90, default_position_for_buttons + 100, 200, 35)
quit_button_text = main_font.render("Quit Game", True, (0, 0, 0))
# select_skill
select_skill_button_1 = pygame.Rect(resolution_x - resolution_x * 0.9, default_position_for_buttons + 100, 200, 35)
select_skill_button_text_1 = main_font.render("Speed + 0.1", True, (0, 0, 0))
select_skill_button_2 = pygame.Rect(resolution_x - resolution_x * 0.61, default_position_for_buttons + 100, 200, 35)
select_skill_button_text_2 = main_font.render("Max Bosst + 5", True, (0, 0, 0))
select_skill_button_3 = pygame.Rect(resolution_x - resolution_x * 0.32, default_position_for_buttons + 100, 200, 35)
select_skill_button_text_3 = main_font.render("HP + 10", True, (0, 0, 0))

enter_button1 = enter_button2 = enter_button3 = False
def main_menu():
    global running, pause_game, player_x_add, player_x_subtract, player_speed, save_player_speed, player_boost_stat, enter_button1, enter_button2, enter_button3
    player_x_add = player_x_subtract = 0
    player_speed = save_player_speed
    player_boost_stat = "off"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if startGame_button.collidepoint(event.pos):
                sound_click_button.play()
                pause_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restartGame_button.collidepoint(event.pos):
                sound_click_button.play()
                load_game()
                pause_game = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quitGame_button.collidepoint(event.pos):
                sound_click_button.play()
                pygame.quit()
                exit()
    #all_buttons
    # start_game
    color = (0, 255, 0) if startGame_button.collidepoint(pygame.mouse.get_pos()) \
        else (255, 0, 0)
    pygame.draw.rect(screen, color, startGame_button)
    screen.blit(start_button_text, (startGame_button.x + 55, startGame_button.y + 4)) 
    # restart_game
    color = (0, 255, 0) if restartGame_button.collidepoint(pygame.mouse.get_pos()) \
        else (255, 0, 0)
    pygame.draw.rect(screen, color, restartGame_button)
    screen.blit(restart_button_text, (restartGame_button.x + 70, restartGame_button.y + 4))
    # quit_game
    color = (0, 255, 0) if quitGame_button.collidepoint(pygame.mouse.get_pos()) \
        else (255, 0, 0)
    pygame.draw.rect(screen, color, quitGame_button)
    screen.blit(quit_button_text, (quitGame_button.x + 60, quitGame_button.y + 4))
    #select_buttons (sound_effect)
    # 1
    if startGame_button.collidepoint(pygame.mouse.get_pos()):
        if enter_button1 == False:
            sound_select_button.play()
            enter_button1 = True
    else:
        enter_button1 = False
    # 2
    if restartGame_button.collidepoint(pygame.mouse.get_pos()):
        if enter_button2 == False:
            sound_select_button.play()
            enter_button2 = True
    else:
        enter_button2 = False
    # 3
    if quitGame_button.collidepoint(pygame.mouse.get_pos()):
        if enter_button3 == False:
            sound_select_button.play()
            enter_button3 = True
    else:
        enter_button3 = False

the_scale = 150
img_more_speed = pygame.transform.scale(pygame.image.load('resurces/img/more_speed.png'), (the_scale, the_scale))
img_more_boost = pygame.transform.scale(pygame.image.load('resurces/img/more_boost.png'), (the_scale, the_scale))
img_hp_up = pygame.transform.scale(pygame.image.load('resurces/img/add_hp_up.png'), (the_scale, the_scale))

def select_skill():
    global select_skill_now, running, pause_game, player_x_add, player_x_subtract, player_speed, save_player_speed, \
        player_boost_stat, enter_button1, enter_button2, enter_button3, save_player_speed, player_boost_speed, player_HP, save_timer_for_boost
    player_x_add = player_x_subtract = 0
    player_speed = save_player_speed
    player_boost_stat = "off"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if select_skill_button_1.collidepoint(event.pos):
                sound_click_button.play()
                save_player_speed += 0.1
                player_boost_speed += 0.1
                select_skill_now = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if select_skill_button_2.collidepoint(event.pos):
                sound_click_button.play()
                save_timer_for_boost += 5
                select_skill_now = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if select_skill_button_3.collidepoint(event.pos):
                sound_click_button.play()
                player_HP += 10
                select_skill_now = False
    #all_buttons
    # select 1
    color = (0, 255, 0) if select_skill_button_1.collidepoint(pygame.mouse.get_pos()) \
        else (255, 0, 0)
    pygame.draw.rect(screen, color, select_skill_button_1)
    screen.blit(select_skill_button_text_1, (select_skill_button_1.x + 53, select_skill_button_1.y + 4)) 
    screen.blit(img_more_speed, (select_skill_button_1.x + 25, select_skill_button_1.y - 170))
    # select 2
    color = (0, 255, 0) if select_skill_button_2.collidepoint(pygame.mouse.get_pos()) \
        else (255, 0, 0)
    pygame.draw.rect(screen, color, select_skill_button_2)
    screen.blit(select_skill_button_text_2, (select_skill_button_2.x + 46, select_skill_button_2.y + 4))
    screen.blit(img_more_boost, (select_skill_button_2.x + 25, select_skill_button_2.y - 170))
    # select 3
    color = (0, 255, 0) if select_skill_button_3.collidepoint(pygame.mouse.get_pos()) \
        else (255, 0, 0)
    pygame.draw.rect(screen, color, select_skill_button_3)
    screen.blit(select_skill_button_text_3, (select_skill_button_3.x + 72, select_skill_button_3.y + 4))
    screen.blit(img_hp_up, (select_skill_button_3.x + 25, select_skill_button_3.y - 170))
    #select_buttons (sound_effect)
    # 1
    if select_skill_button_1.collidepoint(pygame.mouse.get_pos()):
        if enter_button1 == False:
            sound_select_button.play()
            enter_button1 = True
    else:
        enter_button1 = False
    # 2
    if select_skill_button_2.collidepoint(pygame.mouse.get_pos()):
        if enter_button2 == False:
            sound_select_button.play()
            enter_button2 = True
    else:
        enter_button2 = False
    # 3
    if select_skill_button_3.collidepoint(pygame.mouse.get_pos()):
        if enter_button3 == False:
            sound_select_button.play()
            enter_button3 = True
    else:
        enter_button3 = False

def load_game():
    global saveData_player_x, saveData_player_y, saveData_player_HP, saveData_player_boost, player_y, player_x, player_HP, player_timer_for_boost, player_x_add, player_x_subtract, player_score, main_level, saveData_player_speed, player_speed, player_boost_stat

    player_x = saveData_player_x
    player_y = saveData_player_y
    player_HP = saveData_player_HP
    player_HP = saveData_player_HP
    player_timer_for_boost = saveData_player_boost
    player_speed = saveData_player_speed
    player_x_subtract = player_x_add = player_score = 0
    main_level = 1
    all_bullet.clear()
    all_ghostEnemy.clear()
    player_boost_stat = "off"

save_game()
load_game()
sound_spaceship.play(loops=-1)
while running:
    dt = clock.tick(60) / 1000.0
    screen.fill((0, 0 ,0))
    screen.blit(main_bg, (0 ,0))    
    if pause_game == False and select_skill_now == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_game = True
                if event.key == pygame.K_a:
                    player_x_subtract = -1
                if event.key == pygame.K_d:
                    player_x_add = 1
                if event.key == pygame.K_LSHIFT:
                    if player_timer_for_boost > 0:
                        player_speed = player_boost_speed
                        player_boost_stat = "on"
                if event.key == pygame.K_SPACE:
                    if cooldown_for_fire <= 0:
                        fire_bullet(player_x + 12.5, player_y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player_x_subtract = 0
                if event.key == pygame.K_d:
                    player_x_add = 0
                if event.key == pygame.K_LSHIFT:
                    if player_boost_stat == "on":
                        player_speed = save_player_speed
                        player_boost_stat = "off"
        #sound_effect
        #player_move
        if save_player_speed != player_speed:
            sound_spaceship.set_volume(save_volume_for_sound_spaceship * 3.5)
        elif save_player_speed == player_speed:
            sound_spaceship.set_volume(save_volume_for_sound_spaceship * 2)
        else:
            sound_spaceship.set_volume(save_volume_for_sound_spaceship)

        #HUD
        #score, hp, level, boost
        screen.blit(display_score, display_score_rect)
        screen.blit(display_player_HP, display_player_HP_rect)
        screen.blit(display_level, display_level_rect)
        screen.blit(display_timerBoost, display_timerBoost_rect)
        display_score = main_font.render(f"SCORE: {player_score}", True, (255, 255, 255), (0, 0 ,0))
        display_player_HP = main_font.render(f"HP: {player_HP}", True, (255, 0, 0), (0, 0 ,0))
        display_level = main_font.render(f"LEVEL: {main_level}", True, (0, 0, 255), (0, 0 ,0))
        display_timerBoost = main_font.render(f"BOOST: {displey_timer_for_boost}", True, (255, 255, 255), (0, 0 ,0))

        #spawn_enemy
        if cooldown_for_spawn_enemy <= 0:
            if len(all_ghostEnemy) <= max_enemy:
                spawn_enemy()
        # enemy_move
        if len(all_ghostEnemy) > 0:
            for i_enemy in all_ghostEnemy[:]:
                i_enemy.update()
                i_enemy.draw()
                if i_enemy.is_off_screen():
                    all_ghostEnemy.remove(i_enemy)
                elif i_enemy.colision():
                    all_ghostEnemy.remove(i_enemy)
            
        #cooldown
        if cooldown_for_fire > 0:
            cooldown_for_fire -= dt
        if cooldown_for_spawn_enemy > 0:
            cooldown_for_spawn_enemy -= dt
        if player_timer_for_boost <= save_timer_for_boost and player_boost_stat == "off":
            player_timer_for_boost += dt * 5
        if player_timer_for_boost > 2 and player_boost_stat == "on" and (player_x_add != 0 or player_x_subtract != 0):
            player_timer_for_boost -= dt * 10
        displey_timer_for_boost = int(player_timer_for_boost)

        # baraj
        if player_x <= 0:
            player_x = 0
        elif player_x >= resolution_x - 70:
            player_x = resolution_x - 70

        # bullet_move
        if len(all_bullet) > 0:
            for i_bullet in all_bullet:
                i_bullet.update()
                i_bullet.draw()
                if i_bullet.is_off_screen():
                    all_bullet.remove(i_bullet)    

        # player_move
        if player_HP > 0:
            player_x += (player_x_add * player_speed) + (player_x_subtract * player_speed)
        void_player(player_x, player_y) 
        #boost_player
        if player_timer_for_boost <= 2:
            player_boost_stat = "off"
            player_speed = save_player_speed
        
        # all particles
        if len(all_particle) > 0:
            for particle in all_particle:
                particle.update()
                particle.draw()

    elif pause_game == True:
        main_menu()
    else:
        select_skill()
    pygame.display.update()
