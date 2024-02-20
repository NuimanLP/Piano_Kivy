from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from random import choice


TILE = 30

W, H = 10, 20

tetromino_shapes = {
    'I': [(0, 0), (-1, 0), (1, 0), (2, 0)],
    'O': [(0, 0), (0, -1), (-1, -1), (-1, 0)],
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)],
    'J': [(0, 0), (-1, 0), (1, 0), (-1, -1)],
    'L': [(0, 0), (1, 0), (-1, 0), (1, -1)],
}


class Tetromino(Widget):
    def __init__(self, shape, **kwargs):
        super(Tetromino, self).__init__(**kwargs)
        self.shape = shape
        self.blocks = []
        self.create_blocks()

    def create_blocks(self):
        with self.canvas:
            Color(1, 0, 0, 1)
            for pos in self.shape:
                x, y = pos
                self.blocks.append(Rectangle(pos=(x * TILE, y * TILE), size=(TILE, TILE)))


class TetrisGame(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(TetrisGame, self).__init__(*args, **kwargs)
        self.title_screen = TitleScreen(name="title")
        self.game_screen = GameScreen(name="game")
        self.add_widget(self.title_screen)
        self.add_widget(self.game_screen)


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.cols, self.rows = W,H
        self.grid_layout = GridLayout(cols=self.cols)
        self.create_grid()
        self.add_widget(self.grid_layout)

    def create_grid(self):
        for _ in range(self.cols * self.rows):
            self.grid_layout.add_widget(Widget())
    def start_game(self):
        self.current_tetromino = self.create_tetromino()
        self.draw_tetromino(self.current_tetromino)
    def create_tetromino(self):
        shape_name, shape_coords = choice(list(tetromino_shapes.items()))
        tetromino = Tetromino(shape=shape_coords)
        return tetromino
    def draw_tetromino(self, tetromino):
        for block in tetromino.blocks:
            self.canvas.add(block)


class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        # Create a Button widget
        start_button = Button(
            text="Start Game",
            size_hint=(None, None),
            size=(300, 75),
            background_color=[0.2, 1, 1, 1],
            pos_hint={"center_x": 0.5, "center_y": 0.4},  # Center the button
        )
        start_button.bind(on_press=self.on_button_press)
        self.add_widget(start_button)

    def on_button_press(self, instance):
        self.manager.transition.direction = "left"  # transition
        self.manager.current = "game"
        self.manager.get_screen('game').start_game()

class TetrisApp(App):
    def build(self):
        return TetrisGame()


if __name__ == "__main__":
    TetrisApp().run()
