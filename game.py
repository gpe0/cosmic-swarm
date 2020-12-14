import pygame

# Constantes iniciais
SC_WIDTH = 800
SC_HEIGHT = 600
left_mov = False
right_mov = False
up_mov = False
down_mov = False
rot_left = False
rot_right = False

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
        pos_y -= 0.3 * dt
    if left_mov:
        pos_x -= 0.3 * dt
    if down_mov:
        pos_y += 0.3 * dt
    if right_mov:
        pos_x += 0.3 * dt
    
    if rot_left:
        ang += 0.2 * dt
        ang %= 360
        cp = pygame.transform.rotate(ship, ang)
    if rot_right:
        ang -= 0.2 * dt
        ang %= 360
        cp = pygame.transform.rotate(ship, ang)

    #gráficos
    screen.fill('black')
    if rot_left:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
    elif rot_right:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_height()/2)))
    else:
        screen.blit(cp, (pos_x - int(cp.get_width()/2), pos_y - int(cp.get_width()/2)))
    pygame.display.flip()
pygame.quit()
