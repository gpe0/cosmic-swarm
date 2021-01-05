import pygame
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
r_b = 6
energized = False
en_time = 0
en_cool = 3000
game_time = 15000
score = 0

ang = 0
r = 10


#Coordenadas iniciais das térmitas
t_pos_x = []
t_pos_y = []

t_vel = 0.15
spawn_c = 0 # contador de térmitas
t_color_in = []
t_color_out = []
leave_pos = [] # Parede de saída da térmita
place_pos = []
leaving = []
moving = []
r_t = 20

blocks = []
ship = pygame.image.load('images/best_ship.png')
ship.set_colorkey((0, 0, 0))
bullet = pygame.image.load('images/bullet.png')
ter1_in = pygame.image.load('images/termite_purple_block.png')
ter2_in = pygame.image.load('images/termite_red_block.png')
ter3_in = pygame.image.load('images/termite_green_block.png')
ter1_out = pygame.image.load('images/termite_purple.png')
ter2_out = pygame.image.load('images/termite_red.png')
ter3_out = pygame.image.load('images/termite_green.png')
block = pygame.image.load('images/square.png')
block_en = pygame.image.load('images/square_energized.png')
colors_in = [ter1_in, ter2_in, ter3_in]
colors_out = [ter1_out, ter2_out, ter3_out]

clock = pygame.time.Clock()

#Coordenadas e angulo inicial da nave
pos_x = SC_WIDTH/2 - ship.get_width() / 2
pos_y = SC_HEIGHT/2 - ship.get_height() / 2
cp = ship