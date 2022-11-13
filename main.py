'''Módulo Principal do jogo
Nesse módulo será executado o loop principal do jogo
'''

#Importe as bibliotecas necessárias
import pygame
import random
import os

#Defina a localização das pastas necessárias
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")


#Dimensões da tela
WIDTH = 800
HEIGHT = 600

#Frames por segundo
FPS = 30

#Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

#Crie a tela
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Nome do jogo")

#Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()

#Crie um grupo para os sprites
all_sprites = pygame.sprite.Group()

#Crie um grupo para os asteroides
asteroids = pygame.sprite.Group()

#Crie um grupo para as balas
bullets = pygame.sprite.Group()

#Cria a classe para o jogador
class Player(pygame.sprite.Sprite):
    #Característimas iniciais da classe quando ela é iniciada
    def __init__(self):
        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"ship.png")).convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image.set_colorkey((0,0,0))

        #Orienta a posição inicial do jogador
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT -10
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
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
    
#Cria a classe para os asteroides 
class Asteroids(pygame.sprite.Sprite):
    #Característimas iniciais da classe quando ela é iniciada
    def __init__(self):
        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"asteroid.png")).convert()
        self.image.set_colorkey((0,0,0))
        #Orienta a posição inicial do jogador
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        
        #Define uma velocidade aleatória para cada asteroide
        self.x_speed = random.randrange(-5,5)
        self.y_speed = random.randrange(1,10)
    
    #Muda a posição do asteroide
    def update(self):
        self.rect.x += self.x_speed 
        self.rect.y += self.y_speed 
        
        #Caso o asteroide ultrapasse as bordas, crie outro
        if self.rect.top > HEIGHT + 10 or self.rect.left < -10 or self.rect.right > WIDTH + 10:
            self.x_speed = random.randrange(-5,5)
            self.y_speed = random.randrange(1,10)
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.y_speed = random.randrange(1,10)  
        
class Bullet(pygame.sprite.Sprite):
    #Característimas iniciais da classe quando ela é iniciada
    def __init__(self,x,y):
        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(img_folder,"bullet.png")).convert()
        self.image.set_colorkey((0,0,0))
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/2), int(self.size[1]/2)))
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

#Atribui a classe player a uma variável
player = Player()

#Adiciona player aos grupo de sprites
all_sprites.add(player)

#Adiciona 5 asteroides na tela por vez
for i in range (5):
    asteroid= Asteroids()
    asteroids.add(asteroid)
    all_sprites.add(asteroids)

#Loop para o jogo

running = True

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
            
            
    #Atualiza os sprites
    all_sprites.update()
    
    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for hit in hits:
        new_asteroid = Asteroids()
        all_sprites.add(new_asteroid)
        asteroids.add(new_asteroid)
    
    hits = pygame.sprite.spritecollide(player, asteroids, False)
    if hits:
        running = False
    
    #Defina a imagem de fundo da tela
    screen.fill((0,0,0))
    
    #Atualize as imagens dos objetos quando ocorrerem mudanças
    pygame.display.flip()
    
    #Desenha os sprites na tela
    all_sprites.draw(screen)
    

    #Atualiza o jogo
    pygame.display.update()
