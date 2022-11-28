'''Módulo Principal do jogo
Nesse módulo será executado o loop principal do jogo
'''

# Música tema de FoxSynergy
# Importe as bibliotecas necessárias
import json
import pygame
import os
import random

import classes_space_oddity as cso
import modulo_space_oddity as mso

# Defina a localização das pastas necessárias
source_folder = os.path.dirname(__file__)
img_folder = os.path.join(source_folder, "img")
sound_folder = os.path.join(source_folder, "sounds")
font_folder = os.path.join(source_folder, "fonts")
save_folder = os.path.join(source_folder, "save")

# Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

# Dimensões da tela
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h

# Frames por segundo
FPS = 30

# Crie a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Nome do jogo")

# Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()

# Crie um background
background = pygame.image.load(os.path.join(img_folder, "space.png")).convert()
background_rect = background.get_rect()

# Som de background
pygame.mixer.music.load(os.path.join(sound_folder, "som1.mp3"))
# pygame.mixer.music.set_volume(0.5)

# Crie um grupo para todos os sprites
all_sprites = pygame.sprite.Group()

# Crie um grupo para os asteroides
asteroids = pygame.sprite.Group()

# Crie um grupo para as naves inimigas
enemy_ships = pygame.sprite.Group()

# Crie um grupo para as balas
bullets = pygame.sprite.Group()

# Crie um grupo para as balas dos inimigos
enemies_bullets = pygame.sprite.Group()

in_menu = bool
is_playing = True
def menu():
    
    global data, in_menu, firts

    x_centered = WIDTH / 2
    y_centered = HEIGHT / 2

    # Instancia os botões do menu
    play_button = cso.Button(text="PLAY", x=x_centered, y=y_centered-60, width=200, height=25)
    scores_button = cso.Button(text="SCORES", x=x_centered, y=y_centered-30, width=200, height=25)
    intructions_button = cso.Button(text="INSTRUCTIONS", x=x_centered, y=y_centered, width=200, height=25)
    exit_button = cso.Button(text="EXIT", x=x_centered, y=y_centered+30, width=200, height=25)
    back_button = cso.Button(text="BACK TO GAME", x=x_centered, y=y_centered+60, width=200, height=25)

    input_box = cso.InputTextBox(x_centered-300, y_centered, 140, 32)

    # Lê os dados dos high scores a partir do arquivo ".save/scores.txt"
    scores_filepath = os.path.join(save_folder, "scores.txt")
    try:
        with open(scores_filepath, "r") as file:
            if file.read() != "":
                scores_data = json.load(file)
            else:
                scores_data = {}
    except FileNotFoundError:
        scores_data = {"scores": []} # TODO: Conferir qual seria a fórmula de um arquivo vazio
    sorted_scores = sorted(scores_data.items(), key=lambda x: x[1]['points'], reverse=True)

    # Inicia um loop para o menu
    while in_menu:
        # fnc()
        
        # Carrega a imagem de fundo do menu
        # screen.blit(menuBg, (0, 0))

        # Desenha os botões na tela
        play_button.draw(screen, (0,0,0))
        scores_button.draw(screen, (0,0,0))
        intructions_button.draw(screen, (0,0,0))
        exit_button.draw(screen, (0,0,0))

        input_box.update()
        input_box.draw(screen)

        # Caso o usuário estava jogando, desenha o botão de voltar ao jogo
        if is_playing:
            back_button.draw(screen, (0,0,0))

        # Verifica a ocorrência de eventos
        for event in pygame.event.get():
            # Recolhe a posição atual do mouse
            pos = pygame.mouse.get_pos()

            input_box.handle_event(event)
 
            # Caso o usuário feche a janela
            if event.type == pygame.QUIT:
                in_menu = False
                mso.quit_game()

            # Caso o usuário clique com o botão esquerdo do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                # Caso o usuário clique no botão de play
                if play_button.is_over(pos):
                    # changescn("enterName")
                    print("enterName")
      
                # Caso o usuário clique no botão de scores
                elif scores_button.is_over(pos):
                    # changescn("scores")
                    print("scores")

                # Caso o usuário clique no botão de instruções
                elif intructions_button.is_over(pos):
                    # changescn("instructions")
                    print("instructions")
                
                # Caso o usuário clique no botão de sair
                elif exit_button.is_over(pos):
                    in_menu = False
                    mso.quit_game()
                    
                # Caso o usuário clique no botão de voltar para o jogo (caso esteja jogando)
                elif back_button.is_over(pos):
                    # changescn("mainLoop")
                    print("mainLoop")

                else:
                    pass
                    
            # Caso o usuário aperte alguma tecla do teclado
            if event.type==pygame.KEYDOWN:
                # Caso o usuário aperte a tecla ESC
                if event.key==pygame.K_ESCAPE:
                    # changescn("mainLoop") # TODO: precisa disso aqui????
                    in_menu = False
                    print("mainLoop")
                    
        # Atualiza os conteúdos da tela
        pygame.display.flip()

menu()

 
def run_game():

    # Atribui a classe player a uma variável
    player = cso.Player()
    player.hitbox = cso.Hitbox(player)

    # Adiciona player aos grupo de sprites
    all_sprites.add(player, player.hitbox)

    # testButton = cso.Button(color=cso.WHITE, x=200, y=200, width=200, height=200, size=20, text="ABCASKLDASKLDNASD")


    #Cria uma marcação de tempo inicial para spwaning
    start_asteroids = pygame.time.get_ticks()
    start_enemies = pygame.time.get_ticks()
    
    # Loop para o jogo

    running = True
    
    pygame.mixer.music.play(loops=-1)
    
    while running:
        # Faça o jogo funcionar com a quantidade de frames por segundo estabelecidas
        clock.tick(FPS)

        # Faça o jogo reagir a eventos externos
        for event in pygame.event.get():
            # Permita que o usuário saia do jogo
            if event.type == pygame.QUIT:
                running = False
                mso.quit_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    mso.quit_game()

        # Atualiza os sprites
        all_sprites.update()
        
        
        #Spwana asteroides em intervalos de 3 segundos
        now = pygame.time.get_ticks()
        if now - start_asteroids > 3000 :
            start_asteroids = now
            mso.spwan_asteroids(asteroids,all_sprites)
       
        #Spwana naves inimigas em intervalos de 4 segundos
        if now - start_enemies > 4000:
            start_enemies = now
            mso.spwan_enemy_ships(enemy_ships,all_sprites)
        


        #Cria casos de colisão entre balas do jogador e asteroides
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            asteroid_score = hit.get_score()
            player.set_score(asteroid_score) 
            
            explosion_sound = pygame.mixer.Sound(
                os.path.join(sound_folder, "Explosion7.wav"))
            explosion_sound.play()
            new_asteroid = cso.Asteroids()
            all_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)
            
            
        #Cria casos de colisão entre balas do jogador e naves inimigas    
        hits = pygame.sprite.groupcollide(enemy_ships,bullets, True, True)
        for hit in hits:
            enemy_score = hit.get_score()
            player.set_score(enemy_score) 
            
            explosion_sound = pygame.mixer.Sound(
                os.path.join(sound_folder, "Explosion7.wav"))
            explosion_sound.play()
            
        #Cria casos de colisão entre jogador e asteroides    
        hits = pygame.sprite.spritecollide(
            player.hitbox, asteroids, False, pygame.sprite.collide_circle)
        if hits:
            running = False
            
        #Cria casos de colisão entre balas do inimigo e o jogador    
        hits = pygame.sprite.spritecollide(
            player.hitbox, enemies_bullets, False, pygame.sprite.collide_circle)
        if hits:
            running = False
            
        #Cria casos de colisão entre nave inimiga e o jogador    
        hits = pygame.sprite.spritecollide(
            player.hitbox, enemy_ships, False, pygame.sprite.collide_circle)
        if hits:
            running = False    
            
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LSHIFT]:
                player.hitbox.set_visible(True)
        elif not keys_pressed[pygame.K_LSHIFT]:
                player.hitbox.set_visible(False)

        


        # Defina a imagem de fundo da tela
        screen.fill((0, 0, 0))

        # Adiciona a imagem de fundo
        screen.blit(background, background_rect)

        # Atualize as imagens dos objetos quando ocorrerem mudanças
        pygame.display.flip()

        # Desenha os sprites na tela
        all_sprites.draw(screen)

        # Insere o score na tela

        #Adiciona a pontuação no topo da tela
        mso.draw_text(screen, f'score: {str(player.get_score())}', 40, WIDTH/2, 10,(255,255,255))

        # Atualiza o jogo
        pygame.display.update()
        
    #Encerra o jogo quando o loop acaba    
    pygame.quit()

