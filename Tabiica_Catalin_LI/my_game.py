import pygame
import random
import os
pygame.init()

clock = pygame.time.Clock()

resolution_x = 1200
resolution_y = 600
screen = pygame.display.set_mode((resolution_x, resolution_y))

pygame.display.set_caption("Jumps")
icon = pygame.image.load('resources/img/ico.png')
pygame.display.set_icon(icon)

main_bg = pygame.image.load('resources/img/bg_2.png')
main_ground = pygame.image.load('resources/img/ground_2.png')

# all sound effect
main_music_bg = pygame.mixer.Sound('resources/sound_effect/main_music_1.mp3')
main_music_bg.set_volume(0.3)
sound_click_button = pygame.mixer.Sound('resources/sound_effect/click_button.mp3')
sound_click_button.set_volume(1)
sound_bat_spawn = pygame.mixer.Sound('resources/sound_effect/spawn_ghost.mp3')
sound_bat_spawn.set_volume(0.2)
sound_death = pygame.mixer.Sound('resources/sound_effect/death_enemy.mp3')
sound_death.set_volume(0.4)
sound_take_dmg = pygame.mixer.Sound('resources/sound_effect/player_take_dmg.mp3')
sound_take_dmg.set_volume(0.4)
sound_player_attack = pygame.mixer.Sound('resources/sound_effect/player_attack.mp3')
sound_player_attack.set_volume(0.25)
sound_player_jump = pygame.mixer.Sound('resources/sound_effect/player_jump.mp3')
sound_player_jump.set_volume(0.2)

#player
scale_of_player = 120
def load_player_animation(action_folder_0, action_folder, filename_prefix, frame_count = 8):
    global scale_of_player
    path = os.path.join("resources", action_folder_0, action_folder)
    frames = [
        pygame.transform.scale(pygame.image.load(os.path.join(path, f"{filename_prefix}_{i}.png")).convert_alpha(),(scale_of_player, scale_of_player))
        for i in range(1, frame_count + 1)
    ]
    return frames

class Game:
    def __init__(self):
        self.player_walk_frames = load_player_animation("player", "walk", "sprite")
        self.player_jump_frames = load_player_animation("player", "jump", "jump_sprite")
        self.player_attack_frames = load_player_animation("player", "attack", "attack_sprite")
        self.player_death_frames = load_player_animation("player", "death", "death_sprite")
        self.current_frame_walk = 0
        self.current_frame_jump = 0
        self.current_frame_attack = 0
        self.current_frame_death = 0
        self.frame_timer = 0
        self.frame_speed = 0.2
        self.save_frame_speed = frame_speed
        self.player_pos = [100, resolution_y - 200]
        # player controller
        self.player_x_add = 0
        self.player_x_subtract = 0
        self.player_speed = 3
        self.save_player_speed = player_speed
        self.cooldown_for_jump = 0
        self.save_cooldown_for_jump = 0.3
        self.force_jump = 10 * -1
        self.is_jump = False
        # player attack
        is_attack = False
        cooldown_for_attack = 0.5
        save_cooldown_for_attack = cooldown_for_attack
        # player stats
        player_hp = 100
        player_score = 0
        player_death = False

game = Game()
def player_take_dmg(the_dmg):
    global player_hp
    player_hp -= the_dmg
    sound_take_dmg.play()
def add_score(the_score):
    global player_score
    player_score += the_score

# enemy
all_enemy = []
enemy_walk_frames = load_player_animation("enemy","walk", "bat_sprite", 3)
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_frame_enemy = 0
        self.enemy_frame_speed = 0.15
        self.enemy_frame_timer = 0
        self.enemy_dmg = random.randint(5, 20)
        self.speed = random.uniform(1, 2)

    def update(self):
        self.x -= self.speed

    def draw(self):
        self.enemy_frame_timer += self.enemy_frame_speed
        if self.enemy_frame_timer >= 1:
            self.enemy_frame_timer = 0
            self.current_frame_enemy = (self.current_frame_enemy + 1) % len(enemy_walk_frames)
        screen.blit(enemy_walk_frames[self.current_frame_enemy], (self.x, self.y))

    def is_off_screen(self):
        global all_enemy
        if self.x < -50:
            all_enemy.remove(self)

    def colision(self):
        global player_pos
        the_range = 40
        if (self.x - the_range <= player_pos[0] <= self.x + the_range and
                self.y - the_range <= player_pos[1] <= self.y + the_range):
                player_take_dmg(self.enemy_dmg)
                self.enemy_death()
        the_range = 60
        global is_attack
        if is_attack:
            if (self.x - the_range <= player_pos[0] <= self.x + the_range and
                self.y - the_range <= player_pos[1] <= self.y + the_range):
                generate_explosion(self.x, self.y)
                add_score(self.enemy_dmg)
                all_enemy.remove(self)
                sound_death.play()
        
    def enemy_death(self):
        global all_enemy, player_pos
        generate_explosion(player_pos[0], player_pos[1])
        all_enemy.remove(self)
        sound_death.play()

cooldown_spawn_enemy = 3
save_cooldown_spawn_enemy = cooldown_spawn_enemy
def generate_enemy():
    new_enemy = Enemy(resolution_x, random.uniform(resolution_y - 300, resolution_y - 150))
    all_enemy.append(new_enemy)
    sound_bat_spawn.play()

# particle system
explosion_frames = load_player_animation("particle","explosion", "explosion_sprite", 3)
all_particle = []

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.current_frame_enemy = 0
        self.enemy_frame_speed = 0.1
        self.enemy_frame_timer = 0

    def draw(self):
        if self.current_frame_enemy < len(explosion_frames):
            screen.blit(explosion_frames[self.current_frame_enemy], (self.x, self.y))
            self.enemy_frame_timer += self.enemy_frame_speed
            if self.enemy_frame_timer >= 1:
                self.enemy_frame_timer = 0
                self.current_frame_enemy += 1
        else:
            if self in all_particle:
                all_particle.remove(self)


def generate_explosion(x, y):
    new_explosion = Explosion(x, y)
    all_particle.append(new_explosion)

#HUD
main_font = pygame.font.SysFont("Impact", 20)
display_score = main_font.render(f"SCORE: {player_score}", True, (255, 255, 255), (0, 0 ,0))
display_player_HP = main_font.render(f"HP: {player_hp}", True, (255, 0, 0), (0, 0 ,0))
display_score_rect = display_score.get_rect()
display_player_HP_rect = display_player_HP.get_rect()
display_score_rect.topleft = (20, 10)
display_player_HP_rect.center = (resolution_x - 40, 20)
display_timerBoost_rect = (resolution_x / 2 - 55, resolution_y - 30)

#buttons
default_position_for_buttons = 200
# start_game
startGame_button = pygame.Rect(resolution_x / 2 - 90, default_position_for_buttons, 200, 35)
start_button_text = main_font.render("Start Game", True, (0, 0, 0))
# quit_game
quitGame_button = pygame.Rect(resolution_x / 2 - 90, default_position_for_buttons + 50, 200, 35)
quit_button_text = main_font.render("Quit Game", True, (0, 0, 0))

pause_game = False
running = True
def main_menu():
    global pause_game, running, player_x_add
    player_x_add = 0
    if pause_game == True:
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
        # quit_game
        color = (0, 255, 0) if quitGame_button.collidepoint(pygame.mouse.get_pos()) \
            else (255, 0, 0)
        pygame.draw.rect(screen, color, quitGame_button)
        screen.blit(quit_button_text, (quitGame_button.x + 60, quitGame_button.y + 4))

def game_loop():
    global game
    main_music_bg.play(loops=-1)
    while running:
        dt = clock.tick(60) / 1000.0
        if player_hp <= 0:
            game.player_death = True
        if cooldown_spawn_enemy < 0:
            cooldown_spawn_enemy = random.uniform(save_cooldown_spawn_enemy * 0.6, save_cooldown_spawn_enemy)
            generate_enemy()
        else:
            cooldown_spawn_enemy -= dt
        screen.fill((0, 0 ,0))
        screen.blit(main_bg, (-100 ,-420))    
        if pause_game == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_game = True
                    if event.key == pygame.K_d:
                        player_x_add = 1
                    if event.key == pygame.K_a:
                        player_x_subtract = -1
                    if event.key == pygame.K_e:
                        if is_attack == False and player_death == False:
                            is_attack = True
                            cooldown_for_attack = save_cooldown_for_attack
                            sound_player_attack.play()
                    if event.key == pygame.K_SPACE:
                        if is_jump == False and is_attack == False and player_death == False:
                            cooldown_for_jump = save_cooldown_for_jump
                            is_jump = True
                            sound_player_jump.play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        player_x_add = 0
                    if event.key == pygame.K_a:
                        player_x_subtract = 0

            # animation_player  
            frame_timer += frame_speed if (is_jump == False or is_attack) else frame_speed * 0.6
            if frame_timer >= 1:
                if player_death == False:
                    frame_timer = 0
                    if is_jump == False and is_attack == False:
                        current_frame_jump = 0
                        current_frame_attack = 0
                        current_frame_walk = (current_frame_walk + 1) % len(player_walk_frames)
                    elif is_attack == False:
                        current_frame_attack = 0
                        if current_frame_jump < 7:
                            current_frame_jump += 1
                    else: 
                        current_frame_jump = 0
                        if current_frame_attack < 7:
                            current_frame_attack += 1
                        else:
                            is_attack = False
                else:
                    frame_timer = 0
                    if current_frame_death < 7:
                        current_frame_death += 1
                
            # move_player    
            if player_death == False:
                player_pos[0] += (player_x_add + player_x_subtract) * player_speed * dt if is_attack == False or is_jump else 0
            if player_pos[0] < 50:
                player_pos[0] = 50
            if player_pos[0] > resolution_x - 100:
                player_pos[0] = resolution_x - 100
            if player_death == False:
                if is_jump == False and is_attack == False:
                    screen.blit(player_walk_frames[current_frame_walk], player_pos)
                elif is_attack == False:
                    screen.blit(player_jump_frames[current_frame_jump], player_pos)
                else:
                    screen.blit(player_attack_frames[current_frame_attack], player_pos)
            else:
                screen.blit(player_death_frames[current_frame_death], player_pos)
            if (player_x_add == 0 and player_x_subtract != 0) or (player_x_subtract == 0 and player_x_add != 0):
                frame_speed = save_frame_speed + 0.1
            else:
                frame_speed = save_frame_speed
            # jump_player
            if is_jump:
                player_speed = save_player_speed * 0.6
            else:
                player_speed = save_player_speed
            if cooldown_for_jump > 0:
                cooldown_for_jump -= dt
                player_pos[1] += force_jump
            elif player_pos[1] <= resolution_y - 200:
                player_pos[1] -= force_jump * 0.4
            else:
                is_jump = False
            # enemy
            if len(all_enemy) > 0:
                for enemy in all_enemy:
                    enemy.update()
                    enemy.draw()
                    enemy.colision()
                    enemy.is_off_screen()
            # particle effect
            if len(all_particle) > 0:
                for particle in all_particle:
                    particle.draw()
            
            #HUD
            #score, hp, level, boost
            screen.blit(display_score, display_score_rect)
            screen.blit(display_player_HP, display_player_HP_rect)
            display_score = main_font.render(f"SCORE: {player_score}", True, (255, 255, 255), (0, 0 ,0))
            display_player_HP = main_font.render(f"HP: {player_hp}", True, (255, 0, 0), (0, 0 ,0))
            
        else:
            main_menu()
        pygame.display.update()


game()