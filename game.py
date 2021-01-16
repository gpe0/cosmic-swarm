import pygame
import random
import math
from constants import *
from time import time



def place_block(termite_pos, blocks):
    blocks.append((int(termite_pos[0]) + 20, int(termite_pos[1]) + 68))


def collision_termites(p1, r1, p2, r2):
    d1 = ((p1[0]) - (p2[0] + 20))**2 + ((p1[1]) - (p2[1] + 20))**2
    d2 = ((p1[0]) - (p2[0] + 20))**2 + ((p1[1]) - (p2[1] + 60))**2
    return (d1 < (r1 + r2)**2) or (d2 < (r1 + r2)**2)

def collision_blocks(p1, r1, p2, r2):
    d = ((p1[0]) - (p2[0] + 6))**2 + ((p1[1]) - (p2[1] + 6))**2
    return (d < (r1 + r2)**2)

def collision_bullets_blocks(p1, r1, p2, r2):
    d = ((p1[0]) - (p2[0] + 6))**2 + ((p1[1]) - (p2[1] + 6))**2
    return (d < (r1 + r2)**2)

def collision_bullets(p1, r1, p2, r2, moving, energized):
    d1 = ((p1[0] + 1) - (p2[0] + 20))**2 + ((p1[1] + 1) - (p2[1] + 20))**2
    d2 = ((p1[0] + 1) - (p2[0] + 20))**2 + ((p1[1] + 1) - (p2[1] + 60))**2
    d1_e = ((p1[0] + 1) - (p2[0] + 5))**2 + ((p1[1] + 1) - (p2[1] + 85))**2
    d2_e = ((p1[0] + 1) - (p2[0] + 15))**2 + ((p1[1] + 1) - (p2[1] + 85))**2
    d3_e = ((p1[0] + 1) - (p2[0] + 25))**2 + ((p1[1] + 1) - (p2[1] + 85))**2
    d4_e = ((p1[0] + 1) - (p2[0] + 35))**2 + ((p1[1] + 1) - (p2[1] + 85))**2
    if not moving:
        pass
    else:
        if (d1 < (r1 + r2)**2) or (d2 < (r1 + r2)**2):
            if d1_e < (r1 + 5) ** 2 or d2_e < (r1 + 5) ** 2 or d3_e < (r1 + 5) ** 2 or d4_e < (r1 + 5) ** 2:
                energized = True
    return ((d1 < (r1 + r2)**2) or (d2 < (r1 + r2)**2), energized)

def shoot_sound():
    pygame.mixer.music.load("sounds/shoot.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

def explosion_sound():
    pygame.mixer.music.load("sounds/explosion.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

def block_en_sound():
    pygame.mixer.music.load("sounds/block_col_en.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

def block_sound():
    pygame.mixer.music.load("sounds/block_col.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()

def explosion_ship_sound():
    pygame.mixer.music.load("sounds/explosion_ship.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()


def game(screen, font, gamemode=0):
    global SC_WIDTH
    global SC_HEIGHT
    debug_speed = False
    left_mov = False
    right_mov = False
    up_mov = False
    down_mov = False
    rot_left = False
    rot_right = False
    spawn_ter = False
    shooting = False
    v_x = 0
    v_y = 0
    vel = 0.35 # velocidade x e y
    ang_vel = 0.2 # velocidade de rotação
    bul_sp = 0.5 # velocidade da bala
    b_pos_x = []
    b_pos_y = []
    increment = []
    shoot_cool = 1000 # Cooldown para disparar
    time_shoot = 0
    r_b = 6
    energized = False
    en_time = 0
    en_cool = 3000
    game_time = 15000 if gamemode == 0 else 10000
    score = 0
    lives = 3
    ang = 0
    r = 10
    respawn = False
    res_cool = 2000
    res_time = 0
    die_time = 0
    tick = 200
    c = 0
    change = False
    fuel_tot = 0
    fuel_inc = 0.0005 if gamemode == 0 else 0.001
    fuel_regen = 5
    t_spawn = 4000 if gamemode == 0 else 1500
    minutes = 0
    seconds = 0
    offset = pygame.time.get_ticks()
    time = offset # inicio do jogo
    
    #Coordenadas iniciais das térmitas
    t_pos_x = []
    t_pos_y = []
    
    t_vel = 0.15 if gamemode == 0 else 0.2
    spawn_c = 0 # contador de térmitas
    t_color_in = []
    t_color_out = []
    leave_pos = [] # Parede de saída da térmita
    place_pos = []
    leaving = []
    moving = []
    r_t = 20
    blocks = []
    ship = pygame.image.load('images/ship.png')
    life = pygame.image.load('images/life.png')
    
    bullet = pygame.image.load('images/bullet.png')
    ter1_in = [pygame.image.load('images/termite_purple_block.png'), pygame.image.load('images/termite_purple_block_2.png'), pygame.image.load('images/termite_purple_block.png'), pygame.image.load('images/termite_purple_block_3.png')]
    ter2_in = [pygame.image.load('images/termite_red_block.png'), pygame.image.load('images/termite_red_block_2.png'), pygame.image.load('images/termite_red_block.png'), pygame.image.load('images/termite_red_block_3.png')]
    ter3_in = [pygame.image.load('images/termite_green_block.png'), pygame.image.load('images/termite_green_block_2.png'), pygame.image.load('images/termite_green_block.png'), pygame.image.load('images/termite_green_block_3.png')]
    ter1_out = [pygame.image.load('images/termite_purple.png'), pygame.image.load('images/termite_purple_2.png'), pygame.image.load('images/termite_purple.png'), pygame.image.load('images/termite_purple_3.png')]
    ter2_out = [pygame.image.load('images/termite_red.png'), pygame.image.load('images/termite_red_2.png'), pygame.image.load('images/termite_red.png'), pygame.image.load('images/termite_red_3.png')]
    ter3_out = [pygame.image.load('images/termite_green.png'), pygame.image.load('images/termite_green_2.png'), pygame.image.load('images/termite_green.png'), pygame.image.load('images/termite_green_3.png')]
    block = pygame.image.load('images/square.png')
    block_en = pygame.image.load('images/square_energized.png')
    colors_in = [ter1_in, ter2_in, ter3_in]
    colors_out = [ter1_out, ter2_out, ter3_out]
    t_purple_death = [pygame.image.load('images/termite_purple_dead_1.png'), pygame.image.load('images/termite_purple_dead_2.png'), pygame.image.load('images/termite_purple_dead_3.png')]
    t_red_death = [pygame.image.load('images/termite_red_dead_1.png'), pygame.image.load('images/termite_red_dead_2.png'), pygame.image.load('images/termite_red_dead_3.png')]
    t_green_death = [pygame.image.load('images/termite_green_dead_1.png'), pygame.image.load('images/termite_green_dead_2.png'), pygame.image.load('images/termite_green_dead_3.png')]
    t_d_pos = []
    t_d_color = []
    pos_d_ani = []
    c_d_ani = []
    t_animation_pos = []
    c_in = []
    c_out = []
    clock = pygame.time.Clock()
    
    #Coordenadas e angulo inicial da nave
    pos_x = SC_WIDTH/2 - ship.get_width() / 2
    pos_y = SC_HEIGHT/2 - ship.get_height() / 2
    cp = ship

    
    running = True
    while running:
        #eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    left_mov = True
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    right_mov = True
                elif ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    up_mov = True
                elif ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    down_mov = True  
                elif ev.key == pygame.K_q:
                    rot_left = True  
                elif ev.key == pygame.K_e:
                    rot_right = True  
                elif ev.key == pygame.K_p:
                    debug_speed = not debug_speed
                elif ev.key == pygame.K_SPACE:
                    shooting = True
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_a or ev.key == pygame.K_LEFT:
                    left_mov = False
                elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT:
                    right_mov = False
                elif ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    up_mov = False
                elif ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    down_mov = False
                elif ev.key == pygame.K_q:
                    rot_left = False
                elif ev.key == pygame.K_e:
                    rot_right = False
                elif ev.key == pygame.K_SPACE:
                    shooting = False
        #lógica
        dt = clock.tick()
        if up_mov:
            v_y = -vel
        if left_mov:
            v_x = -vel
        if down_mov:
            v_y = vel
        if right_mov:
            v_x = vel
         
        #normalizar velocidade
        
        mod = 1/vel * (v_x **2 + v_y ** 2) ** (1/2)
        
        if mod != 0:
            pos_x, pos_y = (pos_x + (v_x/mod)*dt, pos_y + (v_y/mod)*dt)
        v_x = v_y = 0
        
        #Rotações
        
        if rot_left:
            ang += ang_vel * dt
            ang %= 360
            cp = pygame.transform.rotate(ship, ang)
        if rot_right:
            ang -= ang_vel * dt
            ang %= 360
            cp = pygame.transform.rotate(ship, ang)
        
        #Voltar ao ecrã
        
        if pos_x < 0:
            pos_x = SC_WIDTH
        if pos_y < 50:
            pos_y = SC_HEIGHT - 50
        if pos_x > SC_WIDTH:
            pos_x = 0
        if pos_y > SC_HEIGHT - 50:
            pos_y = 50
    
    
        if (pygame.time.get_ticks()) - time >= t_spawn: # Criar as térmitas
            time = pygame.time.get_ticks()
            leaving.append(False)
            moving.append(True)
            t_pos_x.append(int(random.random() * SC_WIDTH))
            t_pos_y.append(-80)
            col = random.randint(0, 2)
            t_color_in.append(colors_in[col])
            t_color_out.append(colors_out[col])
            rand = random.randint(0, 3)
            t_animation_pos.append(0)
            c_in.append(pygame.time.get_ticks() + 200)
            c_out.append(pygame.time.get_ticks() + 200)
            if rand == 0:  # up
                leave_pos.append((int(random.random() * 1000 - 20),-80 - 85))
            elif rand == 1:  # right
                leave_pos.append((1080 - 20,int(random.random() * 750)- 85))
            elif rand == 2:  # down
                leave_pos.append((int(random.random() * 1000)- 20, 750))
            else:  # left
                leave_pos.append((-80 - 20,int(random.random() * 750)- 85))
            place_pos.append((int(random.random() * 1000)- 20, random.randint(50, 750) - 85))
        for ind in range(len((t_pos_x))):  # enemies
    
            if moving[ind]:
                t_vel_x = t_vel * (place_pos[ind][0] - t_pos_x[ind])
                t_vel_y = t_vel * (place_pos[ind][1] - t_pos_y[ind])
                place_gap_x = int(place_pos[ind][0] - t_pos_x[ind])
                place_gap_y = int(place_pos[ind][1] - t_pos_y[ind])
                mod_t = 1/t_vel * (t_vel_x **2 + t_vel_y ** 2) ** (1/2)
                if mod_t != 0:
                    t_pos_x[ind], t_pos_y[ind] = t_pos_x[ind] + (t_vel_x/mod_t)*dt, t_pos_y[ind] + (t_vel_y/mod_t)*dt
                #if abs(place_gap_x) <= 10 and place_gap_y < 0:
                if ((t_vel_x < 0 and t_pos_x[ind] <= place_pos[ind][0]) or (t_vel_x >= 0 and t_pos_x[ind] >= place_pos[ind][0])) and t_pos_y[ind] >= place_pos[ind][1]:
                    leaving[ind] = True
                    place_block((t_pos_x[ind], t_pos_y[ind]), blocks)
                    moving[ind] = False
               
            elif leaving[ind]:
                t_vel_x = t_vel * (leave_pos[ind][0] - t_pos_x[ind])
                t_vel_y = t_vel * (leave_pos[ind][1] - t_pos_y[ind])
                leave_gap_x = int((leave_pos[ind][0] - t_pos_x[ind]))
                leave_gap_y = int((leave_pos[ind][1] - t_pos_y[ind]))
                mod_t = 1/t_vel * (t_vel_x **2 + t_vel_y ** 2) ** (1/2)
                if mod_t != 0:
                    t_pos_x[ind], t_pos_y[ind] = t_pos_x[ind] + (t_vel_x/mod_t)*dt, t_pos_y[ind] + (t_vel_y/mod_t)*dt
                #if leave_gap_x == 0 and leave_gap_y == 0:
                if t_pos_x[ind]+40 < 0 or t_pos_x[ind] > SC_WIDTH or t_pos_y[ind] > SC_HEIGHT-50 or t_pos_y[ind]+90 < 50:
                    del leave_pos[ind]
                    del t_pos_x[ind]
                    del t_pos_y[ind]
                    del t_color_out[ind]
                    del t_color_in[ind]
                    del place_pos[ind]
                    del leaving[ind]
                    del moving[ind]
                    del t_animation_pos[ind]
                    del c_in[ind]
                    del c_out[ind]
                    break
            
            if len(b_pos_x) != 0:
                    temp = collision_bullets((b_pos_x[0], b_pos_y[0]), 1, (t_pos_x[ind], t_pos_y[ind]), r_t, moving[ind], energized)
                    if temp[0]:
                        if not energized:
                            energized = temp[1]
                            en_time = pygame.time.get_ticks()
                        if moving[ind]:
                            place_block((t_pos_x[ind], t_pos_y[ind]), blocks)
                            if gamemode == 0:
                                score += 2
                            else:
                                score += 3
                        else:
                            if gamemode == 0:
                                score += 1
                            else:
                                score += 2
                        fuel_tot -= fuel_regen
                        explosion_sound()
                        t_d_pos.append((t_pos_x[ind], t_pos_y[ind]))
                        if colors_in.index(t_color_in[ind]) == 0:
                            t_d_color.append(t_purple_death)
                        elif colors_in.index(t_color_in[ind]) == 1:
                            t_d_color.append(t_red_death)
                        else:
                            t_d_color.append(t_green_death)
                        pos_d_ani.append(0)
                        c_d_ani.append(pygame.time.get_ticks() + 120)
                        del leave_pos[ind]
                        del t_pos_x[ind]
                        del t_pos_y[ind]
                        del t_color_out[ind]
                        del t_color_in[ind]
                        del place_pos[ind]
                        del leaving[ind]
                        del moving[ind]
                        del b_pos_x[0]
                        del b_pos_y[0]
                        del increment[0]
                        del t_animation_pos[ind]
                        del c_in[ind]
                        del c_out[ind]
                        break
            
        #Shooting Logic
    
        if shooting and pygame.time.get_ticks() >= time_shoot and len(b_pos_x) == 0:
            shoot_sound()
            b_pos_x.append(pos_x + 16 * -math.sin(math.radians(ang)))
            b_pos_y.append(pos_y + 16 * -math.cos(math.radians(ang)))
            increment.append((-math.sin(math.radians(ang)), -math.cos(math.radians(ang))))
            time_shoot = pygame.time.get_ticks() + shoot_cool
            shooting = False
        
        
        for ind in range(len(b_pos_x)):
            b_vel_x = bul_sp * dt * increment[ind][0]
            b_vel_y = bul_sp * dt * increment[ind][1]
            b_pos_x[ind], b_pos_y[ind] = b_pos_x[ind] + b_vel_x, b_pos_y[ind] + b_vel_y
            if b_pos_x[ind] < 0 or b_pos_x[ind] > SC_WIDTH or b_pos_y[ind] < 0 or b_pos_y[ind] > SC_HEIGHT:
                del b_pos_x[ind]
                del b_pos_y[ind]
                del increment[ind]
                break
        for ind in range(len((t_pos_x))):
            if not respawn:
                if collision_termites((pos_x, pos_y), r, (t_pos_x[ind], t_pos_y[ind]) , r_t):
                        lives -= 1
                        fuel_tot = 0
                        explosion_ship_sound()
                        pos_x = SC_WIDTH/2 - ship.get_width() / 2
                        pos_y = SC_HEIGHT/2 - ship.get_height() / 2
                        die_time = pygame.time.get_ticks()
                        respawn = True
                        res_time = pygame.time.get_ticks() + res_cool
                        break
        for ind, b in enumerate(blocks):
            if not energized:
                if not respawn:
                    if collision_blocks((pos_x, pos_y), r, b, r_b):
                        lives -= 1
                        fuel_tot = 0
                        explosion_ship_sound()
                        pos_x = SC_WIDTH/2 - ship.get_width() / 2
                        pos_y = SC_HEIGHT/2 - ship.get_height() / 2 
                        die_time = pygame.time.get_ticks()
                        respawn = True
                        res_time = pygame.time.get_ticks() + res_cool
                if len(b_pos_x) != 0:
                    if collision_bullets_blocks((b_pos_x[0], b_pos_y[0]), 1, b, r_b):
                            del b_pos_x[0]
                            del b_pos_y[0]
                            del increment[0]
                            block_sound()
                            break
            else:
                if not respawn:
                    if collision_blocks((pos_x, pos_y), r, b, r_b):
                        del blocks[ind]
                        if gamemode == 0:
                            score += 3
                        else:
                            score += 4
                        lives -= 1
                        fuel_tot = 0
                        explosion_ship_sound()
                        pos_x = SC_WIDTH/2 - ship.get_width() / 2
                        pos_y = SC_HEIGHT/2 - ship.get_height() / 2
                        respawn = True
                        die_time = pygame.time.get_ticks()
                        res_time = pygame.time.get_ticks() + res_cool
                        break
                if len(b_pos_x) != 0:
                    if collision_bullets_blocks((b_pos_x[0], b_pos_y[0]), 1, b, r_b):
                        del blocks[ind]
                        del b_pos_x[0]
                        del b_pos_y[0]
                        del increment[0]
                        fuel_tot -= fuel_regen
                        block_en_sound()
                        if gamemode == 0:
                            score += 3
                        else:
                            score += 4
                        break
        if energized and pygame.time.get_ticks() - en_time >= en_cool:
            energized = False
        if game_time <=  (pygame.time.get_ticks() - offset):
            if gamemode == 0:
                game_time =  (pygame.time.get_ticks() - offset) + 15000
            else:
                game_time =  (pygame.time.get_ticks() - offset) + 10000
            t_vel += 0.1 * t_vel
            fuel_inc += 0.1 * fuel_inc
            fuel_regen -= 0.1 * fuel_regen
            t_spawn -= 0.1 * t_spawn
        
        if lives == 0:
            running = False
        if fuel_tot < 0:
            fuel_tot = 0
        if int(fuel_tot) == 30:
            lives -= 1
            fuel_tot = 0
            explosion_ship_sound()
            pos_x = SC_WIDTH/2 - ship.get_width() / 2
            pos_y = SC_HEIGHT/2 - ship.get_height() / 2
            respawn = True
            die_time = pygame.time.get_ticks()
            res_time = pygame.time.get_ticks() + res_cool
        fuel_tot += fuel_inc * dt
        seconds = ((pygame.time.get_ticks() - offset) // 1000) % 60
        minutes = ((pygame.time.get_ticks() - offset) // 1000) // 60
        
        
        #gráficos
        screen.fill('black')
        if not respawn:
            if rot_left:
                screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
            elif rot_right:
                screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
            else:
                screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_width()/2)))
        else:
            if pygame.time.get_ticks() >= res_time:
                respawn = False
                tick = 400
                c = 0
                on = False
            if pygame.time.get_ticks() - die_time < tick:
                if change:
                    change = False
                    c += 1
                if c % 2 == 0:
                    on = False
                else:
                    on = True
            else:
                change = True
                tick += 200
            
            if on:
                if rot_left:
                    screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
                elif rot_right:
                    screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
                else:
                    screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_width()/2)))
            else:
                pass

        for ind in range(len(t_d_pos)):
            if pos_d_ani[ind] == 3:
                del pos_d_ani[ind]
                del t_d_pos[ind]
                del t_d_color[ind]
                del c_d_ani[ind]
                break
            else:
                screen.blit(t_d_color[ind][pos_d_ani[ind]], t_d_pos[ind])
                c_d_ani[ind] -= 1
                if pygame.time.get_ticks() >= c_d_ani[ind]:
                    c_d_ani[ind] = pygame.time.get_ticks() + 120
                    pos_d_ani[ind] += 1
        for ind, pos_x_termita in enumerate(t_pos_x):
            if moving[ind]:
                temp = t_color_in[ind][t_animation_pos[ind]]
                if pygame.time.get_ticks() >= c_in[ind]:
                    t_animation_pos[ind] += 1
                    t_animation_pos[ind] = t_animation_pos[ind] % 4
                    c_in[ind] = pygame.time.get_ticks()+200
                screen.blit(temp, (pos_x_termita, t_pos_y[ind]))
            else:
                temp = t_color_out[ind][t_animation_pos[ind]]
                if pygame.time.get_ticks() >= c_out[ind]:
                    t_animation_pos[ind] += 1
                    t_animation_pos[ind] = t_animation_pos[ind] % 4
                    c_out[ind] = pygame.time.get_ticks()+200
                screen.blit(temp, (pos_x_termita, t_pos_y[ind]))
        for ind in range(len(b_pos_x)):
            screen.blit(bullet, (b_pos_x[ind], b_pos_y[ind]))
        if not energized:
            for b in blocks:
                screen.blit(block, b)
        else:
            for b in blocks:
                screen.blit(block_en, b)
        score_suf = font.render(f'SCORE: {score}', True, 'WHITE')
        score_ret = score_suf.get_rect()
        score_ret.midtop = (500, 5)
        fuel_suf = font.render(f'FUEL', True, 'WHITE')
        fuel_ret = score_suf.get_rect()
        fuel_ret.midbottom = (800, 795)
        lives_suf = font.render(f'LIVES', True, 'WHITE')
        lives_ret = score_suf.get_rect()
        lives_ret.midbottom = (180, 795)
        timer_suf = font.render(f'{minutes:02}:{seconds:02}', True, 'WHITE')
        timer_ret = timer_suf.get_rect()
        timer_ret.midbottom = (500, 795)
        ret_bot = pygame.draw.rect(screen, pygame.Color(20, 20, 20), (0, 750, 1000, 200)) # BOTTOM RECT
        ret_top = pygame.draw.rect(screen, pygame.Color(20, 20, 20), (0, -150, 1000, 200)) # TOP RECT
        screen.blit(score_suf, score_ret) # SCORE
        screen.blit(fuel_suf, fuel_ret) # FUEL
        bg_fuel = pygame.draw.rect(screen, pygame.Color(40, 40, 40), (830, 755, 30, 40)) 
        fuel = pygame.draw.rect(screen, pygame.Color(200, 50, 20), (835, 760 + fuel_tot, 20, 30 - fuel_tot)) 
        screen.blit(lives_suf, lives_ret) # LIVES
        screen.blit(timer_suf, timer_ret) # TIMER
        if lives == 3:
            screen.blit(life, (305, 768))
        if lives >= 2:
            screen.blit(life, (275, 768))
        if lives >= 1:
            screen.blit(life, (245, 768))
        pygame.display.flip()

        if debug_speed:
            pygame.time.wait(50)
    return score
