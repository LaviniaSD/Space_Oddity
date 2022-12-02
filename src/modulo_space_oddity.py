"""Esse módulo contém funções necessárias para o andamento do jogo.
"""

# Importe as bibliotecas necessárias
import pygame
import sys


import classes_space_oddity as cso

# Crie uma variável para a fonte utilizada
font_name = pygame.font.match_font("arial")

# Crie uma função para exibição de texto
def draw_text(surface, text, size, x, y, color):
    """Exibe um texto em uma superfície, o conteúdo do texto, tamanho, cor, posição e 
    a superfície são dados como parâmetro.
    

    Parameters
    ----------
    surface : pygame.sprite.Sprite
        Superfície onde será exibido o texto.
    text : str
        Conteúdo do texto.
    size : int
        Tamanho do texto.
    x : int
        Posição do texto no eixo x.
    y : int
        Posição do texto no eixo y.
    color : tuple
        Cor do texto.

    Returns
    -------
    None.

    """
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Crie uma função para o encerramento do jogo
def quit_game():
    """Encerra o jogo e o executável.
    

    Returns
    -------
    None.

    """
    pygame.quit()
    sys.exit()
    
# Crie uma função para a dispersão de asteroides
def spawn_asteroids(asteroids_group,all_sprites_group):
    """Recebe um grupo para os sprites de asteroides e um para todos os sprites 
    e adiciona asteroides a esses grupos.  
    

    Parameters
    ----------
    asteroids_group : pygame.sprite.Group()
        Grupo com os sprites de asteroides.
    all_sprites_group : pygame.sprite.Group()
        Grupo com todos os sprites .

    Returns
    -------
    None.

    """
    asteroid = cso.Asteroid()
    asteroids_group.add(asteroid)
    all_sprites_group.add(asteroid)

#Crie uma função para dispersão de naves inimigas    
def spawn_enemy_ships(enemy_ships_group,all_sprites_group):
    """Recebe um grupo para os sprites de naves inimigas e um para todos os sprites 
    e adiciona naves inimigas a esses grupos.  
    

    Parameters
    ----------
    enemy_ships_group : pygame.sprite.Group()
        Grupo com os sprites de naves inimigas.
    all_sprites_group : pygame.sprite.Group()
        Grupo com todos os sprites .

    Returns
    -------
    None.

    """
    
    enemy = cso.Enemy_ship()
    enemy.enemy_shoots()
    enemy_ships_group.add(enemy)
    all_sprites_group.add(enemy)
    enemy.update()
    
#Crie uma função para a morte do jogador
def player_dies(loop):
    """Recebe o loop do jogo e o encerra.
    

    Parameters
    ----------
    loop : boll
        Loop do jogo.

    Returns
    -------
    loop : boll
        Loop do jogo, agora sendo "Falso".

    """
    loop = False
    return loop


    
    