import pygame
import random
import math


def collision_termites(p1, r1, p2, r2):
    d1 = ((p1[0]) - (p2[0] + 20))**2 + ((p1[1]) - (p2[1] + 20))**2
    d2 = ((p1[0]) - (p2[0] + 20))**2 + ((p1[1]) - (p2[1] + 60))**2
    return (d1 < (r1 + r2)**2) or (d2 < (r1 + r2)**2)


def collision_bullets(p1, r1, p2, r2):
    d1 = ((p1[0] + 1) - (p2[0] + 20))**2 + ((p1[1] + 1) - (p2[1] + 20))**2
    d2 = ((p1[0] + 1) - (p2[0] + 20))**2 + ((p1[1] + 1) - (p2[1] + 60))**2
    return (d1 < (r1 + r2)**2) or (d2 < (r1 + r2)**2)


# Constantes iniciais
SC_WIDTH = 1000
SC_HEIGHT = 800
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
time = 0 # inicio do jogo
bul_sp = 0.5 # velocidade da bala
b_pos_x = []
b_pos_y = []
increment = []
shoot_cool = 1000 # Cooldown para disparar
time_shoot = 0

#Inicialização

pygame.init()

screen = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

pygame.display.set_caption('Cosmic Swarm')

ship = pygame.image.load('images/best_ship.png')
ship.set_colorkey((0, 0, 0))
bullet = pygame.image.load('images/bullet.png')
ter1_in = pygame.image.load('images/termite_purple_block.png')
ter2_in = pygame.image.load('images/termite_red_block.png')
ter3_in = pygame.image.load('images/termite_green_block.png')
ter1_out = pygame.image.load('images/termite_purple.png')
ter2_out = pygame.image.load('images/termite_red.png')
ter3_out = pygame.image.load('images/termite_green.png')
colors_in = [ter1_in, ter2_in, ter3_in]
colors_out = [ter1_out, ter2_out, ter3_out]

clock = pygame.time.Clock()

#Coordenadas e angulo inicial da nave
pos_x = SC_WIDTH/2 - ship.get_width() / 2
pos_y = SC_HEIGHT/2 - ship.get_height() / 2
ang = 0
r = 10
cp = ship

#Coordenadas iniciais das térmitas
t_pos_x = []
t_pos_y = []

t_vel = 0.25
spawn_c = 0 # contador de térmitas
t_color_in = []
t_color_out = []
leave_pos = [] # Parede de saída da térmita
place_pos = []
leaving = []
moving = []
r_t = 20

running = True
while running:
    #eventos
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                running = False
            elif ev.key == pygame.K_a:
                left_mov = True
            elif ev.key == pygame.K_d:
                right_mov = True
            elif ev.key == pygame.K_w:
                up_mov = True
            elif ev.key == pygame.K_s:
                down_mov = True  
            elif ev.key == pygame.K_q:
                rot_left = True  
            elif ev.key == pygame.K_e:
                rot_right = True  
            elif ev.key == pygame.K_SPACE and len(b_pos_x) == 0:
                shooting = True
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_a:
                left_mov = False
            elif ev.key == pygame.K_d:
                right_mov = False
            elif ev.key == pygame.K_w:
                up_mov = False
            elif ev.key == pygame.K_s:
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
    if pos_y < 0:
        pos_y = SC_HEIGHT
    if pos_x > SC_WIDTH:
        pos_x = 0
    if pos_y > SC_HEIGHT:
        pos_y = 0


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
            leave_pos.append((int(random.random() * 1000),-80))
        elif rand == 1:
            leave_pos.append((1080,int(random.random() * 800)))
        elif rand == 2:
            leave_pos.append((int(random.random() * 1000),880))
        else:
            leave_pos.append((-80,int(random.random() * 800)))
        place_pos.append((int(random.random() * 1000), int(random.random() * 800)))
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
                if collision_bullets((b_pos_x[0], b_pos_y[0]), 1, (t_pos_x[ind], t_pos_y[ind]), r_t):
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
            time_shoot += shoot_cool
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
            if collision_termites((pos_x, pos_y), r, (t_pos_x[ind], t_pos_y[ind]) , r_t):
                    running = False
                    break
        
    #gráficos
    screen.fill('black')
    if rot_left:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
    elif rot_right:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
    else:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_width()/2)))
    for ind, pos_x_termita in enumerate(t_pos_x):
        if moving[ind]:
            screen.blit(t_color_in[ind], (pos_x_termita, t_pos_y[ind]))
        else:
            screen.blit(t_color_out[ind], (pos_x_termita, t_pos_y[ind]))
    for ind in range(len(b_pos_x)):
        screen.blit(bullet, (b_pos_x[ind], b_pos_y[ind]))
    pygame.display.flip()
pygame.quit()
