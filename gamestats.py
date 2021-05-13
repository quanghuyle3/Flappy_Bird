import pygame


class GameStats:
    """A class to manage all statistics"""

    def __init__(self, fb_game):
        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.read_high_score()
        self.res_score()
        self.res_game()

    def read_high_score(self):
        """Read high score from file"""
        with open("highscore.txt", "r") as fhandle:
            self.high_score = int(fhandle.readline().rstrip())
            """convert to integer to do some comparations later"""

    def write_high_score(self):
        """Write high score to file"""
        with open("highscore.txt", "w") as fhandle:
            fhandle.write(str(self.high_score))

    def res_score(self):
        """Initialize the score that could be called for new game"""
        self.score = 0

    def res_game(self):
        """Initialize properties that could be called for new game"""

        # Initial bird's position
        self.init_bird_right = 0
        self.init_bird_y = 400

        # Initialize the right of previous pipe as 0
        self.right_pre_pipe = 0

        # Game active
        self.game_active = False

        # Bird collides
        self.falling_to_ground = False
