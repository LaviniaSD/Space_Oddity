"""Esse módulo contém a classe Game e as funcionalidades para a execução do jogo.
"""

# Importe as bibliotecas necessárias
import json
import math
import os
import pygame
import random
import sys

import gaming_elements as ge
import interface as it
import setup as st

# Inicializando o pygame e o mixer de sons
pygame.init()
pygame.mixer.init()

# Crie a tela
screen = pygame.display.set_mode((st.WIDTH, st.HEIGHT), pygame.FULLSCREEN)

# Crie o nome do jogo (exibido no superior da janela)
pygame.display.set_caption("Space Oddity")

# Relógio para controlar o tempo das ações no jogo
clock = pygame.time.Clock()

# Define a classe principal do jogo, responsável pelas telas e ações da aplicação
class Game():

    # Som de st.background
    pygame.mixer.music.load(os.path.join(st.sound_folder, "som1.mp3"))
    pygame.mixer.music.set_volume(0.2)

    # Crie um grupo para todos os sprites
    st.all_sprites = pygame.sprite.Group()

    # Crie um grupo para os asteroides
    st.asteroids = pygame.sprite.Group()

    # Crie um grupo para as naves inimigas
    st.enemy_ships = pygame.sprite.Group()

    # Crie um grupo para as balas
    st.bullets = pygame.sprite.Group()

    # Crie um grupo para as balas dos inimigos
    st.enemies_bullets = pygame.sprite.Group()

    # Crie um grupo para os bônus
    st.powers = pygame.sprite.Group()
    
    # Define o método construtor da classe
    def __init__(self):

        self.in_menu = True
        self.pause = False
        self.restart = False
        self.mainloop("menu")

    # Define o método que controla o loop principal do jogo
    def mainloop(self, scene):
        """Define o loop do jogo

        Parameters
        ----------
        scene : str
            Indica qual parte do jogo deve ser visualizada pelo usuário.

        Returns
        -------
        None.

        """
        self.scene = scene

        while True:
            if scene == "menu":
                scene = self.menu()
            elif scene == "game":
                scene =  self.run_game()

    # Crie um método para o menu principal
    def menu(self):
        """Exibe o menu do jogo
        

        Returns
        -------
        str
            Variável que será lida pela função 'mainloop', indicando a próxima tela a ser exibida, após uma interação do usuário.

        """
        
        self.load_background("space_menu.jpg")

        # Define referências de posições para os botões, ao centro da tela
        x_centered = st.WIDTH / 2
        y_centered = st.HEIGHT / 2

        # Instancia os botões do menu
        play_button = it.Button(text="PLAY", x=x_centered, y=y_centered+30, width=200, height=30, font_size=25)
        scores_button = it.Button(text="SCORES", x=x_centered, y=y_centered+65, width=200, height=30, font_size=25)
        exit_button = it.Button(text="EXIT", x=x_centered, y=y_centered+100, width=200, height=30, font_size=25)


        self.in_menu = True

        # Inicia um loop para o menu
        while self.in_menu:

            # Carrega a imagem de fundo do menu
            # screen.fill(st.WHITE)
            screen.blit(st.background, (0, 0))

            # Imprime o nome do jogo na tela
            self.draw_text(screen, "Space Oddity", 130, x_centered, y_centered-150, st.WHITE)

            # Desenha os botões na tela
            play_button.draw(screen, (0,0,0))
            scores_button.draw(screen, (0,0,0))
            exit_button.draw(screen, (0,0,0))

            # Verifica a ocorrência de eventos
            for event in pygame.event.get():
                # Recolhe a posição atual do mouse
                pos = pygame.mouse.get_pos()

                # Caso o usuário feche a janela
                if event.type == pygame.QUIT:
                    self.in_menu = False
                    self.quit_game()

                # Caso o usuário clique com o botão esquerdo do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Caso o usuário clique no botão de play
                    if play_button.is_over(pos):
                        self.in_menu = False
                        return "game"
        
                    # Caso o usuário clique no botão de scores
                    elif scores_button.is_over(pos):
                        # changescn("scores")
                        print("scores")
                    
                    # Caso o usuário clique no botão de sair
                    elif exit_button.is_over(pos):
                        self.in_menu = False
                        self.quit_game()

                    else:
                        pass
                        
            # Atualiza os conteúdos da tela
            pygame.display.flip()

    def run_game(self):
        """Método que executa o loop principal do jogo
        

        Returns
        -------
        str
            Variável que será lida pela função 'mainloop', indicando a próxima tela a ser exibida, após o fim da jogatina.

        """
        
        self.load_background("space_pattern.jpg")
        
        #Crie uma variável para o deslizamento da tela
        scrolling = 0
        
        #Crie uma variável para a quantidade de painés necessários no deslizamento da tela
        panels = math.ceil(st.HEIGHT/st.background_height)+2
        
        # Atribui a classe player a uma variável
        player = ge.Player()
        player.hitbox = ge.Hitbox(player)
        
        # Adiciona player aos grupo de sprites
        st.all_sprites.add(player, player.hitbox)
        
        # testButton = ge.Button(color=ge.WHITE, x=200, y=200, width=200, height=200, size=20, text="ABCASKLDASKLDNASD")
        
        #Cria uma marcação de tempo inicial para spawning
        start_asteroids = pygame.time.get_ticks()
        start_enemies_ships = pygame.time.get_ticks()
        
        #Reproduza a música de fundo infinitamente
        pygame.mixer.music.play(loops=-1)
        
        #Estabeleça o nível antes do jogo iniciar
        level = 1
        
        start_level_time = pygame.time.get_ticks()
        
        # Loop para o jogo
        running = True
        
        while running:
            
            # Faça o jogo funcionar com a quantidade de frames por segundo estabelecidas
            clock.tick(st.FPS)
            
            #Recebe a quantidade de tempo decorrida desde o início do jogo
            level_delay = pygame.time.get_ticks()
            
            #Adicione um nível de 5 em 5 segundos
            if level_delay - start_level_time > 5000:
                start_level_time = pygame.time.get_ticks()
                level += 1
            
            # Faça o jogo reagir a eventos externos
            for event in pygame.event.get():
                # Permita que o usuário saia do jogo
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause, running = self.paused()

            # Caso a instrução seja de retornar ao menu, ele encerra o loop do jogo imediatamente
            if not running:
                break

            # Atualiza os sprites
            st.all_sprites.update()
            
            
            # Gera bônus aleatoriamente na tela
            if random.random() < 0.005:
                star_power = ge.StarShooter()
                shield_power = ge.Shield()
                power_up = random.choice([star_power, shield_power])
                st.powers.add(power_up)
                st.all_sprites.add(power_up)

                
            #Spawna asteroides em intervalos de 3 ou menos segundos (dependendo do nível)
            now = pygame.time.get_ticks()
            if now - start_asteroids > (3000 - 10*level) :
                start_asteroids = now
                self.spawn_asteroids(st.asteroids,st.all_sprites)
        
            #spawna naves inimigas em intervalos de 4 ou menos segundos
            if now - start_enemies_ships > (4000 - 5*level):
                start_enemies_ships = now
                self.spawn_enemy_ships(st.enemy_ships,st.all_sprites)

            #Cria casos de colisão entre balas do jogador e asteroides
            bullet_hits_asteroid = pygame.sprite.groupcollide(st.asteroids, st.bullets, True, True)
            for hitted_asteroid in bullet_hits_asteroid:
                asteroid_score = hitted_asteroid.score
                player_old_score = player.score
                player.score = player_old_score+asteroid_score
                
                #Exibe explosão
                explosion = ge.Explosion(hitted_asteroid.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                # Adiciona um novo asteroide à tela
                new_asteroid = ge.Asteroid()
                st.all_sprites.add(new_asteroid)
                st.asteroids.add(new_asteroid)
                
            #Cria casos de colisão entre balas do jogador e naves inimigas    
            bullet_hits_enemy_ship = pygame.sprite.groupcollide(st.enemy_ships,st.bullets, True, True)
            for hitted_enemy_ship in bullet_hits_enemy_ship:
                enemy_score = hitted_enemy_ship.score
                player_old_score = player.score
                player.score = player_old_score+enemy_score 
                
                #Exibe explosão
                explosion = ge.Explosion(hitted_enemy_ship.rect.center,"small")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
            #Cria casos de colisão entre jogador e asteroides    
            asteroid_hits_player = pygame.sprite.spritecollide(
                player.hitbox, st.asteroids, True, pygame.sprite.collide_circle)
            if asteroid_hits_player:
                #Exibe explosão
                explosion = ge.Explosion(player.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                #Diminui a vida do jogador
                life = player.life
                damage = 1
                player.life = life - damage
                if player.life <= 0:
                    running =  self.player_dies(running, player.score) 
                
            #Cria casos de colisão entre balas do inimigo e o jogador    
            enemy_shoots_player = pygame.sprite.spritecollide(
                player.hitbox, st.enemies_bullets, True, pygame.sprite.collide_circle)

            if enemy_shoots_player:
                #Exibe explosão
                explosion = ge.Explosion(player.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                #Diminui a vida do jogador
                life = player.life
                damage = 1
                player.life = life - damage
                if player.life <= 0:
                    running = self.player_dies(running, player.score)  
                
            #Cria casos de colisão entre nave inimiga e o jogador    
            enemy_hits_player = pygame.sprite.spritecollide(
                player.hitbox, st.enemy_ships, False, pygame.sprite.collide_circle)

            if enemy_hits_player:
                #Exibe explosão
                explosion = ge.Explosion(player.rect.center,"large")
                explosion.explosion_sound()
                st.all_sprites.add(explosion) 
                
                #Diminui a vida do jogador
                life = player.life
                damage = 1
                
                #Encerra o loop se o jogador morre
                player.life = life - damage
                if player.life <= 0:
                    running =  self.player_dies(running, player.score) 

            # Caso a instrução seja de retornar ao menu, ele encerra o loop do jogo imediatamente
            if not running:
                break
            
            #Cria casos de colisão entre bônus e o jogador
            player_hits_bonus = pygame.sprite.spritecollide(player.hitbox, st.powers, True, pygame.sprite.collide_circle)
            
            for hitted_bonus in player_hits_bonus:
                hitted_bonus.collect_sound()
                #Caso seja um escudo, adicione vidas ao a jogador
                if hitted_bonus.type == "shield":
                    initial_lifes = player.life
                    player.life = initial_lifes + 1
                #Caso seja uma arma, adicione uma arma mais poderosa ao jogador
                if hitted_bonus.type == "star":
                    player.gain_powerup()
               
            
            # Exibe o hitbox caso o jogador pressione "Shift"
            keys_pressed = pygame.key.get_pressed()

            if keys_pressed[pygame.K_LSHIFT]:
                player.hitbox.set_visible(True)
            elif not keys_pressed[pygame.K_LSHIFT]:
                player.hitbox.set_visible(False)


            # Defina a imagem de fundo da tela
            screen.fill((0, 0, 0))

            #Mova o st.background
            for i in range(panels):
                screen.blit(st.background,(0,i*st.background_height+scrolling-st.background_height))
            
            scrolling += 5
            
            if abs(scrolling)>st.background_height:
                scrolling = 0
            

            # Desenha os sprites na tela
            st.all_sprites.draw(screen)

            # Insere o score na tela

            #Adiciona a pontuação no topo da tela
            self.draw_text(screen, f"Score: {str(player.score)}", 40, st.WIDTH/2, 15,(255,255,255))
            
            #Adiciona a quantidade de escudos na tela
            self.draw_text(screen, f"Shields: {str(player.life - 1)}", 25, st.WIDTH/2, 60,(255,255,255))
            
            # Atualize as imagens dos objetos quando ocorrerem mudanças
            pygame.display.flip()
            
            # Atualiza o jogo
            pygame.display.update()

        # Reinicia as variáveis que armazenam os sprites, evitando crosstalk de objetos entre as jogatinas
        self.reset_game()

        # Encerra o método "run_game()", instruindo a aplicação a se redicionar para o menu
        if self.restart:
            self.restart = False
            return "game"
        else:
            return "menu"

    # Método que pausa o jogo
    def paused(self):
        """Pausa o jogo
        

        Returns
        -------
        bool
            O estado de pause do jogo. Sempre retorna False, pois conclui o ciclo de pause.
        bool
            O estado de loop do jogo. Por padrão, retorna True, indicando que o jogo deve continuar. Se o usuário desejar ir pro menu, retorna False, quebrando o loop do jogo.

        """

        self.load_background("space_pause.png")

        # Altera o estado da variável que controla o loop de pause
        self.pause = True

        # Define referências de posições para os botões, ao centro da tela
        x_centered = st.WIDTH / 2
        y_centered = st.HEIGHT / 2

        # Cria os botões da tela de pause
        back_to_menu = it.Button(text="Sair e voltar ao menu principal", x=x_centered, y=y_centered+35, width=350, height=30, font_size=25)
        back_to_game = it.Button(text="Voltar ao jogo (ESC)", x=x_centered, y=y_centered+70, width=350, height=30, font_size=25)

        # Cria um loop que controla o estado de pause
        while self.pause:

            # Preenche a tela com a cor branca
            # screen.fill(st.WHITE)
            screen.blit(st.background, (0, 0))

            # Imprime o texto "PAUSE" na tela
            self.draw_text(screen, "Jogo pausado", 80, x_centered, y_centered-150, st.WHITE)

            # Desenha os botões da tela de pause
            back_to_menu.draw(screen, (0,0,0))
            back_to_game.draw(screen, (0,0,0))

            # Tratamento de eventos
            for event in pygame.event.get():
                # Recolhe a posição atual do mouse
                pos = pygame.mouse.get_pos()

                # Caso o usuário feche a janela
                if event.type == pygame.QUIT:
                    self.quit_game()

                # Caso o usuário aperte alguma tecla
                elif event.type == pygame.KEYDOWN:
                    # Caso o usuário aperte o botão ESC, ele deve sair da tela de pause e voltar ao jogo
                    if event.key == pygame.K_ESCAPE:
                        self.pause = False
                        self.load_background("space_pattern.jpg")
                        
                        return False, True

                # Caso o usuário clique com o botão esquerdo do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    # Caso o usuário clique no botão de voltar ao menu principal, o loop do jogo se encerra
                    if back_to_menu.is_over(pos):
                        self.pause = False
                        return False, False

                    # Caso o usuário clique no botão de voltar ao jogo
                    elif back_to_game.is_over(pos):
                        self.pause = False
                        self.load_background("space_pattern.jpg")

                        return False, True

                else:
                    pass

            # Atualiza a tela e o clock
            pygame.display.update()
            clock.tick(st.FPS)


    def load_score(self):
        score_filepath = os.path.join(st.save_folder, "scores.json")
        try:
            with open (score_filepath, "r") as file:
                dict_score = json.load(file)
            return dict_score
        except: 
            return None

    def save_score(self, player_name_box, player_score):
        dict_score = self.load_score()
        player_name = player_name_box.text

        if not player_name:
            return False

        if not dict_score:
            dict_score = dict()
    
        score_player = dict_score.get(player_name)

        if not score_player:
            dict_score[player_name] = player_score
        
        elif player_score > score_player:
            dict_score[player_name] = player_score

        else:
            pass

        try:
            score_filepath = os.path.join(st.save_folder, "scores.json")
            with open(score_filepath, "w") as out_file:
                json.dump(dict_score, out_file)
                out_file.close()
        except:
            pass
        
        else:
            return True


    # Método que exibe a tela de game over
    def game_over(self, player_score):

        
        """Cria a tela de game over
        

        Parameters
        ----------
        player_score : int
            Score do jogador.

        Returns
        -------
        bool
            O estado do game over, que é falsa, pois demarca o fim do ciclo de game over.

        """
        score_saved = False
        self.load_background("space_gameover.jpg")

        # Altera o estado da variável que controla o loop de game over
        self.over = True

        # Define referências de posições para os botões, ao centro da tela
        x_centered = st.WIDTH / 2
        y_centered = st.HEIGHT / 2

        # Inicializa os componentes da interface que estarao na tela de game over
        player_name_box = it.InputTextBox(x_centered, y_centered+100, 250, max_input_length=20)
        save_score_button = it.Button(text="Salvar score", x=x_centered, y=y_centered+140, width=250, height=30, font_size=25)
        play_again = it.Button(text="Jogar novamente", x=x_centered, y=y_centered+195, width=250, height=30, font_size=25)
        back_to_menu = it.Button(text="Voltar ao menu (ESC)", x=x_centered, y=y_centered+230, width=250, height=30, font_size=25)

        # Inicia um loop para a exibição da tela de game over
        while self.over:
            
            # Preenche o fundo da tela com a cor branca
            # screen.fill(st.WHITE)
            screen.blit(st.background, (0, 0))

            # Imprime uma mensagem de "Game Over" na tela
            self.draw_text(screen, "GAME OVER", 120, x_centered, y_centered - 150, st.WHITE)
            # Imprime a pontuação do jogador na tela
            self.draw_text(screen, f"Score: {str(player_score)}", 50, x_centered, y_centered - 20, st.WHITE)

            if not score_saved:
                # Imprime um rótulo para a caixa de nome do usuário
                self.draw_text(screen, "Digite seu nome:", 30, x_centered, y_centered+50, st.WHITE)

                # Desenha a caixa de texto para o nome do usuário
                player_name_box.update()
                player_name_box.draw(screen)

                # Desenha os botões da tela de game over
                save_score_button.draw(screen, (0,0,0))

            play_again.draw(screen, (0,0,0))
            back_to_menu.draw(screen, (0,0,0))

            # Tratamento de eventos
            for event in pygame.event.get():
                # Recolhe a posição atual do mouse
                pos = pygame.mouse.get_pos()

                # Atualiza o comportamento da caixa de texto de acordo com o evento
                player_name_box.handle_event(event)

                # Caso o usuário feche a janela
                if event.type == pygame.QUIT:
                    self.quit_game()

                # Caso o usuário aperte alguma tecla
                elif event.type == pygame.KEYDOWN:
                    # Caso o usuário aperte o botão ESC
                    if event.key == pygame.K_ESCAPE:
                        self.over = False
                        return False

                # Caso o usuário clique com o botão esquerdo do mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Caso o usuário clique no botão de play
                    if save_score_button.is_over(pos):
                        # Salva o score do jogador
                        score_saved = self.save_score(player_name_box, player_score)


                    # Caso o usuário clique no botão de voltar ao menu
                    elif back_to_menu.is_over(pos):
                        self.over = False
                        break

                    # Caso o usuário clique no botão de jogar novamente
                    elif play_again.is_over(pos):
                        self.over = False
                        self.restart = True
                        break

                    else:
                        pass
            
            # Atualiza a tela e o clock
            pygame.display.update()
            clock.tick(st.FPS)

    def reset_game(self):
        """Reseta as variáveis do jogo
        

        Returns
        -------
        None.

        """
        
        # Reinicia algumas constantes de controle de fluxo do jogo
        self.pause = False
        self.over = False

        # Reinicia as variáveis que armazenam os sprites do jogo
        st.all_sprites = pygame.sprite.Group()
        st.asteroids = pygame.sprite.Group()
        st.enemy_ships = pygame.sprite.Group()
        st.bullets = pygame.sprite.Group()
        st.enemies_bullets = pygame.sprite.Group()
        st.powers = pygame.sprite.Group()

    # Crie uma função para a dispersão de asteroides
    def spawn_asteroids(self, asteroids_group,all_sprites_group):
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
        asteroid = ge.Asteroid()
        asteroids_group.add(asteroid)
        all_sprites_group.add(asteroid)

    #Crie uma função para dispersão de naves inimigas    
    def spawn_enemy_ships(self, enemy_ships_group,all_sprites_group):
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
        
        enemy = ge.EnemyShip()
        enemy.enemy_shoots()
        enemy_ships_group.add(enemy)
        all_sprites_group.add(enemy)
        enemy.update()

    #Crie uma função para a morte do jogador
    def player_dies(self, loop, player_score):
        """Recebe o loop do jogo e o encerra.

        Parameters
        ----------
        loop : bool
            Loop do jogo.

        Returns
        -------
        loop : bool
            Loop do jogo, agora sendo "Falso".

        """

        # Renderiza a tela de "Game Over"
        self.game_over(player_score)

        # Atualiza e retorna a variável responsavel pelo loop do jogo
        loop = False

        return loop

    # Crie um método para o encerramento do jogo
    def quit_game(self):
        """Encerra o jogo e o executável.
        

        Returns
        -------
        None.

        """
        pygame.quit()
        sys.exit()

    # Crie uma função para exibição de texto
    def draw_text(self, surface, text, size, x, y, color, font_name=st.font_name_bold):
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
        font_name : str, optional
            Nome da fonte do texto. The default is st.font_name_bold.

        Returns
        -------
        None.

        """
        
        # Crie uma variável para a fonte utilizada
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def load_background(self, background_image_filename):
        """Carrega uma imagem de fundo
        

        Parameters
        ----------
        background_image_filename : str
            Nome do arquivo de imagem.

        Returns
        -------
        None.

        """
        # Carrega a imagem de fundo do jogo
        st.background = pygame.image.load(os.path.join(st.img_folder, background_image_filename))
        # Caso a tela seja maior que a imagem, redimensione a imagem de fundo
        if st.WIDTH > st.background.get_width():
            st.background = pygame.transform.scale(st.background, (st.WIDTH, st.WIDTH))

        # Armazene a altura desse st.background
        st.background_height = st.background.get_height()
