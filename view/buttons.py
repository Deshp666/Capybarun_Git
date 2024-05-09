import pygame as pg
from view.constants import GRAY_COLOR, WHITE_COLOR, PEACH_COLOR
pg.init()


class Text:
    def __init__(self, coordinates: (int, int), text: str, font_size: int, color=GRAY_COLOR):
        self.coordinates = coordinates
        self.text = text
        self.color = color
        self.font = pg.font.Font('view/font/FRM3216x16.ttf', font_size)
        self.sprite = self.make_image()
        self.rect = self.sprite.get_rect(center=coordinates)

    def make_image(self) -> pg.Surface:
        image = self.font.render(self.text, True, self.color)
        return image

    def render(self, screen: pg.Surface):
        screen.blit(self.sprite, self.rect)


class Button(Text):
    def __init__(self, coordinates: (int, int), text: str, size: (int, int), font_size: int):
        self.size = size
        super().__init__(coordinates, text, font_size)

    def make_image(self) -> pg.Surface:
        image = pg.Surface(self.size)
        center_for_text = self.size[0] // 2, self.size[1] // 2
        back_ground_color = PEACH_COLOR
        text_color = WHITE_COLOR
        stroke_color = GRAY_COLOR
        image.fill(stroke_color)
        stroke_size = 3
        rect_size = self.size[0] - stroke_size * 2, self.size[1] - stroke_size * 2
        pg.draw.rect(image, back_ground_color, (stroke_size, stroke_size, self.size[0] - stroke_size * 2, self.size[1] - stroke_size * 2))
        text = self.font.render(self.text, 1, text_color)
        text_rect = text.get_rect(center=center_for_text)
        image.blit(text, text_rect)
        return image

    def collide_click(self, coordinates: (int, int)) -> bool:
        return self.rect.collidepoint(coordinates)


class MusicButton(Button):
    def __init__(self):
        pass