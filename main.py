import pygame
import sys

from cart import Cart_Context

pygame.init()

GB_WIDTH, GB_HEIGHT = 160, 144

SCALE = 4

WINDOW_WIDTH, WINDOW_HEIGHT = GB_WIDTH * SCALE, GB_HEIGHT * SCALE

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vindleboy Emulator")

gb_screen = pygame.Surface((GB_WIDTH, GB_HEIGHT))

ctx = Cart_Context()
rom_loaded = ctx.cart_load('dmg-acid2.gb')

if not rom_loaded:
    print("Failed to load ROM")
    pygame.quit()
    sys.exit()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    gb_screen.fill((255, 255, 255))

    scaled_screen = pygame.transform.scale(gb_screen, (WINDOW_WIDTH, WINDOW_HEIGHT))

    screen.blit(scaled_screen, (0, 0))

    pygame.display.flip()

pygame.quit()
sys.exit()