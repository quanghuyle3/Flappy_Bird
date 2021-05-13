import pygame

class Bird:

    def __init__(self, fb_game):
        """A class to manage the main bird"""

        self.screen = fb_game.screen
        self.screen_rect = self.screen.get_rect()
        self.ground = fb_game.bottom_bg_rect.top
        self.stats = fb_game.stats

        self.image = pygame.image.load("images/bird.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.set_init_pos()

        self.image_copy = self.image
        self.rect_copy = self.rect

        # Get the size of bird to create appropriate space between pipes
        self.bird_width, self.bird_height = self.rect.size

        # Set up direction and rate to move the bird
        self.direction = 1
        self.rate = 0.1

        # Special rate for Rasing
        self.rate_up = 7.8

        # Set up the flag to raise bird
        self.allow_raise = 1

    # Set the initial position for bird
    def set_init_pos(self):
        self.angle = 1
        self.rect.right = self.stats.init_bird_right
        self.rect.y = self.stats.init_bird_y

        self.rect_copy = self.rect

    def update_bird(self):
        # Check direction and get new rate
        self._check_direction()

        # Pathway will look like a parabola y = a^2
        self.rect.y += self.direction * (self.rate ** 2)

        # Let bird move to the start position at beginning
        if self.rect.x < 200:
            self.rect.x += 1

        # Once the bird hit ground, game over -> prepare for new game
        if self.rect.bottom >= self.ground:
            self.rect.bottom = self.ground
            self.stats.falling_to_ground = False
            self.stats.game_active = False
            # Die sound
            die_sound = pygame.mixer.Sound("sound/sfx_die.wav")
            die_sound.play()

        self.image_copy, self.rect_copy = self._rotate(self.image, self.angle)
        self.rect_copy.x = self.rect.x
        self.rect_copy.y = self.rect.y

    def draw_bird(self):
        self.screen.blit(self.image_copy, self.rect_copy)

    def _rotate(self, image, angle):
        self.image_copy = pygame.transform.rotozoom(image, angle, 1)
        self.rect_copy = self.image_copy.get_rect()
        return self.image_copy, self.rect_copy

    def _check_direction(self):
        # Check if bird Falling Down
        if self.direction == 1:
            self.rate += 0.05
            # Angle
            if self.angle >= -35:
                self.angle -= 0.7
            if self.angle <= -35:
                self.angle = -35

        # Check if bird Rising Up
        elif self.direction == -1:
            self.rate = self.rate_up
            # Angle
            if self.angle < 0:
                self.angle = 5
            if self.angle <= 40:
                self.angle += 15
            if self.angle >= 40:
                self.angle = 40
