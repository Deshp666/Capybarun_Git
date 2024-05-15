import pygame as pg
from view.paths import PRIZE_PATH, BACKGROUND_PATH, FOURTH_POS_BEAR_PATH, FOURTH_POS_BIRD_PATH, THIRD_POS_BEAR_PATH, \
    THIRD_POS_BIRD_PATH, FIRST_POS_BEAR_PATH, FIRST_POS_BIRD_PATH, SECOND_POS_BEAR_PATH, SECOND_POS_BIRD_PATH, \
    CAPY_WALK_FIRST_PATH, CAPY_FOR_MAZE_PATH, CAPY_JUMP_PATH, CAPY_WALK_SECOND_PATH, BG_FOR_TEXT_PATH, BG_RIGHT_PART, \
    BG_LEFT_PART
pg.init()


def make_image(path: str) -> pg.Surface:
    image = pg.image.load(path).convert_alpha()
    return image


class Sprites:
    def __init__(self):
        self.background = make_image(BACKGROUND_PATH)
        self.capybara_in_maze = make_image(CAPY_FOR_MAZE_PATH)
        self.prize = make_image(PRIZE_PATH)
        self.capybara_walk_1 = make_image(CAPY_WALK_FIRST_PATH)
        self.capybara_walk_2 = make_image(CAPY_WALK_SECOND_PATH)
        self.capybara_jump = make_image(CAPY_JUMP_PATH)
        self.bear_pos_1 = make_image(FIRST_POS_BEAR_PATH)
        self.bear_pos_2 = make_image(SECOND_POS_BEAR_PATH)
        self.bear_pos_3 = make_image(THIRD_POS_BEAR_PATH)
        self.bear_pos_4 = make_image(FOURTH_POS_BEAR_PATH)
        self.bird_pos_1 = make_image(FIRST_POS_BIRD_PATH)
        self.bird_pos_2 = make_image(SECOND_POS_BIRD_PATH)
        self.bird_pos_3 = make_image(THIRD_POS_BIRD_PATH)
        self.bird_pos_4 = make_image(FOURTH_POS_BIRD_PATH)
        self.bg_for_text = make_image(BG_FOR_TEXT_PATH)
        self.bear_animation = [self.bear_pos_1, self.bear_pos_2, self.bear_pos_3, self.bear_pos_4]
        self.bird_animation = [self.bird_pos_1, self.bird_pos_2, self.bird_pos_3, self.bird_pos_4]
        self.capybara_animation = [self.capybara_walk_1, self.capybara_walk_2]
        self.bg_right_part = make_image(BG_RIGHT_PART)
        self.bg_left_part = make_image(BG_LEFT_PART)