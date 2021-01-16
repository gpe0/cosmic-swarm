import pygame


def select_sound():
    pygame.mixer.music.load("sounds/select.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()


def menu(screen, score):
    up = False
    down = False
    running = True
    actual = 0
    press = False
    font = pygame.font.Font('font/8-bit-pusab.ttf', 70)
    font2 = pygame.font.Font('font/8-bit-pusab.ttf', 50)
    font3 = pygame.font.Font('font/8-bit-pusab.ttf', 30)
    font4 = pygame.font.Font('font/8-bit-pusab.ttf', 20)
    c1 = 'WHITE'
    c2 = 'WHITE'
    c3 = 'WHITE'
    time = 0
    while running:
        #eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
                return 2
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False
                    return 2
                elif (ev.key == pygame.K_w or ev.key == pygame.K_UP) and time <= pygame.time.get_ticks():
                    up = True
                    time = pygame.time.get_ticks() + 300
                elif (ev.key == pygame.K_s or ev.key == pygame.K_DOWN) and time <= pygame.time.get_ticks():
                    down = True
                    time = pygame.time.get_ticks() + 300
                elif ev.key == pygame.K_RETURN:
                    press = True
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_w or ev.key == pygame.K_UP:
                    up = False
                    time = pygame.time.get_ticks()
                elif ev.key == pygame.K_s or ev.key == pygame.K_DOWN:
                    down = False
                    time = pygame.time.get_ticks()
        #lógica
        if press:
            select_sound()
            return actual
        if up:
            actual = (actual - 1)  % 3
            up = False
            select_sound()
        if down:
            actual = (actual + 1)  % 3
            down = False
            select_sound()
        
        if actual == 0:
            c1 = pygame.Color(255, 107, 107)
            c2 = pygame.Color(255, 255, 255)
            c3 = pygame.Color(255, 255, 255)
        elif actual == 1:
            c1 = pygame.Color(255, 255, 255)
            c3 = pygame.Color(255, 107, 107)
            c2 = pygame.Color(255, 255, 255)
        else:
            c1 = pygame.Color(255, 255, 255)
            c2 = pygame.Color(255, 107, 107)
            c3 = pygame.Color(255, 255, 255)
        
        #gráficos
        
        screen.fill('black')
        
        title_suf = font2.render('COSMIC SWARM', True, pygame.Color(143, 206, 143))
        title_ret = title_suf.get_rect()
        title_ret.midtop = (500, 100)
        screen.blit(title_suf, title_ret)

        score_suf = font3.render(f'HIGHSCORE: {score}', True, 'WHITE')
        score_ret = score_suf.get_rect()
        score_ret.midtop = (500, 250)
        screen.blit(score_suf, score_ret)
        
        play_n_suf = font2.render('NORMAL MODE', True, c1)
        play_n_ret = play_n_suf.get_rect()
        play_n_ret.midtop = (500, 350)
        screen.blit(play_n_suf, play_n_ret)
        
        play_h_suf = font2.render('HARD MODE', True, c3)
        play_h_ret = play_h_suf.get_rect()
        play_h_ret.midtop = (500, 500)
        screen.blit(play_h_suf, play_h_ret)
        
        play_h2_suf = font4.render('+ points', True, c3)
        play_h2_ret = play_h2_suf.get_rect()
        play_h2_ret.midtop = (830, 500)
        screen.blit(play_h2_suf, play_h2_ret)

        quit_suf = font2.render('QUIT', True, c2)
        quit_ret = quit_suf.get_rect()
        quit_ret.midtop = (500, 650)
        screen.blit(quit_suf, quit_ret)
        pygame.display.flip()
    
