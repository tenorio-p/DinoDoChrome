import pygame
pygame.init()
import random

from Cloud import Cloud
from Const import SCREEN, BG, SMALL_CACTUS, LARGE_CACTUS, BIRD, SCREEN_WIDTH, SCREEN_HEIGHT, RUNNING
from Dino import Dino
from Obstacles import SmallCactus, LargeCactus, Bird




class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.points = 0
        self.font = pygame.font.Font('freesansbold.ttf', 20)
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

        text = self.font.render("Score: " + str(self.points), True, (0, 0, 0))
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

            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()

            self.player.update(userInput)
            self.player.draw(SCREEN)

            self.spawn_obstacle()

            for obstacle in list(self.obstacles):  # iterar sobre cópia para remover com segurança
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
        font = pygame.font.Font('freesansbold.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
        SCREEN.blit(text_surface, text_rect)

    def menu(self):
        run = True
        while run:
            SCREEN.fill((255, 255, 255))
            if self.death_count == 0:
                self.draw_text_center("Pressione qualquer tecla para começar", 30, (0, 0, 0))
            else:
                self.draw_text_center("Game Over", 40, (255, 0, 0), y_offset=-60)
                self.draw_text_center(f"Sua pontuação: {self.points}", 30, (0, 0, 0), y_offset=-20)
                # Botões
                restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50)
                quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 90, 200, 50)
                pygame.draw.rect(SCREEN, (0, 255, 0), restart_button)
                pygame.draw.rect(SCREEN, (255, 0, 0), quit_button)
                self.draw_text_center("Reiniciar", 25, (0, 0, 0), y_offset=40)
                self.draw_text_center("Sair", 25, (0, 0, 0), y_offset=110)
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
