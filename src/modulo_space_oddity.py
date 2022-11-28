import pygame
import sys
import random
import time

import classes_space_oddity as cso

# Crie uam função para a fonte
font_name = pygame.font.match_font("arial")

def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def quit_game():
    pygame.quit()
    sys.exit()
    
def spwan_asteroids(asteroids_group,all_sprites_group):
    asteroid = cso.Asteroids()
    asteroids_group.add(asteroid)
    all_sprites_group.add(asteroid)
    
def spwan_enemy_ships(enemy_ships_group,all_sprites_group):
    enemy = cso.Enemy_ship()
    enemy_shoots(enemy)
    enemy_ships_group.add(enemy)
    all_sprites_group.add(enemy)
    enemy.update()
    
def enemy_shoots(enemy):
    for i in range (10):
        x_speed= random.randint(-10,10)
        y_speed= random.randint(10,10)
        enemy.shoot(x_speed,y_speed)
        time.sleep(0.001)
    
    
    