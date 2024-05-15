import pygame as pg
from view.constants import GRAY_COLOR, WHITE_COLOR, PEACH_COLOR
pg.init()


class Text:
    def __init__(self, coordinates: (int, int), text: str, font_size: int, color=GRAY_COLOR):
        self._coordinates = coordinates
        self._text = text
        self._color = color
        self._font = pg.font.Font('view/font/FRM3216x16.ttf', font_size)
        self._sprite = self.make_image()
        self._rect = self._sprite.get_rect(center=coordinates)

    def make_image(self) -> pg.Surface:
        image = self._font.render(self._text, True, self._color)
        return image

    def render(self, screen: pg.Surface):
        screen.blit(self._sprite, self._rect)


class Button(Text):
    def __init__(self, coordinates: (int, int), text: str, size: (int, int), font_size: int, path: str):
        self._size = size
        self._path = path
        super().__init__(coordinates, text, font_size)

    def make_image(self) -> pg.Surface:
        image = pg.image.load(self._path)
        image = pg.transform.scale(image, self._size)
        center_for_text = self._size[0] // 2, self._size[1] // 2
        text_color = WHITE_COLOR
        text = self._font.render(self._text, 1, text_color)
        text_rect = text.get_rect(center=center_for_text)
        image.blit(text, text_rect)
        return image

    def collide_click(self, coordinates: (int, int)) -> bool:
        return self._rect.collidepoint(coordinates)
