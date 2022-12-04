import os
import pygame

# Defina os caminhos para as pastas necessárias
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

# Define cores 
RED = (255, 0, 0)
GREEN = (20, 255, 140)
BLUE = (100, 100, 255)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (194,9,84)

#Define a fonte utilizada no jogo
font = pygame.font.SysFont("arcade", 20)

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

# Crie um grupo para os bônus
powers = pygame.sprite.Group()

# Crie um background
background = pygame.image.load(os.path.join(img_folder, "space.jpg"))

# Armazene a altura desse background
background_height = background.get_height()

# Som de background
pygame.mixer.music.load(os.path.join(sound_folder, "som1.mp3"))
pygame.mixer.music.set_volume(0.5)