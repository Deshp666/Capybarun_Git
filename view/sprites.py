import pygame as pg
from view.paths import PRIZE_PATH, BACKGROUND_PATH, CAPY_FOR_MAZE_PATH, CAPY_JUMP_PATH, BG_FOR_TEXT_PATH,\
    BG_RIGHT_PART, BG_LEFT_PART, BG_FINAL, BEAR_ANIMATION_PATHS, BIRD_ANIMATION_PATHS, CAPY_ANIMATION_PATH
pg.init()


def make_sprite(path: str) -> pg.Surface:
    image = pg.image.load(path).convert_alpha()
    return image


class Sprites:
    def __init__(self):
        self.background = make_sprite(BACKGROUND_PATH)
        self.capybara_in_maze = make_sprite(CAPY_FOR_MAZE_PATH)
        self.prize = make_sprite(PRIZE_PATH)
        self.capybara_jump = make_sprite(CAPY_JUMP_PATH)
        self.bg_for_text = make_sprite(BG_FOR_TEXT_PATH)
        self.bear_animation = [make_sprite(path) for path in BEAR_ANIMATION_PATHS]
        self.bird_animation = [make_sprite(path) for path in BIRD_ANIMATION_PATHS]
        self.capybara_animation = [make_sprite(path) for path in CAPY_ANIMATION_PATH]
        self.bg_final = make_sprite(BG_FINAL)
