from view.main import SceneRender
from view.constants import WIDTH, HEIGHT, FPS, CAPTION, MAZE_WIDTH, MAZE_HEIGHT, MAZE_INDENTATION_Y, \
    MAZE_INDENTATION_X
from view.buttons import Button
from model.main import Model
from abc import abstractmethod
import pygame as pg
import sys
from enum import Enum

pg.init()
pg.mixer.init()


class SceneState(Enum):
    menu = 0
    runner = 1
    maze = 2
    final = 3


class ScenePresenter:
    def __init__(self, screen: pg.Surface, model: Model, scene_render: SceneRender):
        self._screen = screen
        self._game_logic = model
        self._scene_render = scene_render
        self._buttons = scene_render.get_buttons()
        self._change_scene = False

    @abstractmethod
    def handle_event(self) -> SceneState:
        pass

    @abstractmethod
    def render(self):
        pass


class MenuPresenter(ScenePresenter):
    def __init__(self, screen: pg.Surface, model: Model, scene_render: SceneRender):
        super().__init__(screen, model, scene_render)
        self.__scene_to_return = SceneState.menu

    def handle_event(self) -> SceneState:
        keys = pg.key.get_pressed()
        start_button = self._buttons['start_button']
        turn_on_button = self._buttons['turn_on_sound']
        x, y = pg.mouse.get_pos()
        if start_button.collide_click((x, y)) or keys[pg.K_RETURN]:
            self.__scene_to_return = SceneState.runner
            return SceneState.runner
        if turn_on_button.collide_click((x, y)):
            self._game_logic.toggle_sound()
        return SceneState.menu

    def render(self):
        sound_state = self._game_logic.get_sound_condition()
        self._scene_render.render_menu_scene(self._screen, sound_state)


class RunnerPresenter(ScenePresenter):
    def __init__(self, screen: pg.Surface, model: Model, scene_render: SceneRender):
        super().__init__(screen, model, scene_render)

    def handle_event(self) -> SceneState:
        keys = pg.key.get_pressed()
        if not self._game_logic.is_capybara_dead():
            if keys[pg.K_UP] or keys[pg.K_SPACE] or keys[pg.K_w]:
                self._game_logic.play_jump_sound()
                self._game_logic.run(True)

            elif keys[pg.K_DOWN] or keys[pg.K_s]:
                self._game_logic.run(False, True)

            else:
                self._game_logic.run(False)
        else:
            return SceneState.maze

        return SceneState.runner

    def handle_pause(self):
        pause_button = self._buttons['pause_button']
        turn_on_button = self._buttons['turn_on_sound']
        x, y = pg.mouse.get_pos()
        if pause_button.collide_click((x, y)):
            self._game_logic.toggle_pause()
        if turn_on_button.collide_click((x, y)):
            self._game_logic.toggle_sound()

    def render(self):
        record = self._game_logic.get_record_value()
        capybara_rect = self._game_logic.get_capybara_rect()
        is_capybara_jump = self._game_logic.get_capybara_state()
        enemy_rect = self._game_logic.get_enemy_information()
        pause_condition = self._game_logic.get_pause_condition()
        speed = self._game_logic.get_capybara_speed()
        sound_state = self._game_logic.get_sound_condition()
        self._scene_render.render_runner_scene(self._screen,
                                               record,
                                               (capybara_rect,
                                                is_capybara_jump),
                                               enemy_rect,
                                               pause_condition,
                                               speed,
                                               sound_state)


class MazePresenter(ScenePresenter):
    def __init__(self, screen: pg.Surface, model: Model, scene_render: SceneRender):
        super().__init__(screen, model, scene_render)

    def handle_event(self) -> SceneState:
        keys = pg.key.get_pressed()
        if self._game_logic.is_maze_time_not_over():
            self._game_logic.capybara_in_maze_move(keys)

            if self._game_logic.is_prize_received():
                return SceneState.runner

            return SceneState.maze

        else:
            self._game_logic.game_over()
            self._game_logic.save_record()
            return SceneState.final

    def render(self):
        time_to_print = self._game_logic.get_time_for_print()
        maze = self._game_logic.get_maze_to_render()
        maze_size = self._game_logic.get_maze_size()
        capybara_in_maze_information = self._game_logic.get_maze_capybara_information()
        prize_rect = self._game_logic.get_prize_rect()
        self._scene_render.render_maze_scene(self._screen,
                                             time_to_print,
                                             maze,
                                             maze_size,
                                             capybara_in_maze_information,
                                             prize_rect)


class Presenter:
    def __init__(self):
        self.__screen: pg.Surface = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(CAPTION)
        self.__scene: Enum = SceneState.menu
        self.__clock: pg.time.Clock = pg.time.Clock()
        self.__game_logic: Model = Model(MAZE_WIDTH,
                                         MAZE_HEIGHT,
                                         MAZE_INDENTATION_X,
                                         MAZE_INDENTATION_Y)
        self.__scene_render: SceneRender = SceneRender()
        self.__buttons: dict[str:Button] = self.__scene_render.get_buttons()
        self.__menu_presenter = MenuPresenter(self.__screen, self.__game_logic, self.__scene_render)
        self.__runner_presenter = RunnerPresenter(self.__screen, self.__game_logic, self.__scene_render)
        self.__maze_presenter = MazePresenter(self.__screen, self.__game_logic, self.__scene_render)

    def handle_event(self):
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                self.__game_logic.save_record()
                sys.exit()

            if event.type == pg.MOUSEBUTTONUP or event.type == pg.KEYDOWN:
                if self.__scene == SceneState.menu:
                    self.__scene = self.__menu_presenter.handle_event()

                elif self.__game_logic.get_pause_condition():
                    self.__runner_presenter.handle_pause()

                elif self.__scene == SceneState.final:
                    self.handle_final_click()

            if event.type == pg.KEYDOWN and SceneState.runner:
                if event.key == pg.K_ESCAPE:
                    self.__game_logic.toggle_pause()

        self.handle_gameplay()

    def handle_gameplay(self):
        if self.__scene == SceneState.runner:
            self.__scene = self.__runner_presenter.handle_event()

        if self.__scene == SceneState.maze:
            self.__scene = self.__maze_presenter.handle_event()

    def handle_final_click(self):
        keys = pg.key.get_pressed()
        restart_button = self.__buttons['restart_button']
        x, y = pg.mouse.get_pos()
        if restart_button.collide_click((x, y)) or keys[pg.K_RETURN]:
            self.restart_game()

    def render(self):
        if self.__scene == SceneState.menu:
            self.__menu_presenter.render()

        elif self.__scene == SceneState.runner:
            self.__runner_presenter.render()

        elif self.__scene == SceneState.maze:
            self.__maze_presenter.render()

        elif self.__scene == SceneState.final:
            self.render_final_scene()

    def render_final_scene(self):
        score = self.__game_logic.get_score()
        record = self.__game_logic.get_record()
        self.__scene_render.render_final_scene(self.__screen, score, record)

    def restart_game(self):
        self.__scene = SceneState.runner
        self.__game_logic = Model(MAZE_WIDTH,
                                  MAZE_HEIGHT,
                                  MAZE_INDENTATION_X,
                                  MAZE_INDENTATION_Y)
        self.__scene_render = SceneRender()
        self.__menu_presenter = MenuPresenter(self.__screen, self.__game_logic, self.__scene_render)
        self.__runner_presenter = RunnerPresenter(self.__screen, self.__game_logic, self.__scene_render)
        self.__maze_presenter = MazePresenter(self.__screen, self.__game_logic, self.__scene_render)

    def mainloop(self):
        while True:
            self.render()
            self.handle_event()

            self.__clock.tick(FPS)
