import pygame, time
from os import path
WIDTH = 1300
HEIGHT = 700
TILE_SIZE = 40
PLAYER_WIDTH = TILE_SIZE
PLAYER_HEIGHT = int(TILE_SIZE * 1.5)
FPS = 60 # Frames por segundo

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define a aceleração da gravidade
GRAVITY = 1.5
# Define a altura do chão
GROUND = HEIGHT * 5 // 6

QUIT = 0
FOREST_SCREEN = 6

line_space = 16
basicfont = pygame.font.SysFont('MorePerfectDOSVGA', 40)
snd_dir = path.join(path.dirname(__file__), 'sons')


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
font = pygame.font.SysFont("comicsansms", 72)
screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)

type_sound = pygame.mixer.Sound(path.join(snd_dir, 'type.wav'))
def text_ugh(string, pos):
    x, y = pos
    y = y*line_space ##shift text down by one line
    char = ''        ##new stringing that will take text one char at a time. Not the best variable name I know.
    letter = 0
    count = 0
    screen.fill(BLACK)
    pygame.display.flip()
    for i in range(len(string)):
        pygame.event.clear() ## this is very important if your event queue is not handled properly elsewhere. Alternativly pygame.event.pump() would work.
        time.sleep(0.1) ##change this for faster or slower text animation
        char = char + string[letter]
        text = basicfont.render(char, False, (2, 241, 16), (0, 0, 0)) #First pos is text color, second pos is background color
        textrect = text.get_rect(topleft=(x, y)) ## x, y's provided in function call. y coordinate amended by line height where needed
        screen.blit(text, textrect)
        pygame.display.update(textrect) ## update only the text just added without removing previous lines.
        type_sound.play()
        type_sound.play()
        count += 1
        letter += 1
        
    while True:
        # Ajusta a velocidade do jogo.
        clock.tick(FPS)
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                    return FOREST_SCREEN
                
        