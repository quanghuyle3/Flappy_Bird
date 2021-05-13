import pygame
from pygame.sprite import Sprite
import random


class Pipes(Sprite):
    """A class to manage the pipes moving horizontally"""

    def __init__(self, fb_game, pos, bottom_pos=0):
        super().__init__()
        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.bird = fb_game.bird

        self.pipe_move_rate = fb_game.ground_move_rate

        self.image = pygame.image.load("images/pipes.png").convert_alpha()

        # For the top pipe
        if pos == "top":
            self.rect = self.image.get_rect()
            self.rect.bottom = random.randrange(50, 450)
            self.rect.left = self.screen_rect.right

        # For the bottom pipe
        if pos == "down":
            self.image = pygame.transform.flip(
                self.image, False, True)
            self.rect = self.image.get_rect()
            self.rect.top = bottom_pos + (4 * self.bird.bird_height)
            self.rect.left = self.screen_rect.right

    def update_pipes(self):
        self.rect.x -= self.pipe_move_rate

    def draw_pipes(self):
        self.screen.blit(self.image, self.rect)
