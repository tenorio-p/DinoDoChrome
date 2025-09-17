import pygame
from Const import DUCKING, RUNNING, JUMPING, JUMP_SOUND

class Dino:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        # Sprites
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        # Estados
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        # Passos e velocidade
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL

        # Sprite inicial
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        # Atualizar estado
        if self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.duck()
        else:
            self.run()

        # Reset do step_index
        if self.step_index >= 10:
            self.step_index = 0

        # Detectar entrada do jogador
        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            JUMP_SOUND.play()
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not self.dino_jump and not userInput[pygame.K_DOWN]:
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8

        # Chegou ao chão
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL
            self.dino_rect.y = self.Y_POS  # Garantir posição correta ao aterrissar

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
