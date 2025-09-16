import pygame
import random

from Cloud import Cloud
from Const import (
    SCREEN, BG, SMALL_CACTUS, LARGE_CACTUS, BIRD, SCREEN_WIDTH, SCREEN_HEIGHT,
    WHITE, BLACK, RED, GREEN,
    DEFAULT_FONT_PATH, FONT_SMALL, FONT_MEDIUM, FONT_LARGE, FONT_XL,
    TEXT_SCORE_PREFIX, TEXT_PRESS_START, TEXT_GAME_OVER,
    TEXT_YOUR_SCORE, TEXT_RESTART, TEXT_QUIT,
    RUNNING
)
from Dino import Dino
from Obstacles import SmallCactus, LargeCactus, Bird


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.font = pygame.font.Font(DEFAULT_FONT_PATH, FONT_SMALL)
        self.player = Dino()
        self.cloud = Cloud(self.game_speed)
        self.obstacles = []
        self.death_count = 0
        self.running = True

    def background(self):
        image_width = BG.get_width()
        SCREEN.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        SCREEN.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1

        text = self.font.render(TEXT_SCORE_PREFIX + str(self.points), True, BLACK)
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def spawn_obstacle(self):
        if len(self.obstacles) == 0:
            rand = random.randint(0, 2)
            if rand == 0:
                self.obstacles.append(SmallCactus(SMALL_CACTUS))
            elif rand == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                self.obstacles.append(Bird(BIRD))

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            SCREEN.fill(WHITE)
            userInput = pygame.key.get_pressed()

            self.player.update(userInput)
            self.player.draw(SCREEN)

            self.spawn_obstacle()

            for obstacle in list(self.obstacles):
                obstacle.update(self.game_speed)
                obstacle.draw(SCREEN)
                if self.player.dino_rect.colliderect(obstacle.rect):
                    pygame.time.delay(2000)
                    self.death_count += 1
                    self.running = False

                if obstacle.rect.x < -obstacle.rect.width:
                    self.obstacles.remove(obstacle)

            self.background()

            self.cloud.update(self.game_speed)
            self.cloud.draw(SCREEN)

            self.score()

            self.clock.tick(30)
            pygame.display.update()

        self.menu()

    def draw_text_center(self, text, size, color, y_offset=0):
        font = pygame.font.Font(DEFAULT_FONT_PATH, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        SCREEN.blit(text_surface, text_rect)

    def menu(self):
        run = True
        while run:
            SCREEN.fill(WHITE)
            if self.death_count == 0:
                self.draw_text_center(TEXT_PRESS_START, FONT_LARGE, BLACK)
            else:
                self.draw_text_center(TEXT_GAME_OVER, FONT_XL, RED, y_offset=-60)
                self.draw_text_center(f"{TEXT_YOUR_SCORE} {self.points}", FONT_LARGE, BLACK, y_offset=-20)

                # Botões
                restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
                quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50)
                pygame.draw.rect(SCREEN, GREEN, restart_button)
                pygame.draw.rect(SCREEN, RED, quit_button)
                self.draw_text_center(TEXT_RESTART, FONT_MEDIUM, BLACK, y_offset=40)
                self.draw_text_center(TEXT_QUIT, FONT_MEDIUM, BLACK, y_offset=110)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and self.death_count == 0:
                    self.reset()
                    self.run()
                if event.type == pygame.MOUSEBUTTONDOWN and self.death_count > 0:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_pos):
                        self.reset()
                        self.run()
                    elif quit_button.collidepoint(mouse_pos):
                        run = False
                        pygame.quit()
                        quit()

    def reset(self):
        self.game_speed = 20
        self.points = 0
        self.obstacles = []
        self.player = Dino()
        self.cloud = Cloud(self.game_speed)
        self.running = True
