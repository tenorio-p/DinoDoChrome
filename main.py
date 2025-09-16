import pygame
pygame.init()  # <-- Adicione isso ANTES de criar o Game()

from Game import Game

if __name__ == "__main__":
    game = Game()
    game.menu()
