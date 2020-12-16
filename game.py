import pygame
import random

# Constantes iniciais
SC_WIDTH = 800
SC_HEIGHT = 600
left_mov = False
right_mov = False
up_mov = False
down_mov = False
rot_left = False
rot_right = False
spawn_ter = False
v_x = 0
v_y = 0
vel = 0.35 # velocidade x e y
ang_vel = 0.15 # velocidade de rotação
time = 0 # inicio do jogo

#Inicialização

pygame.init()

screen = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

pygame.display.set_caption('Cosmic Swarm')

ship = pygame.image.load('images/ship.png')
ship.set_colorkey((0, 0, 0))

clock = pygame.time.Clock()

#Coordenadas e angulo inicial da nave
pos_x = SC_WIDTH/2 - ship.get_width() / 2
pos_y = SC_HEIGHT/2 - ship.get_height() / 2
ang = 0
cp = ship

#Coordenadas iniciais das térmitas
t_pos_x = []
t_pos_y = []
spawn_c = 0 # contador de térmitas


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
    if pygame.time.get_ticks() - time >= 6000: # Criar as térmitas
        time = pygame.time.get_ticks()
        t_pos_x.append(int(random.random() * 800))
        t_pos_y.append(-10)
    for ind in range(len((t_pos_x))):
        t_pos_y[ind] += vel * dt
        
        
    #gráficos
    screen.fill('black')
    if rot_left:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
    elif rot_right:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
    else:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_width()/2)))
    for ind, pos_x_termita in enumerate(t_pos_x):
        screen.blit(ship, (pos_x_termita, t_pos_y[ind]))
    pygame.display.flip()
pygame.quit()
