import pygame, math, random, time
from os import path
img_dir = path.join(path.dirname(__file__), 'imagens')
snd_dir = path.join(path.dirname(__file__), 'sons')
# Dados gerais do jogo.
WIDTH = 1300 # Largura da tela
HEIGHT = 700 # Altura da tela
TILE_SIZE = 40 # Tamanho de cada tile (cada tile eh um quadrado)
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = int(TILE_SIZE * 1.5)
FPS = 60 # Frames por segundo
TELA_INICIAL = 4
TELA_AJUDA = 5
BOSS_SCENE = 8
QUIT = 0
# Define algumas variaveis com as cores basicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
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
background = pygame.image.load(path.join(img_dir, 'init.png')).convert()
background_rect = background.get_rect()


click_sound = pygame.mixer.Sound(path.join(snd_dir, 'click.ogg'))
    
def tela_inicial(screen):
    running = True
    is_playing = pygame.mixer.music.get_busy()
    if is_playing == False:
        pygame.mixer.music.load(path.join(snd_dir, 'menu.mp3'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_q:
                    return QUIT
            # Verifica se foi fechado.
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 70 and pos[0] < 500 and pos[1] > 400 and pos[1] < 600:
                    click_sound.play()
                    pygame.mixer.music.stop()
                    return BOSS_SCENE
                elif pos[0] > 755 and pos[0] < 1200 and pos[1] > 400 and pos[1] < 600:
                    click_sound.play()
                    return TELA_AJUDA
                
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()
        
    pygame.mixer.music.stop
        
def tela_ajuda(screen):
    background = pygame.image.load(path.join(img_dir, 'ajuda.png')).convert()
    background_rect = background.get_rect()
    
    running = True
    
    while running:
        
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_q:
                    return QUIT
            # Verifica se foi fechado.
            pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > 1000 and pos[0] < 1300 and pos[1] > 580 and pos[1] < 700:
                    click_sound.play()
                    return TELA_INICIAL
                
        screen.fill(BLACK)
        screen.blit(background, background_rect)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()