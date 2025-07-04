import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 140
PIPE_FREQUENCY = 1500  # milliseconds
GROUND_HEIGHT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (180, 0, 0)
DARK_RED = (120, 0, 0)
YELLOW = (255, 220, 40)
DARK_YELLOW = (200, 180, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (100, 50, 10)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
LIGHT_GREEN = (120, 255, 120)
PIPE_SHADOW = (0, 120, 0)
PIPE_HIGHLIGHT = (180, 255, 180)
SKY_BLUE = (99, 204, 255)
CITY_BLUE = (44, 152, 199)
CITY_DARK = (36, 120, 158)
BUSH_GREEN = (34, 177, 76)
BUSH_DARK = (24, 120, 50)
WINDOW_YELLOW = (255, 221, 51)
GROUND_STRIPE = (170, 220, 120)
GROUND_STRIPE_DARK = (120, 180, 80)
STONE_GRAY = (180, 180, 180)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Angry Bird')
clock = pygame.time.Clock()

def draw_pixel_bird(surface, x, y):
    # Draw a pixel-art angry bird at (x, y) (centered)
    px = x - 16
    py = y - 16
    # Body (red)
    pygame.draw.rect(surface, RED, (px+6, py+8, 20, 16))
    pygame.draw.rect(surface, RED, (px+10, py+6, 12, 4))
    pygame.draw.rect(surface, RED, (px+8, py+6, 2, 2))
    pygame.draw.rect(surface, DARK_RED, (px+6, py+8, 4, 4))
    # Face (white)
    pygame.draw.rect(surface, WHITE, (px+14, py+14, 8, 6))
    pygame.draw.rect(surface, WHITE, (px+10, py+16, 16, 4))
    # Beak (yellow)
    pygame.draw.rect(surface, YELLOW, (px+18, py+18, 6, 4))
    pygame.draw.rect(surface, DARK_YELLOW, (px+20, py+20, 4, 2))
    # Eyes (black)
    pygame.draw.rect(surface, BLACK, (px+16, py+16, 2, 2))
    pygame.draw.rect(surface, BLACK, (px+22, py+16, 2, 2))
    # Eyebrows (black)
    pygame.draw.rect(surface, BLACK, (px+14, py+13, 4, 1))
    pygame.draw.rect(surface, BLACK, (px+20, py+13, 4, 1))
    # Belly (light brown)
    pygame.draw.rect(surface, (220, 200, 160), (px+14, py+20, 8, 4))
    # Outline (black, rough)
    pygame.draw.rect(surface, BLACK, (px+6, py+8, 20, 1))
    pygame.draw.rect(surface, BLACK, (px+6, py+8, 1, 16))
    pygame.draw.rect(surface, BLACK, (px+25, py+8, 1, 16))
    pygame.draw.rect(surface, BLACK, (px+6, py+23, 20, 1))
    # Tail (black)
    pygame.draw.rect(surface, BLACK, (px+4, py+14, 2, 2))
    pygame.draw.rect(surface, BLACK, (px+3, py+16, 2, 2))
    pygame.draw.rect(surface, BLACK, (px+5, py+18, 2, 2))

def draw_pixel_background(surface):
    surface.fill(SKY_BLUE)

def draw_pixel_ground(surface):
    # Striped ground pattern
    for x in range(0, SCREEN_WIDTH, 16):
        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_HEIGHT - GROUND_HEIGHT + 24, 8):
            color = GROUND_STRIPE if (x//16 + y//8) % 2 == 0 else GROUND_STRIPE_DARK
            pygame.draw.rect(surface, color, (x, y, 16, 8))
    # Top border
    pygame.draw.rect(surface, (200, 200, 120), (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, 4))
    # Bottom dirt
    for x in range(0, SCREEN_WIDTH, 8):
        for y in range(SCREEN_HEIGHT - GROUND_HEIGHT + 24, SCREEN_HEIGHT, 8):
            pygame.draw.rect(surface, BROWN, (x, y, 8, 8))
            pygame.draw.rect(surface, DARK_BROWN, (x, y, 8, 2))

def draw_pixel_pipe(surface, x, top_height, bottom_height, width):
    # Top pipe body
    for y in range(0, top_height-16, 8):
        pygame.draw.rect(surface, GREEN, (x, y, width, 8))
        pygame.draw.rect(surface, PIPE_SHADOW, (x, y, 6, 8))
        pygame.draw.rect(surface, PIPE_HIGHLIGHT, (x+width-6, y, 6, 8))
    # Top cap
    pygame.draw.rect(surface, DARK_GREEN, (x-4, top_height-16, width+8, 16))
    pygame.draw.rect(surface, PIPE_HIGHLIGHT, (x+width-8, top_height-16, 8, 16))
    # Bottom pipe body
    for y in range(SCREEN_HEIGHT - GROUND_HEIGHT - bottom_height + 16, SCREEN_HEIGHT - GROUND_HEIGHT, 8):
        pygame.draw.rect(surface, GREEN, (x, y, width, 8))
        pygame.draw.rect(surface, PIPE_SHADOW, (x, y, 6, 8))
        pygame.draw.rect(surface, PIPE_HIGHLIGHT, (x+width-6, y, 6, 8))
    # Bottom cap
    pygame.draw.rect(surface, DARK_GREEN, (x-4, SCREEN_HEIGHT - GROUND_HEIGHT - bottom_height, width+8, 16))
    pygame.draw.rect(surface, PIPE_HIGHLIGHT, (x+width-8, SCREEN_HEIGHT - GROUND_HEIGHT - bottom_height, 8, 16))

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rotation = 0
        self.size = 32
        self.rect = pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

    def flap(self):
        self.velocity = FLAP_STRENGTH
        self.rotation = 30

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.velocity < 0:
            self.rotation = 30
        else:
            self.rotation = max(-90, self.rotation - 3)
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        draw_pixel_bird(screen, self.x, self.y)

class Pipe:
    def __init__(self):
        self.width = random.choice([48, 64, 80])
        self.gap_y = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - 150)
        self.gap = random.choice([120, 140, 160])
        self.x = SCREEN_WIDTH
        self.passed = False
        self.top_height = self.gap_y - self.gap // 2
        self.bottom_height = SCREEN_HEIGHT - (self.gap_y + self.gap // 2) - GROUND_HEIGHT

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        draw_pixel_pipe(screen, self.x, self.top_height, self.bottom_height, self.width)

    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, SCREEN_HEIGHT - GROUND_HEIGHT - self.bottom_height, self.width, self.bottom_height)
        return top_rect, bottom_rect

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.high_score = 0
        self.game_active = False
        self.last_pipe = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 48)

    def spawn_pipe(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe > PIPE_FREQUENCY:
            self.pipes.append(Pipe())
            self.last_pipe = current_time

    def update(self):
        if self.game_active:
            self.bird.update()
            self.spawn_pipe()
            for pipe in self.pipes[:]:
                pipe.update()
                if not pipe.passed and pipe.x < self.bird.x:
                    self.score += 1
                    pipe.passed = True
                if pipe.x < -100:
                    self.pipes.remove(pipe)
                top_rect, bottom_rect = pipe.get_rects()
                if self.bird.rect.colliderect(top_rect) or self.bird.rect.colliderect(bottom_rect):
                    self.game_over()
            if self.bird.y < 0 or self.bird.y > SCREEN_HEIGHT - GROUND_HEIGHT:
                self.game_over()

    def draw(self):
        draw_pixel_background(screen)
        if self.game_active:
            for pipe in self.pipes:
                pipe.draw(screen)
            self.bird.draw(screen)
            score_text = self.font.render(str(self.score), True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        else:
            if self.score == 0:
                message = "Press SPACE to Start"
            else:
                message = "Game Over - Press SPACE to Restart"
            text = self.font.render(message, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
            high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
            screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        draw_pixel_ground(screen)

    def game_over(self):
        self.game_active = False
        if self.score > self.high_score:
            self.high_score = self.score

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_active = True

def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game.game_active:
                        game.reset()
                    else:
                        game.bird.flap()
        game.update()
        game.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
