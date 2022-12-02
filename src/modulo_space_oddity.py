''' Esse módulo contém funções necessárias para o andamento do jogo
'''

# Importe as bibliotecas necessárias
import pygame
import sys
import random
import time

import classes_space_oddity as cso

# Crie uma variável para a fonte utilizada
font_name = pygame.font.match_font("arial")

# Crie uma função para exibição de texto
def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Crie uma função para o encerramento do jogo
def quit_game():
    pygame.quit()
    sys.exit()
    
# Crie uma função para a dispersão de asteróides
def spawn_asteroids(asteroids_group,all_sprites_group):
    asteroid = cso.Asteroid()
    asteroids_group.add(asteroid)
    all_sprites_group.add(asteroid)

#Crie uma função para dispersão de naves inimigas    
def spawn_enemy_ships(enemy_ships_group,all_sprites_group):
    enemy = cso.Enemy_ship()
    enemy.enemy_shoots()
    enemy_ships_group.add(enemy)
    all_sprites_group.add(enemy)
    enemy.update()
    
#Crie uma função para a morte do jogador
def player_dies(loop):
    loop = False
    return loop


    
    