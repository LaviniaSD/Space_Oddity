"""Arquivo com os elementos do jogo.
"""

#Importando bibliotecas necessárias
import pygame
import random
import time
import os
import setup as st
from abc import ABC, abstractmethod
from threading import Timer 


#Classe para o hitbox do jogador
class Hitbox(pygame.sprite.Sprite):
    """Sprite para o hitbox do jogador. Usado na detecção de tiros."""
    
    def __init__(self, entity):
        """Método construtor da classe hitbox"""
            
        pygame.sprite.Sprite.__init__(self)
        
        #Carrega a imagem
        self.__hitbox = pygame.image.load(os.path.join(st.img_folder, "hitbox.png"))\
            .convert_alpha()
        self.__temp = pygame.image.load(os.path.join(st.img_folder, "temp.png")).convert_alpha()
        
        #Instância as propriedades do hitbox.
        self.image = self.__hitbox
        self.rect = self.image.get_rect()
        self.__entity = entity
    
    def position(self, entity):
        """Este método usa a instância do sprite do jogador para se reposicionar.
        

        Parameters
        ----------
        entity : TYPE
            Variável referente ao jogador.

        Returns
        -------
        None.

        """
        
        #Mude o centro do hitbox .
        self.rect.center = entity.rect.center
        
    def set_visible(self, visible):
        """Este método usa o parâmetro visível (booleano), para definir a imagem de
        visível para invisível.
        

        Parameters
        ----------
        visible : boll
            True caso o hitbox esteja visível.

        Returns
        -------
        None.

        """
        
        #Muda a imagem dependendo da visibilidade
        if visible:
            self.image = self.__hitbox
        else:
            self.image = self.__temp

    def update(self):
        """Este sprite atualiza a posição do sprite hitbox. usando um
        método."""
        
        #Posicione o hitbox no centro do sprite do jogador.
        self.position(self.__entity)

   
#Cria a classe para as balas
class Bullet(pygame.sprite.Sprite):
    
    #Características iniciais da classe quando ela é iniciada
    def __init__(self,x,y):
        """Função inicial para a bala
        

        Parameters
        ----------
        x : int
            Coordenada do surgimento da bala no eixo x.
        y : int
            Coordenada do surgimento da bala no eixo y.

        Returns
        -------
        None.

        """
        
        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(st.img_folder,"bullet.png")).convert()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.image.set_colorkey((0,0,0))
        
        #Orienta a posição inicial da bala 
        self.rect = self.image.get_rect()       
        self.rect.bottom = y
        self.rect.centerx = x
        
        #Define a velocidade da bala
        self.speed = (0,0)

    #Retorna a posição da bala   
    @property
    def position(self):
        return self._rect.x,self._rect.y

    @property
    #Retorna a velocidade da bala     
    def speed(self):
        return self._speed
    
    @speed.setter
    #Muda a velocidade da bala
    def speed(self,new_speed):
        self._speed = new_speed
    
    
    #Muda a posição da bala
    def update(self):
        """Muda a posição da bala."""
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        
        #Caso a bala ultrapasse as bordas, a elimine.
        if self.rect.bottom < 0:
            self.kill()
        elif self.rect.bottom > st.HEIGHT:
            self.kill()


#Cria a classe para o jogador
class Player(pygame.sprite.Sprite):
    #Características iniciais da classe quando ela é iniciada
    def __init__(self):

        #Adiciona uma imagem
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(st.img_folder,"ship.png")).convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image.set_colorkey((0,0,0))

        #Criar hitbox de jogador 
        self.hitbox = None

        #Cria a reta e o círculo para posicionar a classe
        self.rect = self.image.get_rect()
        self.radius = 32
        
        #Orienta a posição inicial do jogador
        self.rect.centerx = st.WIDTH/2
        self.rect.bottom = st.HEIGHT -10
        
        # Define a velocidade do jogador
        self.speed = (0,0)
        
        self.focus = False

        #Define a vida do jogador 
        self.life = 1

        #Define o score do jogador
        self.score = 0
        
        #Define o intervalo entre tiros
        self.shoot_delay = 200
        
        #Define o tempo desde o último tiro
        self.last_shot = pygame.time.get_ticks()
        
        #Define o poder(quantidade de tiros)
        self.power = 1
        
        #Define quando o poder iniciou 
        self.power_time = pygame.time.get_ticks()
        
    #Retorna a posição do jogador    
    @property
    def position(self):
        return self._rect.x,self._rect.y
    
    #Retorna a velocidade do jogador    
    @property
    def speed(self):
        return self._speed
    
    #Retorna a vida do jogador
    @property
    def life(self):
        return self._life
    
    #Retorna o score do jogador 
    @property
    def score(self):
        return self._score
    
    #Retorna o shoot_delay do jogador 
    @property
    def shoot_delay(self):
        return self._shoot_delay
    
    #Retorna o poder do jogador 
    @property
    def power(self):
        return self._power
    
    #Retorna o power_time do jogador 
    @property
    def power_time(self):
        return self._power_time
    
    #Altera a propriedade speed
    @speed.setter
    def speed(self,new_speed):
        self._speed = new_speed
    
    #Altera a propriedade life
    @life.setter
    def life(self,new_life):
        self._life = new_life

    #Altera a propriedade score
    @score.setter
    def score(self,new_score):
        self._score = new_score
        
    #Altera a propriedade shoot_delay
    @shoot_delay.setter
    def shoot_delay(self,new_shoot_delay):
        self._shoot_delay = new_shoot_delay
        
    #Altera a propriedade power
    @power.setter
    def power(self,new_power):
        self._power = new_power
    
    #Altera a propriedade power_time
    @power_time.setter
    def power_time(self,new_power_time):
        self._power_time = new_power_time
        
    #Atualiza a nave de acordo com os comandos do jogador   
    def update(self):
        """Muda a posição da nave do jogador"""
        
        #Caso o jogador esteja com um poder há mais de 10 segundos, retire esse poder.
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 10000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        
        #Seta a velocidade como 0
        self.speed = (0,0)  
        
        #Reage a interações do usuário
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
                self.speed = (-4,4)
            elif keystate[pygame.K_UP] or keystate[pygame.K_w]:
                self.speed = (-4,-4)
            else:
                self.speed = (-8,self.speed[1])
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
                self.speed = (4,4)
            elif keystate[pygame.K_UP] or keystate[pygame.K_w]:
                self.speed = (4,-4)
            else:
                self.speed = (8,self.speed[1])
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speed = (self.speed[0],-8)
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speed = (self.speed[0],8)
        if keystate[pygame.K_SPACE] or keystate[pygame.K_z]:
            self.shoot()
            
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        
        #Não deixa que o jogador ultrapasse os limites da tela
        if self.rect.right > st.WIDTH:
            self.rect.right = st.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > st.HEIGHT:
            self.rect.bottom = st.HEIGHT

    
    #Define a função de atirar
    def shoot(self):
        """Função que seta como é o tiro do jogador """
        
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            #Muda o horário do último tiro
            self.last_shot = now
            
            if self.power == 1:
                #Reproduz som de tiro
                shoot_sound = pygame.mixer.Sound(os.path.join(st.sound_folder,"Laser_Shoot4.wav"))
                shoot_sound.set_volume(0.5)
                shoot_sound.play()
                
                #Dispara a balas
                bullet = Bullet(self.rect.centerx,self.rect.top)
                bullet.speed = (0,-15)
                st.all_sprites.add(bullet)
                st.bullets.add(bullet)
            if self.power >= 2:
                #Reproduz som de tiro
                shoot_sound = pygame.mixer.Sound(os.path.join(st.sound_folder,"Laser_Shoot4.wav"))
                shoot_sound.set_volume(0.5)
                shoot_sound.play()
                
                #Dispara a balas
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right,self.rect.centery)
                bullet1.speed= (0,-15)
                bullet2.speed= (0,-15)
                st.all_sprites.add(bullet1)
                st.bullets.add(bullet1)
                st.all_sprites.add(bullet2)
                st.bullets.add(bullet2)
        
    #Altera o poder do jogador e marca o início desse poder
    def gain_powerup(self):
        """Altera o poder do jogador e marca o início desse poder """
        self.power += 1
        self.power_time = pygame.time.get_ticks()
            


#Classe abstrata para inimigos
class Enemy(pygame.sprite.Sprite, ABC):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        #Define a imagem 
        self.image = image        

        #Cria a reta e o círculo para posicionar a classe
        self.rect = self.image.get_rect()
        self.radius = 0        
        
        #Define uma velocidade aleatória 
        self.speed = 0   
        
        #Define o score 
        self.score = 0

    @abstractmethod
    def position(self):
        pass

    @abstractmethod
    def speed(self):
        pass

    @abstractmethod
    def score(self):
        pass

    @abstractmethod
    def update(self):
        pass

        
#Cria a classe para os asteroides 
class Asteroid(Enemy):
    #Características iniciais da classe quando ela é iniciada
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        asteroids_list = ["asteroid.png",
                            "asteroid2.png",
                            "asteroid3.png"]
        asteroids_images = []
                            
        for asteroid in asteroids_list:
            if asteroid == "asteroid.png":
                sprite = pygame.image.load(
                    os.path.join(st.img_folder,asteroid)
                    ).convert()
                sprite = pygame.transform.scale(sprite, (120, 120))

                asteroids_images.append(sprite)
            elif asteroid == "asteroid2.png":
                sprite = pygame.image.load(
                    os.path.join(st.img_folder,asteroid)
                    ).convert()
                sprite = pygame.transform.scale(sprite, (60, 60))

                asteroids_images.append(sprite)
            else:
                sprite = pygame.image.load(
                    os.path.join(st.img_folder,asteroid)
                    ).convert()
                sprite = pygame.transform.scale(sprite, (30, 30))

                asteroids_images.append(sprite)
        
        #Define a imagem do asteroide  
        self.image = random.choice(asteroids_images)
        self.image.set_colorkey((0,0,0))

        self.rect = self.image.get_rect()
        
        self.radius = int(self.rect.width * 0.90 / 2)
                
        #Orienta a posição inicial do asteroide
        self.rect.x = random.randrange(st.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-40,-15)
        
        #Define uma velocidade aleatória para cada asteroide
        self.speed = (random.randrange(-5,5),random.randrange(1,10))
    
        #Define o score do asteroide (quanto ele vale).
        self.score = 100-self.radius
        
    #Retorna a posição do asteroide    
    @property
    def position(self):
        return self._rect.x,self._rect.y
    
    #Retorna a velocidade do asteroide    
    @property
    def speed(self):
        return self._speed

    #Retorna o score que o asteroide dará ao jogador quando destruído
    @property
    def score(self):
        return self._score
    
    #Muda o score do asteroide
    @score.setter
    def score(self,new_score):
        self._score = new_score
    
    #Altera a propriedade speed
    @speed.setter
    def speed(self,new_speed):
        self._speed = new_speed
            
    #Muda a posição do asteroide
    def update(self):
        """Altera a posição do asteroide"""
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        
        #Caso o asteroide ultrapasse as bordas, crie outro
        if self.rect.top > st.HEIGHT + 10 or self.rect.left < -10 or self.rect.right > st.WIDTH + 10:
            self.speed = (random.randrange(-5,5),random.randrange(1,10))
            self.rect.x = random.randrange(st.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
   
    
#Crie uma classe para explosões
class Explosion(pygame.sprite.Sprite):
    
    def __init__(self,center,size):
        """Construtor da classe Explosion
        

        Parameters
        ----------
        center : tuple
            Centro da explosão.
        size : str
            Tamanho da explosão.

        Returns
        -------
        None.

        """
        
        #Crie dois tipos de explosões: as maiores e as menores
        pygame.sprite.Sprite.__init__(self)
        explosion_animation = {}
        explosion_animation["large"] = []
        explosion_animation["small"] = []

        for i in range (6):
            filename = f"explosion{i}.png"
            image = pygame.image.load(os.path.join(st.img_folder, filename)).convert()
            image.set_colorkey((0,0,0))
            
            large_image = pygame.transform.scale(image,(80,80))
            explosion_animation["large"].append(large_image)
            
            small_image = pygame.transform.scale(image,(32,32))
            explosion_animation["small"].append(small_image)
        
        #Define o tamanho da explosão (grande ou pequena)
        self.size = size
        
        #Define a animação a ser utilizada
        self.explosion_animation = explosion_animation[self.size]
        
        #Define a primeira imagem da animação
        self.image = self.explosion_animation[0]
        
        #Define a posição da explosão
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        #Define qual frame aparecerá na tela
        self.frame = 0
        
        # Define a última vez que houve mudança de frame
        self.last_update = pygame.time.get_ticks()
        
        #Define a velocidade que os frames aparecem na explosão
        self.frame_rate = 50
        
    #Retorna a posição da explosão    
    @property
    def position(self):
        return self._rect.center
    
    #Retorna o tamanho da explosão   
    @property
    def size(self):
        return self._size
    
    #Retorna o último update da explosão   
    @property
    def last_update(self):
        return self._last_update
    
    #Retorna a taxa de frames por segundo da explosão   
    @property
    def frame_rate(self):
        return self._frame_rate
    
    #Muda o tamanho da explosão
    @size.setter
    def size(self,new_size):
        self._size = new_size
    
    #Muda o last_update
    @last_update.setter
    def last_update(self,new_last_update):
        self._last_update = new_last_update

    #Muda o frame rate
    @frame_rate.setter
    def frame_rate(self,new_frame_rate):
        self._frame_rate = new_frame_rate
    
    #Método para criar a animação    
    def update(self):
        """Cria a animação da explosão """
    
        now = pygame.time.get_ticks()
        
        #Caso o tempo decorrido entre o último frame e agora seja maior que a velocidade dos frames,
        # atualize o frame exibido
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explosion_animation):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explosion_animation[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
    
    #Método para criar som de explosão  
    def explosion_sound(self):
        """Cria o som da explosão """
        explosion_sound = pygame.mixer.Sound(
            os.path.join(st.sound_folder, "Explosion7.wav"))
        explosion_sound.play()
   

#Cria a classe para as naves inimigas             
class EnemyShip(Enemy):    
    #Características iniciais da classe quando ela é iniciada
    def __init__(self):
        
        #Adiciona uma imagem à nave inimiga
        self.image = pygame.image.load(os.path.join(st.img_folder,"enemy_ship.png")).convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image.set_colorkey((255,255,255))

        super().__init__(self.image)
                
        #Cria a reta e o círculo para posicionar a classe
        self.rect = self.image.get_rect()
        self.radius = 28
        
        #Orienta a posição inicial da nave inimiga
        self.rect.x = random.randrange(st.WIDTH - self.rect.width)
        self.rect.y = random.randrange(int(st.HEIGHT/8),(int(st.HEIGHT/8))+30)
        
        #Define a velocidade da nave inimiga
        self.speed = (0,0)

        #Define o score que a nave inimiga dá ao jogador quando destruida
        self.score = 100
        
        #Define o intervalo entre tiros
        self.shoot_delay = 50
        
        #Define o tempo desde o último tiro
        self.last_shot = pygame.time.get_ticks()

    #Retorna a posição da nave inimiga    
    @property
    def position(self):
        return self._rect.x,self._rect.y
    
    #Retorna a velocidade da nave inimiga   
    @property
    def speed(self):
        return self._speed
    
    #Retorna o score da nave inimiga 
    @property
    def score(self):
        return self._score
    
    #Retorna o intervalo de tiro da nave inimiga 
    @property
    def shoot_delay(self):
        return self._shoot_delay
    
    #Retorna o último tiro da nave inimiga 
    @property
    def last_shot(self):
        return self._last_shot
    
    #Altera a propriedade speed
    @speed.setter
    def speed(self,new_speed):
        self._speed = new_speed
    
    #Altera a propriedade score
    @score.setter
    def score(self,new_score):
        self._score = new_score
        
    #Altera a propriedade shoot_delay
    @shoot_delay.setter
    def shoot_delay(self,new_shoot_delay):
        self._shoot_delay = new_shoot_delay
        
    #Altera a propriedade last_shot
    @last_shot.setter
    def last_shot(self,new_last_shot):
        self._last_shot = new_last_shot
    
    #Permite que a nave inimiga atire
    def shoot(self,speed_x,speed_y):
        """Seta o tiro da nave inimiga
        

        Parameters
        ----------
        speed_x : int
            Velocidade no eixo x.
        speed_y : int
            Velocidade no eixo y.

        Returns
        -------
        None.

        """
        shoot_sound = pygame.mixer.Sound(os.path.join(st.sound_folder,"Laser_Shoot4.wav"))
        shoot_sound.set_volume(0.3)
        bullet = Bullet(self.rect.centerx,self.rect.top)
        bullet.speed = (speed_x, speed_y) 
        st.all_sprites.add(bullet)
        st.enemies_bullets.add(bullet)
        shoot_sound.play()
        
    def enemy_shoots(self):
        """"Método para criar a sequência de tiros do inimigo"""
        for i in range (5):
            x_speed= random.randint(-10,10)
            y_speed= random.randint(10,10)
            self.shoot(x_speed, y_speed)
            time.sleep(0.001)
           
    #Permite que a nave inimiga se movimente   
    def update(self):
        """Movimenta a classe inimiga """
        self.speed = (self.speed[0],-1)
        self.rect.y += self.speed[1]


#Classe abstrata para os itens bônus
class Item(pygame.sprite.Sprite, ABC):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        # Defina a imagem
        self.image = image
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey((0,0,0))
        
        #Define o tipo
        self.type = None

        #Cria a reta para posicionar a classe
        self.rect = self.image.get_rect()
        
        #Orienta a posição inicial do bônus
        self.rect.x = random.randrange(st.WIDTH - self.rect.width)
        self.rect.y = random.randrange(st.HEIGHT - self.rect.height)

        # Desaparece após 3 segundos na tela
        Timer(3, self.disappear).start()

    @abstractmethod
    def disappear(self):
        """Elimina o bônus após 3 segundos na tela"""
        self.kill()
    
    @abstractmethod
    def collect_sound(self):
        collect_sound = pygame.mixer.Sound(os.path.join(st.sound_folder,"Powerup.wav"))
        collect_sound.set_volume(1)
        collect_sound.play()

#Classe para o bônus em forma de estrela
class StarShooter(Item):
    
    #Construtor da classe StarShooter
    def __init__(self):
        image = pygame.image.load(os.path.join(st.img_folder,"star.png")).convert()

        super().__init__(image)

        self.type = "star"
    
    #Define o disaparecimento do bônus
    def disappear(self):
        """Elimina o bônus após 3 segundos na tela"""
        self.kill()
        
    #Define o som de coleta do bônus
    def collect_sound(self):
        """Reproduz som de coleta do bônus"""
        collect_sound = pygame.mixer.Sound(os.path.join(st.sound_folder,"Powerup.wav"))
        collect_sound.set_volume(1)
        collect_sound.play()


#Classe para o bônus de escudo
class Shield(Item):
    #Construtor da classe Shield
    def __init__(self):

        image = pygame.image.load(os.path.join(st.img_folder,"shield.png")).convert()

        super().__init__(image)

        self.type = "shield"

    #Define o disaparecimento do bônus
    def disappear(self):
        """Elimina o bônus após 3 segundos na tela"""
        self.kill()
        
    #Define o som de coleta do bônus
    def collect_sound(self):
        """Reproduz som de coleta do bônus"""
        collect_sound = pygame.mixer.Sound(os.path.join(st.sound_folder,"Powerup.wav"))
        collect_sound.set_volume(1)
        collect_sound.play()