# Importando as bibliotecas necessÃ¡rias.
# -*- coding: utf-8 -*-
import pygame, math, random
from os import path
from Boss_screen import *
from Ugh_screen import *
from Menu import *
from Ugh_scene import *
from Boss_scene import *
#from pygame_functions import *

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'imagens')
snd_dir = path.join(path.dirname(__file__), 'sons')

# Dados gerais do jogo.
WIDTH = 1300 # Largura da tela
HEIGHT = 700 # Altura da tela
TILE_SIZE = 40 # Tamanho de cada tile (cada tile eh um quadrado)
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = int(TILE_SIZE * 1.5)
FPS = 60 # Frames por segundo

# Define algumas variaveis com as cores basicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define a aceleracao da gravidade
GRAVITY = 1.5
# Define a velocidade inicial no pulo
JUMP_SIZE = 25
# Define a altura do chao
GROUND = HEIGHT * 5 // 6

# Define acoes do player
IDLE = 0
RIGHT = 1
LEFT = 2
JUMP = 3
FALL = 4
JUMP_LEFT = 5
FALL_LEFT = 6
IDLE_LEFT = 7
ICED = 8 
ICED_LEFT = 9
POS = [IDLE, RIGHT, JUMP, FALL, ICED]
NEG = [LEFT, JUMP_LEFT, FALL_LEFT, IDLE_LEFT, ICED_LEFT]

# Define acoes do mob
ATTACK = 8
DEAD = 9

# Define acoes do magician
ATTACK_ICE = 10
DIE = 11

# Define os tipos de tiles
BLOCK = 0
EMPTY = -1

# States da tela
QUIT = 0
GAME_SCREEN = 1
BOSS_SCREEN = 2
GAME_OVER = 3
TELA_INICIAL = 4
TELA_AJUDA = 5
FOREST_SCREEN = 6
UGH_SCENE = 7
BOSS_SCENE = 8
# Define o mapa com os tipos de tiles
MAP1 = [   
        [],
        [],
        [],
        [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, BLOCK,BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [],
        [],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],    
        [BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY],
        [],    
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],
        [],    
        [BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY],
        [],    
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK],    
        [],
        [], 
        [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK]
        ]

def rot_center(image, angle):
    rot_image = pygame.transform.rotate(image, angle)
    return rot_image

def rot_center2(image, angle2):
    rot_image = pygame.transform.rotate(image, angle2)
    return rot_image

# Classe Health que representa os meteoros
class HealthBar(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        self.healthsheet =   [pygame.image.load(path.join(img_dir, "health(0).png")).convert(),
                              pygame.image.load(path.join(img_dir, "health(1).png")).convert(),
                              pygame.image.load(path.join(img_dir, "health(2).png")).convert(),
                              pygame.image.load(path.join(img_dir, "health(3).png")).convert(),
                              pygame.image.load(path.join(img_dir, "health(4).png")).convert(),
                              pygame.image.load(path.join(img_dir, "health(5).png")).convert()
                              ]
        
        i = 0
        while i < len(self.healthsheet):
            self.image = self.healthsheet[i]
            self.image.set_colorkey(BLACK)
            i += 1
        
        self.frame = 5
        self.image = self.healthsheet[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = 20
        # Sorteia um lugar inicial em y
        self.rect.y = - 30
        
    def update(self):
        self.image = self.healthsheet[self.frame]


# Class que representa os blocos do cenÃ¡rio
class Tile(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, row, column):

        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        tile_img = pygame.image.load(path.join(img_dir, "ground2.png")).convert()

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x = TILE_SIZE * column
        self.rect.y = TILE_SIZE * row
        
# Classe Health que representa os meteoros
class Health(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, blocks):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        health_img = pygame.image.load(path.join(img_dir, "health.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(health_img, (43,40))
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisÃµes
        self.blocks = blocks
        
        # Sorteia um lugar inicial em x
        self.rect.x = random.randint(43, WIDTH - 43)
        # Sorteia um lugar inicial em y
        self.rect.y = 0
        # Sorteia uma velocidade inicial
        self.speedx = 0
        self.speedy = 0


    def update(self):
        self.speedy += GRAVITY
        self.rect.y += GRAVITY
        
        # Corrige a posiÃ§Ã£o do personagem para antes da colisÃ£o
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                self.speedy = 0 

# Classe Jogador que representa Jack
class Player(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, row, column, blocks):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        #Cria spritesheet
        spritesheet =    [pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_000.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_001.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_002.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_003.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_004.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_005.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_006.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_007.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_008.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_009.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_000.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_001.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_002.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_003.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_004.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_005.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_006.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_007.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_008.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_009.png")).convert(), True, False),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Jump_000.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_000.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_001.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_002.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_003.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_004.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_005.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_006.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_007.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_008.png")).convert(),
                          pygame.image.load(path.join(img_dir, "JK_P_Gun__Right_009.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Jump_000.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_000.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_001.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_002.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_003.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_004.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_005.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_006.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_007.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_008.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_009.png")).convert(), True, False),        
                          pygame.image.load(path.join(img_dir, "rapazinhoAzul.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "rapazinhoAzul.png")).convert(), True,False)] 
                          
        i = 0
        while i < len(spritesheet):
            spritesheet[i] = pygame.transform.scale(spritesheet[i],(40,38))
            self.image = spritesheet[i]
            self.image.set_colorkey(BLACK)
            i += 1
        
        # Carregando a imagem de fundo.
        self.animations = {IDLE:spritesheet[0:10], 
                           LEFT:spritesheet[10:20], 
                           JUMP:spritesheet[20:21], 
                           FALL:spritesheet[20:21], 
                           RIGHT:spritesheet[21:31],
                           JUMP_LEFT:spritesheet[31:32],
                           FALL_LEFT:spritesheet[31:32],
                           IDLE_LEFT:spritesheet[32:42],
                           ICED:spritesheet[42:43],
                           ICED_LEFT:spritesheet[43:44]} 
        
        
        # Define estado atual (que define qual animaÃ§Ã£o deve ser mostrada)
        self.state = IDLE
        # Define animaÃ§Ã£o atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animaÃ§Ã£o
        self.frame = 0
        self.image = self.animation[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisÃµes
        self.blocks = blocks
        
        # Define posiÃ§Ã£o inicial.
        self.rect.x = row * TILE_SIZE - 750
        self.rect.bottom = column * TILE_SIZE + 750
        
        
        # Velocidade K_UP de Jack
        self.speedx = 0
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animaÃ§Ã£o: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        self.freeze_ticks = 1500
        self.startfreeze_ticks = 0
        
    def freeze(self):  
        if self.state != ICED and self.state != ICED_LEFT:            
            self.prevstate = self.state
            if self.prevstate == RIGHT or self.prevstate == JUMP:
                self.prevstate = IDLE
                self.speedx = 0
            elif self.prevstate == LEFT or self.prevstate == JUMP_LEFT:
                self.prevstate = IDLE_LEFT
                self.speedx = 0
            else:
                self.prevstate = self.state
        if self.state in POS:
            self.state = ICED 
        elif self.state in NEG:
            self.state = ICED_LEFT
        self.frame = 0 
        self.animation = self.animations[self.state]
        self.image = self.animation[self.frame]
        self.startfreeze_ticks = pygame.time.get_ticks()
        
    # Metodo que atualiza a posiÃ§Ã£o de Jack
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
         # Verifica o tick atual.
        now = pygame.time.get_ticks()
        if self.state == ICED or self.state == ICED_LEFT: 
            elapsed_ticks = now - self.startfreeze_ticks
            if elapsed_ticks > self.freeze_ticks: 
                self.state = self.prevstate
            else: 
                return 
                
            
            
        # Verifica quantos ticks se passaram desde a ultima mudanÃ§a de frame.
        elapsed_ticks = now - self.last_update

        # Se jÃ¡ estÃ¡ na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # AvanÃ§a um quadro.
            self.frame += 1
        
            # Atualiza animaÃ§Ã£o atual
            self.animation = self.animations[self.state]
            # Reinicia a animaÃ§Ã£o caso o Ã­ndice da imagem atual seja invÃ¡lido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posiÃ§Ã£o do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleraÃ§Ã£o da gravidade
        self.speedy += GRAVITY
        # Atualiza a posiÃ§Ã£o y
        self.rect.y += self.speedy

        
        # Se colidiu com algum bloco, volta para o ponto antes da colisÃ£o
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Atualiza o estado para caindo
        if self.speedy > 0 and self.state == JUMP:
            self.state = FALL
        elif self.speedy > 0 and self.state == JUMP_LEFT:
            self.state = FALL_LEFT

        # Corrige a posiÃ§Ã£o do personagem para antes da colisÃ£o
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                # Atualiza o estado para parado
                if self.state == FALL:
                    self.state = IDLE
                elif self.state == FALL_LEFT:
                    self.state = IDLE_LEFT
                # Se colidiu com algo, para de cair
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                # Atualiza o estado para parado
                if self.state == FALL:
                    self.state = IDLE
                elif self.state == FALL_LEFT:
                    self.state = IDLE_LEFT
                # Se colidiu com algo, para de cair
                self.speedy = 0
                
               
        if self.state == IDLE or self.state == IDLE_LEFT:
            # Define variÃ¡vel para caminhar
            keys = pygame.key.get_pressed()    
            # Verifica se estÃ¡ segurando alguma tela
            if keys[pygame.K_RIGHT] == True and keys[pygame.K_LEFT] == False:
                self.state = RIGHT
            elif keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == False:
                self.state = LEFT
                

        # Tenta andar em x
        self.rect.x += self.speedx
        # Corrige a posiÃ§Ã£o caso tenha passado do tamanho da janela
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        # Se colidiu com algum bloco, volta para o ponto antes da colisÃ£o
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posiÃ§Ã£o do personagem para antes da colisÃ£o
        for collision in collisions:
            # Estava indo para a direita
            if self.speedx > 0:
                self.rect.right = collision.rect.left
            # Estava indo para a esquerda
            elif self.speedx < 0:
                self.rect.left = collision.rect.right

    # MÃ©todo que faz o personagem pular
    def jump(self):               
        # SÃ³ pode pular se ainda nÃ£o estiver pulando ou caindo
        if self.speedy != 0:
            self.state = JUMP            
        elif self.state == IDLE or self.state == RIGHT:
            self.speedy -= JUMP_SIZE
            self.state = JUMP
        elif self.state == IDLE_LEFT or self.state == LEFT:
            self.speedy -= JUMP_SIZE
            self.state = JUMP_LEFT
    
# Classe Bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, blocks, mob, player):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        bullet_img = pygame.image.load(path.join(img_dir, "bala2.png")).convert()
        self.image = pygame.transform.scale(bullet_img,(8,8))
        
        # Arrumando tamanho da imagem
        
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisÃµes
        self.blocks = blocks
        
        # Guarda o grupo de blocos para tratar as colisÃµes
        self.mob = mob
        
        # Coloca no lugar inicial definido em x, y do constutor
        if player.state in POS:
            self.rect.bottom = y+30
            self.rect.centerx = x+10
            self.speedx = 20
        if player.state in NEG:
            self.rect.bottom = y+30
            self.rect.centerx = x-10
            self.speedx = -20

    # Metodo que atualiza a posiÃ§Ã£o da bala
    def update(self):
        self.rect.x += self.speedx
        self.mask = pygame.mask.from_surface(self.image)
        
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()
        
        # Se colidiu com algum bloco, morre
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posiÃ§Ã£o do personagem para antes da colisÃ£o
        if len(collisions) > 0:
            self.kill()

# Classe Mob que representa os meteoros
class Mob(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, blocks, fire):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        spritesheetmob = [pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (2).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (3).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (4).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (5).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (6).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (7).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (8).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (9).png")).convert(),
                          pygame.image.load(path.join(img_dir, "attack (10).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (1).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (2).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (3).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (4).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (5).png")).convert(),
                          pygame.image.load(path.join(img_dir, "dead (6).png")).convert()
                          ]

        
        
        i = 0
        while i < len(spritesheetmob):
            spritesheetmob[i] = pygame.transform.scale(spritesheetmob[i],(50,73))
            self.image = spritesheetmob[i]
            self.image.set_colorkey(BLACK)
            i += 1
        
        # Carregando a imagem de fundo.
        self.animations = {ATTACK:spritesheetmob[0:25],
                           DEAD:spritesheetmob[26:31]}
        
        self.morre = False
        self.state = ATTACK 
        # Define estado atual (que define qual animaÃ§Ã£o deve ser mostrada)
        if self.state == ATTACK:
            
        # Define animaÃ§Ã£o atual
            self.animation = self.animations[self.state]
            # Inicializa o primeiro quadro da animaÃ§Ã£o
            self.frame = 0
            self.image = self.animation[self.frame]
            
            # Detalhes sobre o posicionamento.
            self.rect = self.image.get_rect()
            
        if self.state == DEAD:
            
        # Define animaÃ§Ã£o atual
            self.animation = self.animations[self.state]
            # Inicializa o primeiro quadro da animaÃ§Ã£o
            self.frame = 0
            self.image = self.animation[self.frame]
            
            
            # Detalhes sobre o posicionamento.
            self.rect = self.image.get_rect()
    
        # Guarda o grupo de blocos para tratar as colisÃµes
        self.blocks = blocks
        self.fire = fire
        self.vida = 5
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 0
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animaÃ§Ã£o: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posiÃ§Ã£o de mob
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudanÃ§a de frame.
        elapsed_ticks = now - self.last_update

        if self.state == DEAD and self.frame == 4:
            self.morre = True


        # Se jÃ¡ estÃ¡ na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            if self.frame == 24:
                self.fire = True
            else:
                self.fire = False

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # AvanÃ§a um quadro.
            self.frame += 1
        
            # Atualiza animaÃ§Ã£o atual
            self.animation = self.animations[self.state]
            # Reinicia a animaÃ§Ã£o caso o Ã­ndice da imagem atual seja invÃ¡lido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posiÃ§Ã£o do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleraÃ§Ã£o da gravidade
        self.speedy += GRAVITY
        # Atualiza a posiÃ§Ã£o y
        self.rect.y += self.speedy
        
        # Se colidiu com algum bloco, volta para o ponto antes da colisÃ£o
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)

        # Corrige a posiÃ§Ã£o do personagem para antes da colisÃ£o
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                self.speedy = 0 

# Classe Arrow que representa flechas
class Arrow(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, speedx, speedy, angle):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        arrow_img = pygame.image.load(path.join(img_dir, "arrow.png")).convert()
        self.image = pygame.transform.scale(arrow_img,(30,5))
        self.image = rot_center(self.image, angle)
        
        # Arrumando tamanho da imagem
        
        
        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centery = y
        self.rect.centerx = x
        self.cx = x
        self.cy = y
        self.speedx = speedx
        self.speedy = speedy

    # Metodo que atualiza a posiÃ§Ã£o da bala
    def update(self):
        self.cx += self.speedx
        self.cy += self.speedy
        self.rect.x = int(self.cx)
        self.rect.y = int(self.cy)
        self.mask = pygame.mask.from_surface(self.image)
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()

#Classe que representa os Magos 
class Magician(pygame.sprite.Sprite):
    #Construtor da Classe 
    def __init__(self, x, y, blocks, fire):
        # Construtor da classe Final (sprite) 
        pygame.sprite.Sprite.__init__(self)
        
        spritesheetmag =  [
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_000.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_000.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_002.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_003.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_004.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_005.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_006.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_007.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_008.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"Attack 2_entity_000_Attack 2_009.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"ad_entity_000_Dead_000.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"ad_entity_000_Dead_001.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"ad_entity_000_Dead_002.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"ad_entity_000_Dead_003.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"ad_entity_000_Dead_004.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"ad_entity_000_Dead_005.png" )).convert(),True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir,"ad_entity_000_Dead_006.png" )).convert(),True, False),
                           ]
        i = 0
        while i < len(spritesheetmag):
            spritesheetmag[i] = pygame.transform.scale(spritesheetmag[i],(50,44))
            self.image = spritesheetmag[i]
            self.image.set_colorkey(BLACK)
            i += 1
         # Carregando a imagem de fundo.
        self.animations = {ATTACK:spritesheetmag[0:22],
                           DIE:spritesheetmag[22:29]}
        
        
        # Define estado atual (que define qual animaÃ§Ã£o deve ser mostrada)
        self.state = ATTACK
        self.morre = False

        # Define animaÃ§Ã£o atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animaÃ§Ã£o
        self.frame = 0
        self.image = self.animation[self.frame]
        self.vida = 5

        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisÃµes
        self.blocks = blocks
        self.fire = fire
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 0
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animaÃ§Ã£o: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posiÃ§Ã£o dos Magos 
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudanÃ§a de frame.
        elapsed_ticks = now - self.last_update
        
        if self.state == DIE and self.frame == 5:
            self.morre = True

        # Se jÃ¡ estÃ¡ na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            if self.frame == 21:
                self.fire = True
            else:
                self.fire = False

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # AvanÃ§a um quadro.
            self.frame += 1
        
            # Atualiza animaÃ§Ã£o atual
            self.animation = self.animations[self.state]
            # Reinicia a animaÃ§Ã£o caso o Ã­ndice da imagem atual seja invÃ¡lido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posiÃ§Ã£o do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            self.mask = pygame.mask.from_surface(self.image)
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleraÃ§Ã£o da gravidade
        self.speedy += GRAVITY
        # Atualiza a posiÃ§Ã£o y
        self.rect.y += self.speedy
        
        # Se colidiu com algum bloco, volta para o ponto antes da colisÃ£o
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)

        # Corrige a posiÃ§Ã£o do personagem para antes da colisÃ£o
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                self.speedy = 0 
        

class Ice(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, speedx, speedy, angle2):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        arrow_img = pygame.image.load(path.join(img_dir, "ice spell.png")).convert()
        self.image = pygame.transform.scale(arrow_img,(15,14))
        self.image = rot_center2(self.image, angle2)
        
        # Arrumando tamanho da imagem
        
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centery = y
        self.rect.centerx = x
        self.cx = x
        self.cy = y
        self.speedx = speedx
        self.speedy = speedy


    # Metodo que atualiza a posiÃ§Ã£o da bala
    def update(self):
        self.cx += self.speedx
        self.cy += self.speedy
        self.rect.x = int(self.cx)
        self.rect.y = int(self.cy)
        self.mask = pygame.mask.from_surface(self.image)
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()

# InicializaÃ§Ã£o do Pygame.
pygame.init()
pygame.mixer.init()

# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)

# Nome do jogo
pygame.display.set_caption("Tales of Jack")

# VariÃ¡vel para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'Full Moon - background.png')).convert()
background_rect = background.get_rect()

# Carrega os sons do jogo
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'shot.ogg'))
game_over_sound = pygame.mixer.Sound(path.join(snd_dir, 'game_over_bad_chest.wav'))
arrow_sound = pygame.mixer.Sound(path.join(snd_dir, 'Archers-shooting.ogg'))
die_sound = pygame.mixer.Sound(path.join(snd_dir, 'Hurting The Robot.wav'))
grunt_sound = pygame.mixer.Sound(path.join(snd_dir, 'grunt.wav'))  
victory_sound = pygame.mixer.Sound(path.join(snd_dir, 'victory.ogg'))
ice_sound = pygame.mixer.Sound(path.join(snd_dir, 'ice_sound.ogg'))
heal_sound = pygame.mixer.Sound(path.join(snd_dir, 'healspell.ogg'))
door_sound = pygame.mixer.Sound(path.join(snd_dir, 'door.ogg'))
click_sound = pygame.mixer.Sound(path.join(snd_dir, 'click.ogg'))

# Classe Jogador que representa Jack
class Door(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        # Carregando a imagem de fundo.
        door = pygame.image.load(path.join(img_dir, "door.png")).convert()
        
        # Diminuindo o tamanho da imagem.
        self.image = pygame.transform.scale(door, (64,96))
        
        # Deixando transparente.
        self.image.set_colorkey(WHITE)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Sorteia um lugar inicial em x
        self.rect.x = 1236
        # Sorteia um lugar inicial em y
        self.rect.y = 604
doors = pygame.sprite.Group()


def fade(WIDTH, HEIGHT): 
    door_sound.play()
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0,0,0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(4)
        
quit_button = pygame.image.load(path.join(img_dir, "quit.png")).convert()
retry_button = pygame.image.load(path.join(img_dir, "retry.png")).convert()

def retry():
    global HEIGHT
    x =  (220)
    y = (HEIGHT * 0.05)
    retry_button.set_colorkey(WHITE)
    screen.blit(retry_button, (x,y))
    
def leave():
    global HEIGHT
    x =  (880)
    y = (HEIGHT * 0.05)
    quit_button.set_colorkey(WHITE)
    screen.blit(quit_button, (x,y))
        
# Comando para evitar travamentos.
def game_screen(screen):
    
    # Loop principal.
    
    vida = 5
    last_heal = 0
    door = Door()

    # Sprites de block sÃ£o aqueles que impedem o movimento do jogador
    blocks = pygame.sprite.Group()
    

    row = len(MAP1)
    column = len(MAP1[0])

    # Cria Jack. O construtor serÃ¡ chamado automaticamente.
    player = Player(row, column, blocks)
    
    # Cria barra de vida. O construtor serÃ¡ chamado automaticamente.
    healthbar = HealthBar()
    
    
    
    # Cria um grupo de sprites e adiciona Jack.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(healthbar)
    
    # Cria tiles de acordo com o mapa
    for row in range(len(MAP1)):
        for column in range(len(MAP1[row])):
            tile_type = MAP1[row][column]
            if tile_type == BLOCK:
                tile = Tile(row, column)
                all_sprites.add(tile)
                blocks.add(tile)
                
    # Cria um grupo sÃ³ de esqueletos
    mob = pygame.sprite.Group()
    
    #Cria um grupo so para magos 
    mag = pygame.sprite.Group() 
    
    # Cria i mobs e adiciona no grupo
    xs = [1275,1275,1275]
    ys = [600,500,50]
    for i in range (len(xs)): 
        x = xs[i]
        y = ys[i] 
        m = Mob(x,y,blocks,Ice )
        all_sprites.add(m)
        mob.add(m)
        
    # Cria i magos e adiciona o grupo 
    xs = [20,20,20]
    ys = [500,250,50]
    for i in range(len(xs)):
        x = xs[i]
        y = ys[i] 
        m = Magician(x,y, blocks, Ice)
        all_sprites.add(m)
        mag.add(m) 
        
    
    # Cria um grupo para tiros
    bullets = pygame.sprite.Group()
    
    # Cria um grupo para flechas
    arrows = pygame.sprite.Group()
    
    #Cria um grupo so para icehits
    ices = pygame.sprite.Group()     
    
    # Cria um grupo sÃ³ de itens health
    healths = pygame.sprite.Group()
    
    pygame.mixer.music.load(path.join(snd_dir, 'blackmist II.mp3'))
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(loops=-1)
    while True:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        #Adiciona as flechas no mapa 
        for m in mob:
            if m.fire:  
                m.fire = False
                dx = player.rect.centerx - m.rect.left
                dy = player.rect.centery - m.rect.centery
                d = (dx**2 + dy**2)**(1/2)
                if dy < 0:
                    Sy = -10*dy/d
                Sx = 10*dx/d
                Sy = 10*dy/d
                angle = math.atan(Sy/Sx)
                angle = -(math.degrees(angle))

                

                arrow = Arrow(m.rect.left, m.rect.centery, Sx, Sy, angle)
                all_sprites.add(arrow)
                arrows.add(arrow)
                arrow_sound.play()
                
        #Adiciona os ices
        for mg in mag:
            if mg.fire:
                mg.fire = False
                
                dx2 = player.rect.centerx - mg.rect.left
                dy2 = player.rect.centery - mg.rect.centery
                d2 = (dx2**2 + dy2**2)**(1/2)
                if dy2 < 0:
                    Sy2 = -10*dy2/d2
                Sx2 = 10*dx2/d2
                Sy2 = 10*dy2/d2  
                angle2 = math.atan(Sy2/Sx2)
                angle2 = -(math.degrees(angle2))


                
                ice = Ice(mg.rect.right, mg.rect.centery, Sx2, Sy2, angle2)
                all_sprites.add(ice)
                ices.add(ice) 
                
                
                
                
        # Processa os eventos (mouse, teclado, botÃ£o, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_q:
                    return QUIT
            
            if player.state != ICED and player.state != ICED_LEFT:  
                # Verifica se pulou
                if event.type == pygame.KEYDOWN:       
                    if event.key == pygame.K_UP and player.state in POS:                    
                        player.jump()
                        player.state = JUMP
                    elif event.key == pygame.K_UP and player.state in NEG:                    
                        player.jump()
                        player.state = JUMP_LEFT
            
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = -5
                        player.state = LEFT
                    elif event.key == pygame.K_RIGHT:
                        player.speedx = 5
                        player.state = RIGHT
                    # Se for um espaÃ§o atira!
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(player.rect.centerx, player.rect.top, blocks, mob, player)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                        pew_sound.stop() 
                        pew_sound.play()                    
                
                # Verifica se soltou alguma tecla.
                if event.type == pygame.KEYUP:
                    # Dependendo da tecla, altera a velocidade.
                    if event.key == pygame.K_LEFT:
                        player.speedx = 0                    
                        player.state = IDLE_LEFT
                    elif event.key == pygame.K_RIGHT:
                        player.speedx = 0                    
                        player.state = IDLE
                    
        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite.
        all_sprites.update()
        
        # Tempo da risada
        now_heal = pygame.time.get_ticks()
        elapsed_heal = now_heal - last_heal      
        if elapsed_heal > random.randint(25000, 35000):
            health = Health(blocks)
            all_sprites.add(health)
            healths.add(health)
            last_heal = now_heal
        
        # Verifica se houve colisÃ£o entre tiro e meteoro
        hits = pygame.sprite.groupcollide(mob, bullets, False, True, pygame.sprite.collide_mask)
        for m in hits:
            die_sound.play()
            m.vida -= 1
            if m.vida == 0:
                m.state = DEAD
        for m in mob:
            if m.morre == True:
                m.kill()
                
        # Verifica se houve colisÃ£o entre tiro e meteoro
        hits = pygame.sprite.groupcollide(mag, bullets, False, True, pygame.sprite.collide_mask)
        for mg in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            die_sound.play()
            mg.vida -= 1
            if mg.vida == 0:
                mg.state = DIE
        for mg in mag:
            if mg.morre == True:
                mg.kill()
            
    
        hits = pygame.sprite.spritecollide(player, arrows, True, pygame.sprite.collide_mask)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            grunt_sound.play()
            vida -= 1
            healthbar.frame -= 1
            
        hits = pygame.sprite.spritecollide(player, ices, True, pygame.sprite.collide_mask) 
        for hit in hits: #Pode haver mais de um 
            ice_sound.play()
            player.freeze()
            
        hits = pygame.sprite.spritecollide(player, healths, True, pygame.sprite.collide_mask)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            if vida < 4:
                vida += 2        
                healthbar.frame += 2
            elif vida < 5:
                vida += 1
                healthbar.frame += 1
            else:
                vida == 5
            heal_sound.play()
            
        hits = pygame.sprite.spritecollide(player, doors, True, pygame.sprite.collide_mask) 
        for hit in hits: #Pode haver mais de um 
            fade(WIDTH, HEIGHT)
            pygame.mixer.music.stop()
            return BOSS_SCREEN
            
        # Verifica se caiu da tela
        if player.rect.y > 700 or vida == 0:
            pygame.mixer.music.stop()
            return GAME_OVER
        
        if len(mob) == 0 and len(mag) == 0:
            all_sprites.add(door)
            doors.add(door)
            
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
def game_over(screen, tela_anterior):
    pygame.mixer.music.stop()
    game_over_sound.play()  
    game_over = pygame.image.load(path.join(img_dir, "Game-over-2.png")).convert()
    while True:        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        screen.fill(BLACK)
        screen.blit(game_over,[77,0])
        retry()
        leave()
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 230 and pos[0] < 420 and pos[1] > 35 and pos[1] < 180:
                    click_sound.play()
                    return tela_anterior
                elif pos[0] > 890 and pos[0] < 1110 and pos[1] > 35 and pos[1] < 180:
                    click_sound.play()
                    return QUIT

try:
    tela_anterior = -1
    tela_atual = TELA_INICIAL
    while tela_atual != QUIT:
        if tela_atual == TELA_INICIAL:
            tela_atual = tela_inicial(screen)
        elif tela_atual == TELA_AJUDA:
            tela_atual = tela_ajuda(screen)
        elif tela_atual == BOSS_SCENE:
            tela_atual = text_ani('Stage 1: Lobosster´s Castle', (1, 1))
        elif tela_atual == GAME_SCREEN:
            tela_anterior = tela_atual
            tela_atual = game_screen(screen)            
        elif tela_atual == BOSS_SCREEN:
            tela_anterior = tela_atual
            tela_atual = boss_screen(screen)
        elif tela_atual == UGH_SCENE:
            tela_atual = text_ugh('Stage 2: Ugh´s Forest', (1, 1))
        elif tela_atual == FOREST_SCREEN:
            tela_anterior = tela_atual
            tela_atual = ugh_screen(screen)
        elif tela_atual == GAME_OVER:
            tela_atual = game_over(screen, tela_anterior)
        
finally:
    pygame.quit()
