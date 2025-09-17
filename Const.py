import pygame
import os

# Tela
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game OO")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Fontes
DEFAULT_FONT_PATH = 'freesansbold.ttf'
FONT_SMALL = 20
FONT_MEDIUM = 25
FONT_LARGE = 30
FONT_XL = 40

# Sons
JUMP_SOUND = pygame.mixer.Sound(os.path.join("Assets/sounds", "jump.wav"))
DEATH_SOUND = pygame.mixer.Sound(os.path.join("Assets/sounds", "hit.wav"))
SCORE_SOUND = pygame.mixer.Sound(os.path.join("Assets/sounds", "score.wav"))


# Textos
TEXT_PRESS_START = "Pressione qualquer tecla para começar"
TEXT_GAME_OVER = "Game Over"
TEXT_SCORE_PREFIX = "Score: "
TEXT_YOUR_SCORE = "Sua pontuação: "
TEXT_RESTART = "Reiniciar"
TEXT_QUIT = "Sair"

# Sprites
RUNNING = [pygame.image.load(os.path.join("Assets/dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/dino", "DinoJump.png"))

DUCKING = [pygame.image.load(os.path.join("Assets/dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/others", "cloud.png"))
BG_DAY = pygame.image.load(os.path.join("Assets/others", "TrackDay.png"))
BG_NIGHT = pygame.image.load(os.path.join("Assets/others", "TrackNight.png"))
