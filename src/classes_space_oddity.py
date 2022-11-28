import pygame
import random
import os

import space_oddity as so
import modulo_space_oddity as mso

RED = (255, 0, 0)
GREEN = (20, 255, 140)
BLUE = (100, 100, 255)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (194,9,84)

pygame.init()

font = pygame.font.SysFont('arial', 20)

#Cria a classe para o jogador
class Player(pygame.sprite.Sprite):
    #Características iniciais da classe quando ela é iniciada
    def __init__(self):
        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(so.img_folder,"ship.png")).convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image.set_colorkey((0,0,0))

        #Orienta a posição inicial do jogador
        self.rect = self.image.get_rect()
        self.radius = 28
        self.rect.centerx = so.WIDTH/2
        self.rect.bottom = so.HEIGHT -10
        self.x_speed = 0
        self.y_speed = 0
        
    #Atualiza a nave de acordo com os comandos do jogador   
    def update(self):
        self.x_speed = 0
        self.y_speed = 0
        #Reage a interações do usuário
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.x_speed = -8
        if keystate[pygame.K_RIGHT]:
            self.x_speed = 8
        if keystate[pygame.K_UP]:
            self.y_speed = -8
        if keystate[pygame.K_DOWN]:
            self.y_speed = 8
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        
        #Não deixa que o jogador ultrapasse os limites da tela
        if self.rect.right > so.WIDTH:
            self.rect.right = so.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > so.HEIGHT:
            self.rect.bottom = so.HEIGHT
    def shoot(self):
        shoot_sound = pygame.mixer.Sound(os.path.join(so.sound_folder,"Laser_Shoot4.wav"))
        shoot_sound.set_volume(0.5)
        bullet = Bullet(self.rect.centerx,self.rect.top)
        so.all_sprites.add(bullet)
        so.bullets.add(bullet)
        shoot_sound.play()

#Cria a classe para os asteroides 
class Asteroids(pygame.sprite.Sprite):
    #Características iniciais da classe quando ela é iniciada
    def __init__(self):
        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(so.img_folder,"asteroid.png")).convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image.set_colorkey((0,0,0))
        #Orienta a posição inicial do jogador
        self.rect = self.image.get_rect()
        self.radius = 30
        self.rect.x = random.randrange(so.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-40,-15)
        
        #Define uma velocidade aleatória para cada asteroide
        self.x_speed = random.randrange(-5,5)
        self.y_speed = random.randrange(1,10)
    
    #Muda a posição do asteroide
    def update(self):
        self.rect.x += self.x_speed 
        self.rect.y += self.y_speed 
        
        #Caso o asteroide ultrapasse as bordas, crie outro
        if self.rect.top > so.HEIGHT + 10 or self.rect.left < -10 or self.rect.right > so.WIDTH + 10:
            self.x_speed = random.randrange(-5,5)
            self.y_speed = random.randrange(1,10)
            self.rect.x = random.randrange(so.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.y_speed = random.randrange(1,10)

class Bullet(pygame.sprite.Sprite):
    #Características iniciais da classe quando ela é iniciada
    def __init__(self,x,y):
        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(so.img_folder,"bullet.png")).convert()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.image.set_colorkey((0,0,0))
        #Orienta a posição inicial do jogador
        self.rect = self.image.get_rect()       
        self.rect.bottom = y
        self.rect.centerx = x
        
        #Define uma velocidade aleatória para cada asteroide
        self.y_speed = -15
    
    #Muda a posição do asteroide
    def update(self):
        self.rect.y += self.y_speed 
        
        #Caso o asteroide ultrapasse as bordas, crie outro
        if self.rect.bottom < 0:
            self.kill()

class Button():

    # Construtor da classe Button
    def __init__(self, text, x, y, width=200, height=25, font_size=20, background_color=(255, 255, 255), text_color=(0,0,0), centered=True):
        self.text = text
        # Caso deseje centralizar o componente nas coordenadas apontadas
        if not centered:
            self.x = x
            self.y = y
        else:
            self.x = x - width/2
            self.y = y - height/2
        self.width = width
        self.height = height
        self.font_size = font_size
        self.background_color = background_color
        self.text_color = text_color
        self.centered = centered

    # Método para desenhar o botão na tela
    def draw(self, screen, outline=None):
        # Desenha uma borda ao redor do botão, caso outline seja True
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        
        # Desenha o retângulo do botão
        pygame.draw.rect(screen, self.background_color, (self.x,self.y,self.width,self.height),0)
        
        # Caso o botão tenha texto, desenha o texto
        if self.text != "":
            text_surface = font.render(self.text, 1, self.text_color)
            screen.blit(text_surface, (self.x + (self.width/2 - text_surface.get_width()/2), self.y + (self.height/2 - text_surface.get_height()/2)))

        # Recolhe a posição do mouse
        pos = pygame.mouse.get_pos()
        # Altera a cor de fundo do botão, caso o mouse esteja sobre ele
        if self.is_over(pos):
            self.background_color = WHITE
        else:
            self.background_color = GREY

    # Método para verificar se o mouse está sobre o botão
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
                
        return False

class InputTextBox():

    # Defina as cores padrão das bordas para os estados de atividade do componente
    COLOR_INACTIVE = GREY
    COLOR_ACTIVE = BLACK

    # Construtor da classe InputTextBox
    def __init__(self, x, y, width=200, height=25, text="", background_color=(255, 255, 255), text_color=(0, 0, 0), centered=True, max_input_length=30):
        # Caso deseje centralizar o componente nas coordenadas apontadas
        if not centered:
            self.x = x
            self.y = y
        else:
            self.x = x - width/2
            self.y = y - height/2
        self.width = width
        self.height = height
        self.text = text
        self.background_color = background_color
        self.text_color = text_color
        self.centered = centered
        self.max_input_length = max_input_length

        # Defina propriedades secundárias do componente
        self.outline_color = InputTextBox.COLOR_INACTIVE
        self.text_surface = font.render(text, True, text_color)
        self.active = False
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # Método para permitir que a caixa de texto interaja com os eventos do sistema
    def handle_event(self, event):
        # Caso o usuário clique com o botão esquerdo do mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Caso o mouse esteja sobre a caixa de texto
            if self.rect.collidepoint(event.pos):
                # Ative a caixa de texto
                self.active = not self.active
            else:
                # Desative a caixa de texto
                self.active = False
            
            # Altere a cor da borda da caixa de texto segundo o seu estado
            self.outline_color = InputTextBox.COLOR_ACTIVE if self.active else InputTextBox.COLOR_INACTIVE
        
        # Caso o usuário pressione alguma tecla do teclado
        elif event.type == pygame.KEYDOWN:
            # Caso a caixa de texto esteja ativa
            if self.active:
                # Caso a tecla pressionada seja a tecla ENTER
                if event.key == pygame.K_RETURN:
                    self.text = ""
                # Caso a tecla pressionada seja a tecla BACKSPACE
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Caso qualquer outra tecla seja pressionada
                else:
                    if len(self.text) < self.max_input_length:
                        self.text += event.unicode

                # Atualize a superfície de texto
                self.text_surface = font.render(self.text, True, self.outline_color)

    # Método para atualizar o tamanho da caixa de texto caso o texto seja maior que o tamanho da caixa   
    def update(self):
        self.width = max(self.width, self.text_surface.get_width()+10)
        self.rect.w = self.width

    # Método para desenhar o componente na tela
    def draw(self, screen):
        # Desenhe a caixa de texto
        pygame.draw.rect(screen, self.background_color, (self.x,self.y,self.width,self.height),0)
        # Desenhe a borda da caixa de texto
        pygame.draw.rect(screen, self.outline_color, self.rect, 2)

        # Desenhe o texto na caixa de texto
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))