#Importando bibliotecas necessárias
import pygame
import random
import time
import os
import setup as st
from abc import ABC, abstractmethod
from threading import Timer 

# import space_oddity as so

#Hitbox
#Bullet
#Player
#Enemy
#Asteroid
#Explosion
#Enemy_ship
#Power

class Hitbox(pygame.sprite.Sprite):
    """The sprite for the player hit box sprite. Used in bullet detection."""
    
    def __init__(self, entity):
        """This method initializes the sprite using the player sprite."""
            
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Image loading
        self.__hitbox = pygame.image.load(os.path.join(st.img_folder, "hitbox.png"))\
            .convert_alpha()
        self.__temp = pygame.image.load(os.path.join(st.img_folder, "temp.png")).convert_alpha()
        
        #Instance value setting.
        self.image = self.__hitbox
        self.rect = self.image.get_rect()
        self.__entity = entity
    
    def position(self, entity):
        """This method uses the player sprite instance to reposition itself."""
        
        #Mutate self center.
        self.rect.center = entity.rect.center
        
    def set_visible(self, visible):
        """This method uses the visible parameter (boolean), to set image from
        visible to invisible."""
        
        #Change image depending on if visible
        if visible:
            self.image = self.__hitbox
        else:
            self.image = self.__temp

    def update(self):
        """This sprite updates the position of the hitbox sprite. using a
        method."""
        
        #Position hit box in the center of the player sprite.
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
        self.x_speed = 0
        self.y_speed = 0
        
    
    #Retorna a posição da bala   
    #@property
    def get_position(self):
        return self.rect.x,self.rect.y
    
    #@property
    #Retorna a velocidade da bala     
    def speed(self):
        return self.x_speed,self.y_speed
    
    #@speed.setter
    #Muda a velocidade da bala
    def set_speed(self,new_speed_x,new_speed_y):
        self.x_speed = new_speed_x
        self.y_speed = new_speed_y
    
    
    #Muda a posição da bala
    def update(self):
        self.rect.x += self.x_speed 
        self.rect.y += self.y_speed 
        
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
        self.x_speed = 0
        self.y_speed = 0

        
        self.focus = False

        #Define se o jogador está vivo
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
    #@property
    def get_position(self):
        return self.rect.x,self.rect.y
    
    #Retorna a velocidade do jogador    
    #@property
    def speed(self):
        return self.x_speed,self.y_speed
    
    #Retorna se o jogador está vivo
    #@property
    def get_life(self):
        return self.life
    
    #Retorna o score do jogador 
    #@property
    def get_score(self):
        return self.score
    
    #Retorna o score do jogador 
    #@property
    def get_shoot_delay(self):
        return self.shoot_delay
    
    #Retorna o score do jogador 
    #@property
    def get_power(self):
        return self.power
    
    #Retorna o score do jogador 
    #@property
    def get_power_time(self):
        return self.power_time
    
    #Altera a propriedade life
    #@speed.setter
    def set_speed(self,new_speed_x,new_speed_y):
        self.x_speed = new_speed_x
        self.x_speed = new_speed_y
    
    #Altera a propriedade life
    #@get_life.setter
    def set_life(self,new_life):
        self.life = new_life

    #Altera a propriedade score
    #@get_score.setter
    def set_score(self,new_score):
        self.score = new_score
        
    #Atualiza a nave de acordo com os comandos do jogador   
    def update(self):
        
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 10000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        
        #Seta a velocidade como 0
        self.x_speed = 0
        self.y_speed = 0
        
        #Reage a interações do usuário
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
                self.x_speed = -4
                self.y_speed = 4
            elif keystate[pygame.K_UP] or keystate[pygame.K_w]:
                self.x_speed = -4
                self.y_speed = -4
            else:
                self.x_speed = -8
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
                self.x_speed = 4
                self.y_speed = 4
            elif keystate[pygame.K_UP] or keystate[pygame.K_w]:
                self.x_speed = 4
                self.y_speed = -4
            else:
                self.x_speed = 8
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.y_speed = -8
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.y_speed = 8
        if keystate[pygame.K_SPACE] or keystate[pygame.K_z]:
            self.shoot()
            
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        
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
                bullet.set_speed(0,-15)
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
                bullet1.set_speed(0,-15)
                bullet2.set_speed(0,-15)
                st.all_sprites.add(bullet1)
                st.bullets.add(bullet1)
                st.all_sprites.add(bullet2)
                st.bullets.add(bullet2)
        
    
    def gain_powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
            

class Enemy(pygame.sprite.Sprite, ABC):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def speed(self):
        pass

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def get_is_alive(self):
        pass

    @abstractmethod
    def get_score(self):
        pass

    @abstractmethod
    def set_is_alive(self):
        pass

    @abstractmethod
    def update(self):
        pass

        
#Cria a classe para os asteroides 
class Asteroid(Enemy):
    #Características iniciais da classe quando ela é iniciada
    def __init__(self):
        
        #Cria opções de asteroides
        super().__init__()

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
        #self.image = pygame.transform.scale2x(self.image)
        self.image.set_colorkey((0,0,0))
        
        #Define a hitbox 
        self.hitbox = None

        #Cria a reta e o círculo para posicionar a classe
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.90 / 2)
        
        
        #Orienta a posição inicial do asteroide
        self.rect.x = random.randrange(st.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-40,-15)
        
        #Define uma velocidade aleatória para cada asteroide
        self.x_speed = random.randrange(-5,5)
        self.y_speed = random.randrange(1,10)
    
        #Define se o jogador está vivo
        self.is_alive = True
        
        #Define o score do jogador
        self.score = 100-self.radius
        
   
    #Retorna a posição do asteroide    
    #@property
    def get_position(self):
        return self.rect.x,self.rect.y
    

    #Retorna a velocidade do asteroide    
    #@property
    def speed(self):
        return self.x_speed,self.y_speed
    
    #Retorna se o asteroide está "vivo"
    #@property
    def get_is_alive(self):
        return self.is_alive

    #Retorna o score que o asteroide dará ao jogador quando destruído
    #@property
    def get_score(self):
        return self.score
    
    #@get_score.setter
    def set_score(self,new_score):
        self.score = new_score
    
    #Altera a propriedade is_alive
    #@get_is_alive.setter
    def set_is_alive(self,life_status):
        self.is_alive = life_status
        
        if self.is_alive == False:
            self.kill()
        
    #Muda a posição do asteroide
    def update(self):
        self.rect.x += self.x_speed 
        self.rect.y += self.y_speed 
        
        #Caso o asteroide ultrapasse as bordas, crie outro
        if self.rect.top > st.HEIGHT + 10 or self.rect.left < -10 or self.rect.right > st.WIDTH + 10:
            self.x_speed = random.randrange(-5,5)
            self.y_speed = random.randrange(1,10)
            self.rect.x = random.randrange(st.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.y_speed = random.randrange(1,10)
   
    
#Crie uma classe para explosões
class Explosion(pygame.sprite.Sprite):
    
    
    def __init__(self,center,size):
        
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
    #@property
    def get_position(self):
        return self.rect.center
    
    #Retorna o tamanho da explosão   
    #@property
    def get_size(self):
        return self.size
    
    #Retorna o último update da explosão   
    #@property
    def get_last_update(self):
        return self.last_update
    
    #Retorna a taxa de frames por segundo da explosão   
    #@property
    def get_frame_rate(self):
        return self.frame_rate

    #Método para criar a animação    
    def update(self):
    
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
        explosion_sound = pygame.mixer.Sound(
            os.path.join(st.sound_folder, "Explosion7.wav"))
        explosion_sound.play()
   


#Cria a classe para as naves inimigas             
class Enemy_ship(Enemy):    
    #Características iniciais da classe quando ela é iniciada
    def __init__(self):
        
        #Adiciona uma imagem à nave inimiga
        super().__init__()

        self.image = pygame.image.load(os.path.join(st.img_folder,"enemy_ship.png")).convert()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.image.set_colorkey((255,255,255))
        
        
        #Cria a reta e o círculo para posicionar a classe
        self.rect = self.image.get_rect()
        self.radius = 28
        
        #Orienta a posição inicial da nave inimiga
        self.rect.x = random.randrange(st.WIDTH - self.rect.width)
        self.rect.y = random.randrange(int(st.HEIGHT/8),(int(st.HEIGHT/8))+30)
        
        #Define a velocidade da nave inimiga
        self.x_speed = 0
        self.y_speed = 0
        
        #Define se a nave inimiga está "viva"
        self.is_alive = True
        
        #Define o score que a nave inimiga dá ao jogador quando destruida
        self.score = 100
        
        #Define o intervalo entre tiros
        self.shoot_delay = 50
        
        #Define o tempo desde o último tiro
        self.last_shot = pygame.time.get_ticks()

    #Retorna a posição da nave inimiga    
    #@property
    def get_position(self):
        return self.rect.x,self.rect.y
    

    #Retorna a velocidade da nave inimiga   
    #@property
    def speed(self):
        return self.x_speed,self.y_speed
    

    #Retorna se a nave inimiga está viva
    #@property
    def get_is_alive(self):
        return self.is_alive
    

    #Retorna o score da nave inimiga 
    #@property
    def get_score(self):
        return self.score
    
    #Retorna o intervalo de tiro da nave inimiga 
    #@property
    def get_shoot_delay(self):
        return self.shoot_delay
    
    #Retorna o último tiro da nave inimiga 
    #@property
    def get_last_shot(self):
        return self.last_shot
    

    #Altera a propriedade is_alive
    #@set.get_is_alive
    def set_is_alive(self,life_status):
        self.is_alive = life_status
        
        #Caso o asteroide ultrapasse as bordas, crie outro
        if self.rect.bottom < 0:
            self.kill()

        if self.is_alive == False:
            self.kill()
            
    #Altera a propriedade score
    #@set.get_score
    def set_score(self,new_score):
        self.score = new_score
        
    #Permite que a nave inimiga atire
    def shoot(self,speed_x,speed_y):
        shoot_sound = pygame.mixer.Sound(os.path.join(st.sound_folder,"Laser_Shoot4.wav"))
        shoot_sound.set_volume(0.5)
        bullet = Bullet(self.rect.centerx,self.rect.top)
        bullet.set_speed(speed_x, speed_y) 
        st.all_sprites.add(bullet)
        st.enemies_bullets.add(bullet)
        shoot_sound.play()
        
    def enemy_shoots(self):
        for i in range (5):
            x_speed= random.randint(-10,10)
            y_speed= random.randint(10,10)
            self.shoot(x_speed, y_speed)
            time.sleep(0.001)
           
    #Permite que a nave inimiga se movimente   
    def update(self):
        self.y_speed = -1
        self.rect.y += self.y_speed

class Item(pygame.sprite.Sprite, ABC):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)

        # Defina a imagem
        self.image = image
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.image.set_colorkey((0,0,0))
        
        #Define a hitbox 
        self.hitbox = None

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
        self.kill()

class StarShooter(Item):
    def __init__(self):

        image = pygame.image.load(os.path.join(st.img_folder,"star.png")).convert()

        super().__init__(image)

        self.type = "star"

    def disappear(self):
        self.kill()

class Shield(Item):
    def __init__(self):

        image = pygame.image.load(os.path.join(st.img_folder,"shield.png")).convert()

        super().__init__(image)

        self.type = "shield"

    def disappear(self):
        self.kill()


