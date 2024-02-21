from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import random

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
        self.shape = tetromino_shapes[random.choice(list(tetromino_shapes.keys()))]
        self.blocks = []
        self.create_blocks()

    def create_blocks(self):
        with self.canvas:
            Color(1, 0, 0, 1)
            for x, y in self.shape:
                block_x = (W // 2 + x) * TILE  
                block_y = (H - 1 + y) * TILE  
                self.blocks.append(Rectangle(pos=(block_x, block_y), size=(TILE, TILE)))
                
    def move_left(self):
        if all((block.x - TILE) >= 0 for block in self.blocks):
            for block in self.blocks:
                block.x -= TILE

    def move_right(self):
        if all((block.x + TILE) < W * TILE for block in self.blocks):
            for block in self.blocks:
                block.x += TILE
    def rotate(self):
        pivot = self.blocks[0].pos
        for block in self.blocks:
            x, y = block.pos
            rel_x, rel_y = x - pivot[0], y - pivot[1]
            new_x = -rel_y + pivot[0]
            new_y = rel_x + pivot[1]
            block.pos = (new_x, new_y)


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
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self.current_tetromino = None
        self.cols, self.rows = W, H
        self.grid_layout = GridLayout(cols=self.cols)
        self.create_grid()
        self.add_widget(self.grid_layout)
        self.start_game()  # Start the game immediately for testing; move this to a proper start game trigger

    def start_game(self):
        self.current_tetromino = Tetromino(shape=random.choice(list(tetromino_shapes.keys())))  # Create a new tetromino with a random shape
        self.add_widget(self.current_tetromino)  # Add the tetromino to the game screen

    
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if self.current_tetromino:
            if keycode[1] == 'left':
                self.current_tetromino.move_left()
            elif keycode[1] == 'right':
                self.current_tetromino.move_right()
            elif keycode[1] == 'up':
                self.current_tetromino.rotate()
        return True

    def create_grid(self):
        for _ in range(self.cols * self.rows):
            self.grid_layout.add_widget(Widget())


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


class TetrisApp(App):
    def build(self):
        return TetrisGame()


if __name__ == "__main__":
    TetrisApp().run()
