import pygame as pg
from view.paths import *
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
        self.bear_animation = [make_sprite(path) for path in BEAR_ANIMATION_PATHS]
        self.bird_animation = [make_sprite(path) for path in BIRD_ANIMATION_PATHS]
        self.capybara_animation = [make_sprite(path) for path in CAPY_ANIMATION_PATH]
        self.bg_menu_final = make_sprite(BG_MENU_FINAL)


class StartSceneSprites:
    def __init__(self):
        self.background = create_background()


class RunnerSceneSprites:
    def __init__(self):
        self.first_background_part = create_background()
        self.second_background_part = create_background()
        self.capybara_animation = [make_sprite(path) for path in CAPY_ANIMATION_PATH]
        self.capybara_jump = make_sprite(CAPY_JUMP_PATH)
        self.bear_animation = [make_sprite(path) for path in BEAR_ANIMATION_PATHS]
        self.bird_animation = [make_sprite(path) for path in BIRD_ANIMATION_PATHS]


class MazeSceneSprites:
    def __init__(self):
        self.background = create_background()
        self.capybara_in_maze = make_sprite(CAPY_FOR_MAZE_PATH)
        self.prize = make_sprite(PRIZE_PATH)


class FinalSceneSprites:
    def __init__(self):
        self.background = create_background()
        self.bg_menu_final = make_sprite(BG_MENU_FINAL)


def create_background() -> pg.Surface:
    background = make_sprite(BACKGROUND_PATH)
    return background
