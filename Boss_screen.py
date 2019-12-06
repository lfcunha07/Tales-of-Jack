# Importando as bibliotecas necessárias.
import pygame, time, random
from os import path
#from pygame_functions import *

# Estabelece a pasta que contem as figuras.
img_dir = path.join(path.dirname(__file__), 'imagens')
snd_dir = path.join(path.dirname(__file__), 'sons')

# Dados gerais do jogo.
WIDTH = 1300 # Largura da tela
HEIGHT = 700 # Altura da tela
TILE_SIZE = 40 # Tamanho de cada tile (cada tile é um quadrado)
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = int(TILE_SIZE * 1.5)
FPS = 60 # Frames por segundo

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Define a aceleração da gravidade
GRAVITY = 1.5
# Define a velocidade inicial no pulo
JUMP_SIZE = 25
# Define a altura do chão
GROUND = HEIGHT * 5 // 6

# Define global game over
game_over = False

# Define ações do player
IDLE = 0
RIGHT = 1
LEFT = 2
JUMP = 3
FALL = 4
JUMP_LEFT = 5
FALL_LEFT = 6
IDLE_LEFT = 7
POS = [IDLE, RIGHT, JUMP, FALL]
NEG = [LEFT, JUMP_LEFT, FALL_LEFT, IDLE_LEFT]

# Define ações do boss
WALK_RIGHT = 8
WALK_LEFT = 9
SHOOT_RIGHT = 10
SHOOT_LEFT = 11
SHOOT = [SHOOT_RIGHT, SHOOT_LEFT]

# Constantes tela
QUIT = 0
GAME_SCREEN = 1
BOSS_SCREEN = 2
GAME_OVER = 3
UGH_SCENE = 7
# Define os tipos de tiles
BLOCK = 0
EMPTY = -1

# Define o mapa com os tipos de tiles
MAP2 = [   
        [],    
        [],
        [],
        [],
        [],
        [],
        [],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [],    
        [],
        [],    
        [],
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY,EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],    
        [],
        [],    
        [],    
        [],
        [BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK,BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK]
        ]

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
        if self.frame < 0:
            self.frame = 0
        self.image = self.healthsheet[self.frame]

# Class que representa os blocos do cenário
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
        
        # Guarda o grupo de blocos para tratar as colisões
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
        
        # Corrige a posição do personagem para antes da colisão
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
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "JK_P_Gun__Idle_009.png")).convert(), True, False)]         
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
                           IDLE_LEFT:spritesheet[32:42]}
        
        self.damage = False
        
        
        # Define estado atual (que define qual animação deve ser mostrada)
        self.state = IDLE
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        
        # Define posição inicial.
        self.rect.x = row * TILE_SIZE - 600
        self.rect.bottom = column * TILE_SIZE
        
        
        # Velocidade K_UP de Jack
        self.speedx = 0
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posição de Jack
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # Avança um quadro.
            self.frame += 1
        
            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleração da gravidade
        self.speedy += GRAVITY
        # Atualiza a posição y
        self.rect.y += self.speedy
        
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Atualiza o estado para caindo
        if self.speedy > 0 and self.state == JUMP:
            self.state = FALL
        elif self.speedy > 0 and self.state == JUMP_LEFT:
            self.state = FALL_LEFT

        # Corrige a posição do personagem para antes da colisão
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
            # Define variável para caminhar
            keys = pygame.key.get_pressed()    
            # Verifica se está segurando alguma tela
            if keys[pygame.K_RIGHT] == True and keys[pygame.K_LEFT] == False:
                self.state = RIGHT
            elif keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == False:
                self.state = LEFT
                

        # Tenta andar em x
        self.rect.x += self.speedx
        # Corrige a posição caso tenha passado do tamanho da janela
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 1
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para a direita
            if self.speedx > 0:
                self.rect.right = collision.rect.left
            # Estava indo para a esquerda
            elif self.speedx < 0:
                self.rect.left = collision.rect.right

    # Método que faz o personagem pular
    def jump(self):               
        # Só pode pular se ainda não estiver pulando ou caindo
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
    def __init__(self, x, y, blocks, boss, player):
        
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
        
        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        
        # Guarda o grupo de blocos para tratar as colisões
        self.boss = boss
        
        # Coloca no lugar inicial definido em x, y do constutor
        if player.state in POS:
            self.rect.bottom = y+30
            self.rect.centerx = x+10
            self.speedx = 20
        if player.state in NEG:
            self.rect.bottom = y+30
            self.rect.centerx = x-10
            self.speedx = -20

    # Metodo que atualiza a posição da bala
    def update(self):
        self.rect.x += self.speedx
        self.mask = pygame.mask.from_surface(self.image)
        
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()
        
        # Se colidiu com algum bloco, morre
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)
        # Corrige a posição do personagem para antes da colisão
        if len(collisions) > 0:
            self.kill()

# Classe Boss que representa os meteoros
class Boss(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, blocks):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        spritesheetboss = [pygame.image.load(path.join(img_dir, "spr_lobster_walk_0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobster_walk_1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobster_walk_2.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobster_walk_3.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobster_walk_4.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobster_walk_5.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobster_walk_6.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobster_walk_7.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_0.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_1.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_2.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_3.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_4.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_5.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_6.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobster_walk_7.png")).convert(), True, False),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_2.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_3.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_4.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_5.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_6.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_7.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_8.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_9.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_10.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_11.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_12.png")).convert(),
                          pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_13.png")).convert(),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_0.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_1.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_2.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_3.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_4.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_5.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_6.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_7.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_8.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_9.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_10.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_11.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_12.png")).convert(), True, False),
                          pygame.transform.flip(pygame.image.load(path.join(img_dir, "spr_lobtser_lobsterHammer_13.png")).convert(), True, False)
                          ]
        
        i = 0
        while i < len(spritesheetboss):
            spritesheetboss[i] = pygame.transform.scale(spritesheetboss[i],(217,150))
            self.image = spritesheetboss[i]
            self.image.set_colorkey(BLACK)
            i += 1
        
        # Carregando a imagem de fundo.
        self.animations = {WALK_RIGHT:spritesheetboss[0:8], WALK_LEFT:spritesheetboss[8:16], SHOOT_RIGHT:spritesheetboss[16:31], SHOOT_LEFT:spritesheetboss[31:46]}
        
        
        # Define estado atual (que define qual animação deve ser mostrada)
        self.state = WALK_LEFT
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Guarda o grupo de blocos para tratar as colisões
        self.blocks = blocks
        self.fire = False
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y + 700
        self.rect.centerx = x + 1200
        self.speedx = -8
        self.speedy = 0
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posição de boss
    def update(self):
        # Vamos tratar os movimentos de maneira independente.
        # Primeiro tentamos andar no eixo y e depois no x.
        
        # Verifica o tick atual.
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudança de frame.
        elapsed_ticks = now - self.last_update

        # Se já está na hora de mudar de imagem...
        if elapsed_ticks > self.frame_ticks:
            if self.state in SHOOT and self.frame == 7:
                self.fire = True
            else:
                self.fire = False

            # Marca o tick da nova imagem.
            self.last_update = now
            
            # Avança um quadro.
            self.frame += 1
        
            # Atualiza animação atual
            self.animation = self.animations[self.state]
            # Reinicia a animação caso o índice da imagem atual seja inválido
            if self.frame >= len(self.animation):
                self.frame = 0
            
            # Armazena a posição do centro da imagem
            center = self.rect.center
            # Atualiza imagem atual
            self.image = self.animation[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleração da gravidade
        self.speedy += GRAVITY
        # Atualiza a posição y
        self.rect.y += self.speedy
        
        # Se colidiu com algum bloco, volta para o ponto antes da colisão
        collisions = pygame.sprite.spritecollide(self, self.blocks, False)

        # Corrige a posição do personagem para antes da colisão
        for collision in collisions:
            # Estava indo para baixo
            if self.speedy > 0:
                self.rect.bottom = collision.rect.top
                self.speedy = 0
                
            # Estava indo para cima
            elif self.speedy < 0:
                self.rect.top = collision.rect.bottom
                self.speedy = 0 
        
         # Tenta andar em x
        self.rect.x += self.speedx
        
        # Corrige a posição caso tenha passado do tamanho da janela
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx = 0
            self.state = SHOOT_RIGHT
            self.frame = 0
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH - 10
            self.speedx = 0      
            self.state = SHOOT_LEFT
            self.frame = 0
        
        if self.frame == (len(self.animation)-1) and self.state == SHOOT_RIGHT:
            self.state = WALK_RIGHT
            self.frame = 0
            self.speedx = 8
        elif self.frame == (len(self.animation)-1) and self.state == SHOOT_LEFT:
            self.state = WALK_LEFT
            self.frame = 0
            self.speedx = -8

            

# Classe Rock que representa flechas
class Rock(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, boss):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        # Carregando a imagem de fundo.
        rock_img = pygame.image.load(path.join(img_dir, "pedra.png")).convert()
        self.image = pygame.transform.scale(rock_img,(15,15))

        # Deixando transparente.
        self.image.set_colorkey(BLACK)
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Coloca no lugar inicial definido em x, y do constutor
        if boss.state == SHOOT_RIGHT:
            self.rect.bottom = y + 200
            self.rect.centerx = x + 30
            self.speedx = random.randint(5, 18)
            self.speedy = random.randint(-80, -30)
        if boss.state == SHOOT_LEFT:
            self.rect.bottom = y + 200
            self.rect.centerx = x - 30
            self.speedx = random.randint(-18, -5)
            self.speedy = random.randint(-80, -30)

    # Metodo que atualiza a posição da pedra
    def update(self):
        self.rect.x += self.speedx
        self.speedy += GRAVITY
        self.rect.y += self.speedy
        self.mask = pygame.mask.from_surface(self.image)
        # Se o tiro passar do fim da tela, morre.
        if self.rect.x > 1300 or self.rect.x < 0:
            self.kill()
        if self.rect.y > 700:
            self.kill()


# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()


# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)

# Nome do jogo
pygame.display.set_caption("Tales of Jack")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega o fundo do jogo
background = pygame.image.load(path.join(img_dir, 'Full Moon - background.png')).convert()
background_rect = background.get_rect()

# Carrega os sons do jogo
game_over_sound = pygame.mixer.Sound(path.join(snd_dir, 'game_over_bad_chest.wav'))
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'shot.ogg'))
laugh_sound = pygame.mixer.Sound(path.join(snd_dir, 'laugh-evil-1.ogg'))
grunt_sound = pygame.mixer.Sound(path.join(snd_dir, 'grunt.wav'))  
victory_sound = pygame.mixer.Sound(path.join(snd_dir, 'victory.ogg'))
boom_sound = pygame.mixer.Sound(path.join(snd_dir, 'boom.ogg'))
heal_sound = pygame.mixer.Sound(path.join(snd_dir, 'healspell.ogg'))

def bosshealth(vida_boss):
    
    if vida_boss > 500:
        vida_boss_color = GREEN
    elif vida_boss > 250:
        vida_boss_color = YELLOW
    else:
        vida_boss_color = RED
    
    pygame.draw.rect(screen, vida_boss_color, (WIDTH - vida_boss, 150, vida_boss, 10))
    
name_boss = pygame.image.load(path.join(img_dir, "lobosster.png")).convert()
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

def lobosster():
    global WIDTH, HEIGHT
    x =  (WIDTH - 160)
    y = (HEIGHT * 0.14)
    name_boss.set_colorkey(BLACK)
    screen.blit(name_boss, (x,y))

# Comando para evitar travamentos.
def boss_screen(screen):
    
    # Loop principal.
    pygame.mixer.music.load(path.join(snd_dir, 'the final boss.ogg'))
    pygame.mixer.music.set_volume(0.7)
    vida = 5
    vida_boss = 750
    running = True
    pygame.mixer.music.play(loops=-1)
    last_laugh = 0
    last_heal = 0        
    row = len(MAP2)
    column = len(MAP2[0])
        # Sprites de block são aqueles que impedem o movimento do jogador
    blocks = pygame.sprite.Group()
    
    # Cria Jack. O construtor será chamado automaticamente.
    player = Player(row, column, blocks)
    
    # Cria Boss. O construtor será chamado automaticamente.
    boss = [Boss(row, column, blocks)]
    
    # Cria barra de vida. O construtor será chamado automaticamente.
    healthbar = HealthBar()
    
    # Cria um grupo de sprites e adiciona Jack.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(boss)
    all_sprites.add(healthbar)
    # Cria tiles de acordo com o mapa
    for row in range(len(MAP2)):
        for column in range(len(MAP2[row])):
            tile_type = MAP2[row][column]
            if tile_type == BLOCK:
                tile = Tile(row, column)
                all_sprites.add(tile)
                blocks.add(tile)
    
    # Cria um grupo para tiros
    bullets = pygame.sprite.Group()
    
    # Cria um grupo para flechas
    rocks = pygame.sprite.Group()
    
    # Cria um grupo só de itens health
    healths = pygame.sprite.Group()
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                return QUIT
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_q:
                    return QUIT
                
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
                # Se for um espaço atira!
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top, blocks, boss[0], player)
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
        now = pygame.time.get_ticks()
        elapsed_time = now - last_laugh
        if elapsed_time > 15000:
            laugh_sound.play()   
            last_laugh = now
            
        # Tempo da risada
        now_heal = pygame.time.get_ticks()
        elapsed_heal = now_heal - last_heal      
        if elapsed_heal > random.randint(25000, 35000):
            health = Health(blocks)
            all_sprites.add(health)
            healths.add(health)
            last_heal = now_heal
        
        # Quando jogar pedra
        if boss[0].state == SHOOT_RIGHT and boss[0].frame == 9 or boss[0].state == SHOOT_LEFT and boss[0].frame == 9:
            r = random.randint(5, 10)
            if boss[0].fire == False:
                for i in range (r):
                    #boss[0].fire = True
                    rock = Rock(boss[0].rect.centerx, boss[0].rect.top, boss[0])
                    all_sprites.add(rock)
                    rocks.add(rock)
                    boom_sound.play()
                boss[0].fire = True
            else:
                boss[0].fire == False
                
        # Verifica se houve colisão entre tiro e boss
        hits = pygame.sprite.spritecollide(boss[0], bullets, True, pygame.sprite.collide_mask)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            vida_boss -= 3
            if vida_boss == 0:
                boss[0].kill()
        
        hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_mask)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            grunt_sound.play()
            vida -= 1
            healthbar.frame -= 1
            
        hits = pygame.sprite.spritecollide(player, boss, False, pygame.sprite.collide_mask)
        for hit in hits: # Pode haver mais de um
            # O meteoro e destruido e precisa ser recriado
            if not player.damage:
                player.damage = True
                grunt_sound.play()
                vida -= 1
                healthbar.frame -= 1
                if player.speedx == 0 and player.speedy == 0 and boss[0].state == WALK_RIGHT:
                    player.speedx = 10
                    player.speedy = 10
                elif player.speedx == 0 and player.speedy == 0 and boss[0].state == WALK_LEFT:
                    player.speedx = -10
                    player.speedy = 10
                else:
                    player.speedx *= 1
                    player.speedy *= -1.5
        player.damage = False
            
            
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
            
        # Verifica se morreu
        if vida <= 0:
            pygame.mixer.music.stop()
            return GAME_OVER

        elif vida_boss == 0:
            pygame.mixer.music.stop()
            return UGH_SCENE
          
        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        lobosster()
        bosshealth(vida_boss)
        all_sprites.draw(screen)       
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()