'''Módulo Principal do jogo
Nesse módulo será executado o loop principal do jogo
'''
#Música tema de FoxSynergy
#Importe as bibliotecas necessárias
import pygame
import os

import classes_space_oddity as cso
import modulo_space_oddity as mso

#Defina a localização das pastas necessárias
source_folder = os.path.dirname(__file__)
img_folder = os.path.join(source_folder, "img")
sound_folder = os.path.join(source_folder, "sounds")

#Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

#Dimensões da tela
display_info = pygame.display.Info()
WIDTH = display_info.current_w
HEIGHT = display_info.current_h

#Frames por segundo
FPS = 30

#Crie a tela
screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.FULLSCREEN)

#Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Nome do jogo")

#Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()

#Crie um background
background =  pygame.image.load(os.path.join(img_folder,"space.png")).convert()
background_rect = background.get_rect()

#Som de background
pygame.mixer.music.load(os.path.join(sound_folder,"som1.mp3"))
#pygame.mixer.music.set_volume(0.5)

#Crie um grupo para todos os sprites
all_sprites = pygame.sprite.Group()

#Crie um grupo para os asteroides
asteroids = pygame.sprite.Group()

#Crie um grupo para as balas
bullets = pygame.sprite.Group()

def run_game():

    #Atribui a classe player a uma variável
    player = cso.Player()

    #Adiciona player aos grupo de sprites
    all_sprites.add(player)

    #Adiciona 5 asteroides na tela por vez
    for i in range (5):
        asteroid= cso.Asteroids()
        asteroids.add(asteroid)
        all_sprites.add(asteroids)

    #Loop para o jogo

    running = True

    score = 0
    pygame.mixer.music.play(loops=-1)
    while running:
        #Faça o jogo funcionar com a quantidade de frames por segundo estabelecidas
        clock.tick(FPS)
        
        
        #Faça o jogo reagir a eventos externos
        for event in pygame.event.get():
            #Permita que o usuário saia do jogo
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                
                
        #Atualiza os sprites
        all_sprites.update()
        
        
        
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            score += 50
            explosion_sound = pygame.mixer.Sound(os.path.join(sound_folder,"Explosion7.wav"))
            explosion_sound.play()
            new_asteroid = cso.Asteroids()
            all_sprites.add(new_asteroid)
            asteroids.add(new_asteroid)
            
        
        hits = pygame.sprite.spritecollide(player, asteroids, False,pygame.sprite.collide_circle)
        if hits:
            running = False
            
        
        
        #Defina a imagem de fundo da tela
        screen.fill((0,0,0))
        
        #Adiciona a imagem de fundo
        screen.blit(background,background_rect)
        
        #Atualize as imagens dos objetos quando ocorrerem mudanças
        pygame.display.flip()
        
        #Desenha os sprites na tela
        all_sprites.draw(screen)
        
        mso.draw_text(screen,f'score: {str(score)}',20,WIDTH/2,10)

        #Atualiza o jogo
        pygame.display.update()