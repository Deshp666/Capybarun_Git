import pygame
import sys
import random
from model.main import Timer
pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Moving Circle')

circle_color = (255, 0, 0)
circle_radius = 20
circle_x = width // 2
circle_y = height // 2
circle_speed = 0.2
timer = Timer(60)

def handle_event(circle_x, circle_y):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        circle_x -= circle_speed
    if keys[pygame.K_RIGHT]:
        circle_x += circle_speed
    if keys[pygame.K_UP]:
        circle_y -= circle_speed
    if keys[pygame.K_DOWN]:
        circle_y += circle_speed

while True:
    handle_event(circle_x, circle_y)

    # timer.update_time()
    # print(timer.get_time_to_print())

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)
    pygame.display.flip()
