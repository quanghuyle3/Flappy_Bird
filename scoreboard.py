import pygame


class Scoreboard:
    """A class to present the scoreboard on screen"""

    def __init__(self, fb_game):
        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = fb_game.stats

        self.font_score = pygame.font.Font("font/04B_19.ttf", 70)
        self.font_statistic = pygame.font.Font("font/04B_19.ttf", 40)
        self.color = (255, 255, 255)

    def prep_score_statistic(self):
        # Main score during playing game
        self.score = str(self.stats.score)
        self.score_image = self.font_score.render(
            self.score, True, self.color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.centerx = self.screen_rect.centerx
        self.score_rect.y = 100

        # Your score
        self.your_score = "Your score: " + str(self.stats.score)
        self.your_score_image = self.font_statistic.render(
            self.your_score, True, self.color)
        self.your_score_rect = self.your_score_image.get_rect()
        self.your_score_rect.centerx = self.screen_rect.centerx
        self.your_score_rect.y = 230

        # High score
        self.high_score = "High score: " + str(self.stats.high_score)
        self.high_score_image = self.font_statistic.render(
            self.high_score, True, self.color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.y = 50

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)

    def show_statistic(self):
        self.screen.blit(self.your_score_image, self.your_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
