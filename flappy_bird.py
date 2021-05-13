# This program simulates Flappy Bird game

import sys
import pygame
from bird import Bird
from pipes import Pipes
from gamestats import GameStats
import time
from scoreboard import Scoreboard

class Flappy_bird:

    def __init__(self):

        pygame.init()

        self.screen_width = 800
        self.screen_height = 800
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Flappy Bird")
        self.screen_rect = self.screen.get_rect()

        # Background
        self.top_bg = pygame.image.load("images/top_bg.png")
        self.top_bg_rect = self.top_bg.get_rect()

        self.bottom_bg = pygame.image.load(
            "images/bottom_bg.png")
        self.bottom_bg_rect = self.bottom_bg.get_rect()
        self.bottom_bg_rect.top = self.top_bg_rect.bottom - 5

        # Game title & tap
        self.title = pygame.image.load("images/title_tap.png")
        self.title_rect = self.title.get_rect()
        self.title_rect.x = 170
        self.title_rect.y = 100

        # Intances of this game
        self.pipes = pygame.sprite.Group()
        self.stats = GameStats(self)
        self.bird = Bird(self)
        self.scoreboard = Scoreboard(self)
        self.scoreboard.prep_score_statistic()

        # Pipe property
        self.ground_move_rate = 3
        self.pipe_collide = None

    def run_game(self):
        while True:
            self._check_event()

            # Get ready before new game
            if not self.stats.game_active and not self.stats.falling_to_ground:
                self._get_ready()

            # Let only the bird fall to ground once collides
            if self.stats.falling_to_ground:
                self._falling_bird()

            # PLaying
            if self.stats.game_active:
                self._check_to_add_pipes()
                self._falling_bird()
                self._update_pipes()
                self._check_bird_pipe_collision()
                self._check_adding_score()

            self._update_screen()

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

            # RAISE BIRD/ START NEW GAME
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Won't raise bird while it's falling down or just reach the ground
                if not self.stats.falling_to_ground and self.bird.rect.bottom != self.bottom_bg_rect.top:
                    # Activate the game
                    self.stats.game_active = True

                    # Raise the bird one at a time
                    if self.bird.allow_raise == 1:
                        # Change direction to raise up
                        self.bird.direction *= -1
                        # Update new position of bird
                        self.bird.update_bird()
                        # Restoring the initial falling rate after raising the bird
                        self.bird.rate = 0.1

                    # Restart score to 0
                    if self.bird.rect.right == 1:
                        self.stats.res_score()

                    self.scoreboard.prep_score_statistic()

                    # Wing sound
                    wing_sound = pygame.mixer.Sound("sound/sfx_wing.wav")
                    wing_sound.play()

    def _get_ready(self):
        # Save high score before new game
        self.stats.write_high_score()
        self.scoreboard.prep_score_statistic()

        # Delete all pipes
        if self.pipes.sprites():
            for pipe in self.pipes.sprites():
                self.pipes.remove(pipe)

        # Reset bird, properties
        self.stats.res_game()

        # Set the initial position for bird
        self.bird.set_init_pos()

    def _check_to_add_pipes(self):
        # Check if there's no pipe
        if not self.pipes.sprites():
            self._create_pipes()

        # Check if there are 3*width of bird space after the last pipe
        if self.pipes.sprites():
            # Get the list contains all pipes
            all_pipes = self.pipes.sprites()
            # take the last pipe
            last_pipe = all_pipes[-1]
            if (last_pipe.rect.right + 3 * self.bird.bird_width) < self.screen_width:
                self._create_pipes()

    def _create_pipes(self):

        if self.bird.rect.x >= 100:
            # Create pipe in the top
            pipe = Pipes(self, "top")
            self.pipes.add(pipe)
            current_bottom = pipe.rect.bottom

            # Create pipe in the bottom
            pipe = Pipes(self, "down", current_bottom)
            self.pipes.add(pipe)

    def _falling_bird(self):
        """Falling bird"""
        self.bird.direction = 1
        self.bird.allow_raise = 1
        self.bird.update_bird()

    def _update_pipes(self):
        """Update the pipes position"""
        if self.pipes.sprites():
            for pipe in self.pipes.sprites():
                pipe.update_pipes()
                # Delete the pipe once it go beyond screen
                if pipe.rect.right < 0:
                    self.pipes.remove(pipe)

    def _check_bird_pipe_collision(self):
        if pygame.sprite.spritecollideany(self.bird, self.pipes):
            # Find the specific pipe then set the eadge of bird and pipe match
            self.pipe_collide = pygame.sprite.spritecollideany(
                self.bird, self.pipes)

            # Hit sound
            hit_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
            hit_sound.play()

            # Set appropriate bird's position once collides within the pipe
            if (self.bird.rect.right - 2) > self.pipe_collide.rect.left and (self.bird.rect.right - 2) < self.pipe_collide.rect.right:
                if self.pipe_collide.rect.top < 0:
                    """This means the top pipe"""
                    self.bird.rect.top = self.pipe_collide.rect.bottom
                else:
                    """This means the bottom pipe"""
                    self.bird.rect.bottom = self.pipe_collide.rect.top

            # Stop any movement of pipe and bottom bg
            self.stats.game_active = False

            # Set the bird to falling mode
            self.stats.falling_to_ground = True

    def _check_adding_score(self):

        # Let the pos right of previous pipe move horizontally like a pipe
        if self.stats.right_pre_pipe != 0:
            self.stats.right_pre_pipe -= 2

        # Add score if bird pass the left of a pipe
        for pipe in self.pipes.sprites():
            if self.stats.right_pre_pipe < self.bird.rect.centerx and self.bird.rect.centerx in range(pipe.rect.left, pipe.rect.right):
                self.stats.score += 1
                self.stats.right_pre_pipe = pipe.rect.right

                # Point sound
                point_sound = pygame.mixer.Sound("sound/sfx_point.wav")
                point_sound.play()

                # Update high score if needed
                self._check_update_highscore()
                # Update new score on screen
                self.scoreboard.prep_score_statistic()
                break

    def _check_update_highscore(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score

    def _update_screen(self):
        # Draw top background
        self.screen.blit(self.top_bg, self.top_bg_rect)

        # Draw pipes
        for pipe in self.pipes.sprites():
            pipe.draw_pipes()

        # Draw the botom background moving
        if not self.stats.falling_to_ground:
            self.bottom_bg_rect.right -= int(self.ground_move_rate)
        if self.bottom_bg_rect.right <= self.screen_rect.right:
            self.bottom_bg_rect.left = 0
        self.screen.blit(self.bottom_bg, self.bottom_bg_rect)

        # Draw title and statistic before starting game
        if not self.stats.game_active and not self.stats.falling_to_ground:
            self.screen.blit(self.title, self.title_rect)
            self.scoreboard.show_statistic()
        else:
            # Draw score when playing game
            self.scoreboard.show_score()

        # Draw bird
        self.bird.draw_bird()
        if self.bird.rect.bottom == self.bottom_bg_rect.top:
            time.sleep(0.3)

        pygame.display.flip()

        # Stop a moment to see the collision
        if self.pipe_collide:
            time.sleep(0.3)
            self.pipe_collide = None


if __name__ == '__main__':
    fb = Flappy_bird()
    fb.run_game()
