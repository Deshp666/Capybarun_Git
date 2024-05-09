# import pygame
# import sys
# import random
# import time
# from model.main import Timer
# from view.buttons import Text
# pygame.init()
#
# width, height = 800, 600
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption('Moving Circle')
# clock = pygame.time.Clock()
#
# circle_color = (255, 0, 0)
# circle_radius = 20
# circle_x = width // 2
# circle_y = height // 2
# circle_speed = 3
# timer = Timer(3)
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#         circle_x -= circle_speed
#     if keys[pygame.K_RIGHT]:
#         circle_x += circle_speed
#     if keys[pygame.K_UP]:
#         circle_y -= circle_speed
#     if keys[pygame.K_DOWN]:
#         circle_y += circle_speed
#     text = Text((100, 100), f"{timer.get_for_print()}", 10)
#     screen.fill((100, 40, 142))
#     text.render(screen)
#     if timer.update() is False:
#         break
#
#     # timer.update_time()
#     # print(timer.get_time_to_print())
#     clock.tick(60)
#
#     pygame.draw.circle(screen, circle_color, (circle_x, circle_y), circle_radius)
#     pygame.display.update()
ds = ['1' for i in range(2) for j in range(3)]
print(ds)