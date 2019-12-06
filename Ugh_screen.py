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
GAME_OVER = 3
QUIT = 0

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

# Define ações do ugh
FLY = 9
# Define ações da bomba
ARMED = 10
EXPLODE = 11
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
    def __init__(self, x, y, blocks, ugh, player):
        
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
        self.ugh = ugh
        
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
            
# Classe Ugh que representa os meteoros
class Ugh(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        spritesheetugh = [pygame.image.load(path.join(img_dir, "ugh1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "ugh2.png")).convert(),
                          pygame.image.load(path.join(img_dir, "ugh3.png")).convert(),
                          pygame.image.load(path.join(img_dir, "ugh4.png")).convert()
                         ]
        
        i = 0
        while i < len(spritesheetugh):
            spritesheetugh[i] = pygame.transform.scale(spritesheetugh[i],(120,120))
            self.image = spritesheetugh[i]
            self.image.set_colorkey(BLACK)
            i += 1
        
        # Carregando a imagem de fundo.
        self.animations = {FLY:spritesheetugh[0:4]}
        
        
        # Define estado atual (que define qual animação deve ser mostrada)
        self.state = FLY
        # Define animação atual
        self.animation = self.animations[self.state]
        # Inicializa o primeiro quadro da animação
        self.frame = 0
        self.image = self.animation[self.frame]
        
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()
        
        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y + 600
        self.rect.centerx = x + 1200
        self.speedx = random.randint(-6, -3)
        self.speedy = random.randint(-6, -3)
        
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animação: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posição de ugh
    def update(self):
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
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            
        if self.rect.left < 0:
            self.speedx = random.randint(3, 6)
        elif self.rect.right >= WIDTH:
            self.speedx = random.randint(-6, -3)
        if self.rect.top <= 0:
            self.speedy = random.randint(3, 6)
        elif self.rect.bottom >= HEIGHT:
            self.speedy = random.randint(-6, -3)
            
        # Tenta andar em y
        # Atualiza a velocidade aplicando a aceleração da gravidade
        # Atualiza a posição y
        self.rect.y += self.speedy
        self.rect.x += self.speedx

# Classe Bomb que representa flechas
class Bomb(pygame.sprite.Sprite):
    
    # Construtor da classe.
    def __init__(self, x, y, ugh, blocks):
        
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)
        
        spritesheetbomb = [pygame.image.load(path.join(img_dir, "bomb-0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "bomb-1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "bomb-2.png")).convert(),
                          pygame.image.load(path.join(img_dir, "bomb-3.png")).convert(),
                          pygame.image.load(path.join(img_dir, "explosion-0.png")).convert(),
                          pygame.image.load(path.join(img_dir, "explosion-1.png")).convert(),
                          pygame.image.load(path.join(img_dir, "explosion-2.png")).convert(),
                          pygame.image.load(path.join(img_dir, "explosion-3.png")).convert(),
                          pygame.image.load(path.join(img_dir, "explosion-4.png")).convert(),
                          pygame.image.load(path.join(img_dir, "explosion-5.png")).convert()
                          ]
        i = 0
        while i < len(spritesheetbomb):
            if i < 4:
                spritesheetbomb[i] = pygame.transform.scale(spritesheetbomb[i],(20,26))
                self.image = spritesheetbomb[i]
                self.image.set_colorkey(BLACK)
            else:
                spritesheetbomb[i] = pygame.transform.scale(spritesheetbomb[i],(30,30))
                self.image = spritesheetbomb[i]
                self.image.set_colorkey(BLACK)
            i += 1
        
        # Carregando a imagem de fundo.
        self.animations = {ARMED:spritesheetbomb[0:4],
                           EXPLODE:spritesheetbomb[4:10]}
        
        self.morre = False
        self.state = ARMED 
        # Define estado atual (que define qual animaÃ§Ã£o deve ser mostrada)
        if self.state == ARMED:
            
        # Define animaÃ§Ã£o atual
            self.animation = self.animations[self.state]
            # Inicializa o primeiro quadro da animaÃ§Ã£o
            self.frame = 0
            self.image = self.animation[self.frame]
            # Detalhes sobre o posicionamento.
            self.rect = self.image.get_rect()
            
        if self.state == EXPLODE:
        # Define animaÃ§Ã£o atual
            self.animation = self.animations[self.state]
            # Inicializa o primeiro quadro da animaÃ§Ã£o
            self.frame = 0
            self.image = self.animation[self.frame]
            # Detalhes sobre o posicionamento.
            self.rect = self.image.get_rect()
            
        self.vida = 2

        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.bottom = y + 50
        self.rect.centerx = x
        self.speedx = 0
        self.speedy = 0
        self.blocks = blocks
        # Guarda o tick da primeira imagem
        self.last_update = pygame.time.get_ticks()

        # Controle de ticks de animaÃ§Ã£o: troca de imagem a cada self.frame_ticks milissegundos.
        self.frame_ticks = 100
        
    # Metodo que atualiza a posição da pedra
    def update(self):
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde a ultima mudanÃ§a de frame.
        elapsed_ticks = now - self.last_update

        if self.state == EXPLODE and self.frame == 5:
            self.morre = True
            
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
            self.mask = pygame.mask.from_surface(self.image)
            # Atualiza os detalhes de posicionamento
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.mask = pygame.mask.from_surface(self.image)
            
        if self.state == ARMED:
            self.speedy += GRAVITY
        elif self.state == EXPLODE:
            self.speedy = 0
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
            
# Inicialização do Pygame.
pygame.init()
pygame.mixer.init()


# Tamanho da tela.
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)

# Nome do jogo
pygame.display.set_caption("Tales of Jack")

# Variável para o ajuste de velocidade
clock = pygame.time.Clock()

# Carrega os sons do jogo
game_over_sound = pygame.mixer.Sound(path.join(snd_dir, 'game_over_bad_chest.wav'))
pew_sound = pygame.mixer.Sound(path.join(snd_dir, 'shot.ogg'))
grunt_sound = pygame.mixer.Sound(path.join(snd_dir, 'grunt.wav'))  
victory_sound = pygame.mixer.Sound(path.join(snd_dir, 'victory.ogg'))
boom_sound = pygame.mixer.Sound(path.join(snd_dir, 'boom.ogg'))
heal_sound = pygame.mixer.Sound(path.join(snd_dir, 'healspell.ogg'))
bang_sound = pygame.mixer.Sound(path.join(snd_dir, 'bang.ogg'))
drop_sound = pygame.mixer.Sound(path.join(snd_dir, 'dropbomb.ogg'))

def ughhealth(vida_ugh):
    if vida_ugh > 500:
        vida_ugh_color = GREEN
    elif vida_ugh > 250:
        vida_ugh_color = YELLOW
    else:
        vida_ugh_color = RED   
    pygame.draw.rect(screen, vida_ugh_color, (WIDTH - vida_ugh, 150, vida_ugh, 10))

ugh_name = pygame.image.load(path.join(img_dir, 'ugh.png')).convert()
def ughname():
    global WIDTH, HEIGHT
    x =  (WIDTH - 160)
    y = (HEIGHT * 0.06)
    ugh_name.set_colorkey(BLACK)
    screen.blit(ugh_name, (x,y))
    
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
background = pygame.image.load(path.join(img_dir, 'forest-background.png')).convert()
background_rect = background.get_rect()

# Comando para evitar travamentos.
def ugh_screen(screen):
    
    # Loop principal.
    pygame.mixer.music.load(path.join(snd_dir, 'forest.ogg'))
    pygame.mixer.music.set_volume(0.7)
    vida = 5
    vida_ugh = 750
    running = True
    pygame.mixer.music.play(loops=-1)
    last_heal = 0    
    last_bomb = 0        
    row = len(MAP2)
    column = len(MAP2[0])
        # Sprites de block são aqueles que impedem o movimento do jogador
    blocks = pygame.sprite.Group()
    
    # Cria Jack. O construtor será chamado automaticamente.
    player = Player(row, column, blocks)
    ughs = [Ugh(row, column)]
    # Cria barra de vida. O construtor será chamado automaticamente.
    healthbar = HealthBar()
    
    # Cria um grupo de sprites e adiciona Jack.
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    #all_sprites.add(ugh)
    all_sprites.add(ughs)
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
    # Cria um grupo só de itens health
    healths = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    
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
                    bullet = Bullet(player.rect.centerx, player.rect.top, blocks, ughs, player)
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
        
        # Tempo da bomba
        now_bomb = pygame.time.get_ticks()
        elapsed_bomb = now_heal - last_bomb
        if elapsed_bomb > random.randint(3000, 5000):
            bomb = Bomb(ughs[0].rect.x + 60, ughs[0].rect.y + 60, ughs[0], blocks)
            all_sprites.add(bomb)
            bombs.add(bomb)
            last_bomb = now_bomb
            drop_sound.stop()
            drop_sound.play()
            
        # Verifica se houve colisão entre tiro e ughs
        hits = pygame.sprite.spritecollide(ughs[0], bullets, True, pygame.sprite.collide_mask)
        for hit in hits: 
            vida_ugh -= 10
            if vida_ugh == 0:
                ughs[0].kill()
                
        # Verifica se houve colisÃ£o entre tiro e meteoro
        hits = pygame.sprite.groupcollide(bombs, bullets, False, True, pygame.sprite.collide_mask)
        for bomb in hits:
            bomb.vida -= 1
            if bomb.vida == 0:
                bang_sound.play()
                bomb.state = EXPLODE
        for bomb in bombs:
            if bomb.morre == True:
                bomb.kill()
            
        hits = pygame.sprite.spritecollide(player, bombs, False, pygame.sprite.collide_mask)
        for bomb in hits:
            if bomb.state == ARMED:
                bomb.vida == 0
                bomb.state = EXPLODE
                bang_sound.play()
                grunt_sound.play()
                vida -= 2
                healthbar.frame -= 2
        for bomb in bombs:
            if bomb.morre == True:
                bomb.kill()
            
        hits = pygame.sprite.spritecollide(player, healths, True, pygame.sprite.collide_mask)
        for hit in hits:
            if vida < 4:
                vida += 2        
                healthbar.frame += 2
            elif vida < 5:
                vida += 1
                healthbar.frame += 1
            else:
                vida == 5
            heal_sound.play()
            
        hits = pygame.sprite.spritecollide(player, ughs, False, pygame.sprite.collide_mask)
        for hit in hits:
            grunt_sound.play()
            vida -= 1
            healthbar.frame -= 1
            player.rect.x = ughs[0].rect.x + 20
            player.rect.y = ughs[0].rect.y - 80
            player.speedy = -15

        # Verifica se morreu
        if vida <= 0:
            return GAME_OVER
            
        if vida_ugh <= 0:
            pygame.mixer.music.stop()
            victory = pygame.image.load(path.join(img_dir, "victory.jpg")).convert()
            screen.fill(BLACK)
            screen.blit(victory,[0,0])
            pygame.display.update()
            victory_sound.play()    
            time.sleep(10)           
            return QUIT
        
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        ughhealth(vida_ugh)
        ughname()
        all_sprites.draw(screen)       
        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()