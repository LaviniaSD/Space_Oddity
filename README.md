<h1 align="center" >🪐Space Oddity🪐</h1>
<p align="center">  Status: Concluído 🚀</p>

<p>"Space Oddity" é um jogo Shoot 'em Up no estilo arcade. Nele, o jogador controla sua nave através do espaço destruindo asteroides e naves inimigas e durante sua jornada ele poderá encontrar algumas recompensas para ajudá-lo, como escudos que o protegerão e estrelas que o darão a habilidade de tiros duplos, mas esses efeitos não são permanentes, então cuidado! A qualquer momento você poderá colidir com algo que encerará sua jornada.</p>

<h3>Índice:</h3>

   * [Sobre o projeto](#sobre)
   * [Pré Requisitos](#pre-requisitos)
   * [Como ler esse projeto?](#como-ler)
   * [Nossa Equipe](#equipe)




<h3 id=sobre>Sobre o projeto:</h3>
=======
- [X] Background em movimentação
- [X] Música de Fundo

<h3>Jogador:</h3>

- [X] Movimentação (4 direções, livre), velocidade
- [X] Life (1 life, morreu acabou o jogo)
- [X] Hitbox (derivada de uma classe hitbox)
- [X] Atirar (Tiros derivados de uma classe Bullet, com cadência e sprites próprios, inerentes ao jogador, dano próprio.
)
- [X] Guardar Pontuação (Calculada pela pontuação dos inimigos que o jogador matou
)

<h3>Asteroides:</h3>

- [X] Movimentação Fixa
- [X] Spawn Controlado (gerado de forma randômica controlada, a cada x segundos conforme o tempo de jogo (quantidade de iterações))
- [X] Tamanhos de hitbox diferentes
- [X] Life
- [X] Pontuação conforme hitbox
- [X] Explodir e gerar asteroides menores

<h3>Naves inimigas:</h3>

- [X] Movimentação Fixa
- [X] Spawn Controlado (gerado de forma randômica controlada, a cada x segundos conforme o tempo de jogo (quantidade de iterações))
- [X] Hitbox
- [X] Life
- [X] Pontuação conforme life da nave
- [X] Atira (Configurar cadência, velocidade e padrão de tiro por ângulo)

<h3>Score:</h3>

- [X] Aumenta conforme o score de jogador
- [X] Exibido na tela como tratamento de texto 


<h3>Bônus:</h3>

- [X] Shields
- [X] Tiros duplos

<h3>Tela de game over:</h3>

- [ ] Escurecer a tela do jogo ("Pausada")
- [ ] Botão Restart - Reiniciar o jogo
- [ ] Botão Menu - Volta para o menu
- [ ] Botão Registrar score - Diponível apenas para jogador no top 20. Caso o jogador não esteja no top 20 ele só possui a opção de sair.

  Esse projeto tem por finalidade criar um jogo utilizando a biblioteca pygame com base nos conhecimentos de orientação a objetos.

<h3 id=pre-requisitos>Pré requisitos:</h3>

1. : Instalar os requerimentos
  

<h3 id=como-ler>Como utilizar esse projeto?</h3>
Para entender e executar esse projeto siga as seguintes instruções:
 
- [ ] Certifique-se que esse repositório está em sua máquina e o acesse.


- [ ] No prompt de comando do seu computador, digite o seguinte código:

```
pip install -r requirements.txt
```

- [ ] Para entender as regras do jogo, acesse o arquivo <b>index</b> na pasta <b>instructions</b> ou acesse o link ...
- [ ] Para iniciar o jogo, execute o arquivo main.py.
- [ ] Para visualizar os diagramas UML e de classes utilizados como base do projeto, acesse a pasta <b>Diagrams</b>
- [ ] Para ler os arquivos que contém as classes e os loops do jogo acesse a pasta <b>src</b>.
  
  
  <h3 id=equipe>Nossa equipe:</h3>
  
  * [Abner Lucas](https://github.com/AbPCV)
  
  * [Almir Fonseca](https://github.com/AlmirFonseca)
  
  * [Lavínia Dias](https://github.com/LaviniaSD)
   
  * [Gustavo Campanha](https://github.com/GustavoCampanha)
    
  
  
<p align="center"> Vista seu capacete e inicie sua jornada!🚀</p>
