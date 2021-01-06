import pygame
import random
import math
from constants import *

def place_block(termite_pos):
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


#Inicialização

pygame.init()
screen = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

pygame.display.set_caption('Cosmic Swarm')
font = pygame.font.Font('font/8-bit-pusab.ttf', 23)

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
        v_y = -vel * dt
    if left_mov:
        v_x = -vel * dt
    if down_mov:
        v_y = vel * dt
    if right_mov:
        v_x = vel * dt
     
    #normalizar velocidade
    
    mod =  1/vel * (v_x **2 + v_y ** 2) ** (1/2)
    
    if mod != 0:
        pos_x, pos_y = (pos_x + v_x/mod, pos_y + v_y/mod)
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


    if pygame.time.get_ticks() - time >= 4000: # Criar as térmitas
        time = pygame.time.get_ticks()
        leaving.append(False)
        moving.append(True)
        t_pos_x.append(int(random.random() * SC_WIDTH))
        t_pos_y.append(-80)
        col = random.randint(0, 2)
        t_color_in.append(colors_in[col])
        t_color_out.append(colors_out[col])
        rand = random.randint(0, 3)
        if rand == 0:
            leave_pos.append((int(random.random() * 1000 - 20),-80 - 85))
        elif rand == 1:
            leave_pos.append((1080 - 20,int(random.random() * 750)- 85))
        elif rand == 2:
            leave_pos.append((int(random.random() * 1000)- 20,750 + 80 - 85))
        else:
            leave_pos.append((-80 - 20,int(random.random() * 750)- 85))
        place_pos.append((int(random.random() * 1000)- 20, random.randint(50, 750) - 85))
    for ind in range(len((t_pos_x))):

        if moving[ind]:
            t_vel_x = t_vel * dt * (place_pos[ind][0] - t_pos_x[ind])
            t_vel_y = t_vel * dt * (place_pos[ind][1] - t_pos_y[ind])
            place_gap_x = int((place_pos[ind][0] - t_pos_x[ind]))
            place_gap_y = int((place_pos[ind][1] - t_pos_y[ind]))
            mod_t = 1/t_vel * (t_vel_x **2 + t_vel_y ** 2) ** (1/2)
            if mod_t != 0:
                t_pos_x[ind], t_pos_y[ind] = t_pos_x[ind] + t_vel_x/mod_t, t_pos_y[ind] + t_vel_y/mod_t
            if place_gap_x == 0 and place_gap_y == 0:
                leaving[ind] = True
                place_block((t_pos_x[ind], t_pos_y[ind]))
                moving[ind] = False
           
        elif leaving[ind]:
            t_vel_x = t_vel * dt * (leave_pos[ind][0] - t_pos_x[ind])
            t_vel_y = t_vel * dt * (leave_pos[ind][1] - t_pos_y[ind])
            leave_gap_x = int((leave_pos[ind][0] - t_pos_x[ind]))
            leave_gap_y = int((leave_pos[ind][1] - t_pos_y[ind]))
            mod_t = 1/t_vel * (t_vel_x **2 + t_vel_y ** 2) ** (1/2)
            if mod_t != 0:
                t_pos_x[ind], t_pos_y[ind] = t_pos_x[ind] + t_vel_x/mod_t, t_pos_y[ind] + t_vel_y/mod_t
            if leave_gap_x == 0 and leave_gap_y == 0:
                del leave_pos[ind]
                del t_pos_x[ind]
                del t_pos_y[ind]
                del t_color_out[ind]
                del t_color_in[ind]
                del place_pos[ind]
                del leaving[ind]
                del moving[ind]
                break
        
        if len(b_pos_x) != 0:
                temp = collision_bullets((b_pos_x[0], b_pos_y[0]), 1, (t_pos_x[ind], t_pos_y[ind]), r_t, moving[ind], energized)
                if temp[0]:
                    if not energized:
                        energized = temp[1]
                        en_time = pygame.time.get_ticks()
                    if moving[ind]:
                        place_block((t_pos_x[ind], t_pos_y[ind]))
                        score += 2
                    else:
                        score += 1
                    fuel_tot -= 5
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
                    break
        
    #Shooting Logic

    if shooting and pygame.time.get_ticks() >= time_shoot and len(b_pos_x) == 0:
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
                        break
        else:
            if not respawn:
                if collision_blocks((pos_x, pos_y), r, b, r_b):
                    del blocks[ind]
                    lives -= 1
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
                    fuel_tot -= 7
                    score += 3
                    break
    if energized and pygame.time.get_ticks() - en_time >= en_cool:
        energized = False
    if game_time <=  pygame.time.get_ticks():
        game_time =  pygame.time.get_ticks() + 15000
        t_vel += 0.03
    
    if lives == 0:
        running = False
    if fuel_tot < 0:
        fuel_tot = 0
    if int(fuel_tot) == 30:
        running = False
    fuel_tot += 0.0005

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
            
    for ind, pos_x_termita in enumerate(t_pos_x):
        if moving[ind]:
            screen.blit(t_color_in[ind], (pos_x_termita, t_pos_y[ind]))
        else:
            screen.blit(t_color_out[ind], (pos_x_termita, t_pos_y[ind]))
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
    lives_ret.midbottom = (200, 795)
    ret_bot = pygame.draw.rect(screen, pygame.Color(20, 20, 20), (0, 750, 1000, 200)) # BOTTOM RECT
    ret_top = pygame.draw.rect(screen, pygame.Color(20, 20, 20), (0, -150, 1000, 200)) # TOP RECT
    screen.blit(score_suf, score_ret) # SCORE
    screen.blit(fuel_suf, fuel_ret) # FUEL
    bg_fuel = pygame.draw.rect(screen, pygame.Color(40, 40, 40), (830, 755, 30, 40)) 
    fuel = pygame.draw.rect(screen, pygame.Color(200, 50, 20), (835, 760 + fuel_tot, 20, 30 - fuel_tot)) 
    screen.blit(lives_suf, lives_ret) # LIVES
    if lives == 3:
        screen.blit(life, (325, 768))
    if lives >= 2:
        screen.blit(life, (295, 768))
    if lives >= 1:
        screen.blit(life, (265, 768))
    pygame.display.flip()
pygame.quit()
