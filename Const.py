import pygame
import os

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game OO")
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
BG = pygame.image.load(os.path.join("Assets/others", "Track.png"))

