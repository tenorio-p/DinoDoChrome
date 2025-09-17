import pygame
import random
import os

from Cloud import Cloud
from Const import (
    SCREEN, BG_DAY, BG_NIGHT, SMALL_CACTUS, LARGE_CACTUS, BIRD, SCREEN_WIDTH, SCREEN_HEIGHT,
    WHITE, BLACK, RED, GREEN,
    DEFAULT_FONT_PATH, FONT_SMALL, FONT_MEDIUM, FONT_LARGE, FONT_XL,
    TEXT_SCORE_PREFIX, TEXT_PRESS_START, TEXT_GAME_OVER,
    TEXT_YOUR_SCORE, TEXT_RESTART, TEXT_QUIT,
    RUNNING, DEATH_SOUND, SCORE_SOUND
)
from Dino import Dino
from Obstacles import SmallCactus, LargeCactus, Bird


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.bg_day = BG_DAY
        self.bg_night = BG_NIGHT
        self.is_night = False
        self.bg_current = self.bg_day  # Começa no modo dia
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
        self.high_score = self.load_high_score()  # Carrega pontuação máxima do arquivo

    def load_high_score(self):
        if not os.path.exists("highscore.txt"):
            with open("highscore.txt", "w") as f:
                f.write("0")
            return 0
        with open("highscore.txt", "r") as f:
            return int(f.read())

    def save_high_score(self):
        if self.points > self.high_score:
            self.high_score = self.points
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

    def background(self):
        if self.is_night:
            SCREEN.fill((20, 20, 40))  # fundo azul escuro para noite
        else:
            SCREEN.fill(WHITE)  # fundo branco para dia

        # Desenhar o chão que se move
        image_width = self.bg_current.get_width()
        SCREEN.blit(self.bg_current, (self.x_pos_bg, self.y_pos_bg))
        SCREEN.blit(self.bg_current, (image_width + self.x_pos_bg, self.y_pos_bg))

        # Resetar posição do chão quando sair da tela
        if self.x_pos_bg <= -image_width:
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def score(self):
        self.points += 1

        if self.points % 100 == 0:
            SCORE_SOUND.play()  # toca som de checkpoint
            self.game_speed += 1
        # Aumenta velocidade a cada 100 pontos
        if self.points % 100 == 0:
            self.game_speed += 1

        # Alterna entre dia e noite a cada 500 pontos
        if self.points % 500 == 0:
            self.is_night = not self.is_night
            self.bg_current = self.bg_night if self.is_night else self.bg_day

        text_color = WHITE if self.is_night else BLACK
        text = self.font.render(TEXT_SCORE_PREFIX + str(self.points), True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (1000, 40)
        SCREEN.blit(text, text_rect)

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

            userInput = pygame.key.get_pressed()

            # 1️⃣ Pintar fundo de acordo com o modo
            if self.is_night:
                SCREEN.fill((20, 20, 40))  # fundo noite
            else:
                SCREEN.fill(WHITE)  # fundo dia

            # 2️⃣ Desenhar o chão
            self.background()

            # 3️⃣ Atualizar e desenhar nuvens
            self.cloud.update(self.game_speed)
            self.cloud.draw(SCREEN)

            # 4️⃣ Atualizar e desenhar obstáculos
            self.spawn_obstacle()
            for obstacle in list(self.obstacles):
                obstacle.update(self.game_speed)
                obstacle.draw(SCREEN)
                # Checar colisão
                if self.player.dino_rect.colliderect(obstacle.rect):
                    DEATH_SOUND.play()  # toca som de colisão
                    pygame.time.delay(2000)
                    self.death_count += 1
                    self.save_high_score()
                    self.running = False

                # Remover obstáculos que saíram da tela
                if obstacle.rect.x < -obstacle.rect.width:
                    self.obstacles.remove(obstacle)

            # 5️⃣ Atualizar e desenhar o dinossauro
            self.player.update(userInput)
            self.player.draw(SCREEN)

            # 6️⃣ Mostrar pontuação
            self.score()

            # 7️⃣ Atualizar tela e controlar FPS
            pygame.display.update()
            self.clock.tick(30)

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
                self.draw_text_center(f"Recorde: {self.high_score}", FONT_LARGE, BLACK, y_offset=20)

                # Botões
                restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 60, 200, 50)
                quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 130, 200, 50)
                pygame.draw.rect(SCREEN, GREEN, restart_button)
                pygame.draw.rect(SCREEN, RED, quit_button)
                self.draw_text_center(TEXT_RESTART, FONT_MEDIUM, BLACK, y_offset=80)
                self.draw_text_center(TEXT_QUIT, FONT_MEDIUM, BLACK, y_offset=150)

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
