import pygame as pg
from view.constants import GRAY_COLOR, WHITE_COLOR, PEACH_COLOR
pg.init()


class Text:
    def __init__(self, coordinates: tuple[int, int],
                 text: str,
                 font_size: int,
                 color: tuple[int, int, int] = GRAY_COLOR):
        self._coordinates: tuple[int, int] = coordinates
        self._text: str = text
        self._color: tuple[int, int, int] = color
        self._font: pg.font.Font = pg.font.Font('view/font/FRM3216x16.ttf', font_size)
        self._sprite: pg.Surface = self.make_image()
        self._rect: pg.Rect = self._sprite.get_rect(center=coordinates)

    def make_image(self) -> pg.Surface:
        image = self._font.render(self._text, True, self._color)
        return image

    def render(self, screen: pg.Surface):
        screen.blit(self._sprite, self._rect)


class Button(Text):
    def __init__(self, coordinates: tuple[int, int],
                 text: str,
                 size: tuple[int, int],
                 font_size: int, path: str):
        self._size: tuple[int, int] = size
        self._path: str = path
        super().__init__(coordinates, text, font_size)

    def make_image(self) -> pg.Surface:
        background = pg.image.load(self._path)
        background = pg.transform.scale(background, self._size)
        center_for_text = self._size[0] // 2, self._size[1] // 2
        text_color = WHITE_COLOR
        text = self._font.render(self._text, True, text_color)
        text_rect = text.get_rect(center=center_for_text)
        background.blit(text, text_rect)
        return background

    def collide_click(self, coordinates: tuple[int, int]) -> bool:
        return self._rect.collidepoint(coordinates)
