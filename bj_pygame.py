import pygame
import sys

pygame.init()

# display settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BlackJack")

# color variables
DARK_GREY = (30, 30, 30)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
DARK_GREEN = (2, 48, 32)

# clock for frame rate
clock = pygame.time.Clock()
FPS = 60

# game loop
running = True
while running:
    # game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic goes here

    # create border
    screen.fill(DARK_GREY)
    rect = pygame.Rect(10, 10, 780, 580)

    card = pygame.Rect(100, 100, 100, 150)
    pygame.draw.rect(screen, GREEN, rect, border_radius=20)
    pygame.draw.rect(screen, WHITE, card)
    pygame.draw.rect(screen, DARK_GREEN, rect, width=3, border_radius=20)

    pygame.display.flip()

    # cap frame rate
    clock.tick(FPS)

# quit game
pygame.quit()
sys.exit()
