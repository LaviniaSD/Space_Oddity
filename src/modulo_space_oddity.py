import pygame
import sys

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
    
