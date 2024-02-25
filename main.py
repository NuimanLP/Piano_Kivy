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
from kivy.graphics import Color, Rectangle, Line


class Block(Widget):
    def __init__(self, color, **kwargs):
        super(Block, self).__init__(**kwargs)
        self.bind(pos=self.update_graphics_pos)
        self.size = (TILE, TILE)
        with self.canvas:
            self.color = Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_graphics_pos(self, instance, value):
        self.rect.pos = value

    # def update_color(self, color):
    #     self.canvas.before.clear()  # Clear previous color
    #     with self.canvas.before:
    #         Color(*color)
    #         self.rect = Rectangle(pos=self.pos, size=self.size)


TILE = 30

W, H = 20, 40


tetromino_shapes = {
    "I": [(0, 0), (-1, 0), (1, 0), (2, 0)],
    "O": [(0, 0), (0, -1), (-1, -1), (-1, 0)],
    "T": [(0, 0), (-1, 0), (1, 0), (0, -1)],
    "S": [(0, 0), (-1, 0), (0, -1), (1, -1)],
    "Z": [(0, 0), (1, 0), (0, -1), (-1, -1)],
    "J": [(0, 0), (-1, 0), (1, 0), (-1, -1)],
    "L": [(0, 0), (1, 0), (-1, 0), (1, -1)],
}


class GameManager(ScreenManager):

    def create_blocks(self):
        with self.canvas:
            Color = (1, 0, 0, 1)  # Red color
            for x, y in self.shape:
                block_x = (W // 2 + x) * TILE
                block_y = (H - 1 + y) * TILE
                block = Block(color=Color, pos=(block_x, block_y), size=(TILE, TILE))
                self.blocks.append(block)
                self.add_widget(block)

    def can_move(self, dx, dy):
        for block in self.blocks:
            x, y = block.pos
            grid_x, grid_y = int((x + dx * TILE) / TILE), int((y + dy * TILE) / TILE)
            if (
                grid_x < 0
                or grid_x >= W
                or grid_y < 0
                or grid_y >= H
                or self.parent.board[grid_y][grid_x]
            ):
                return False
        return True

    def move(self, dx, dy):
        if self.can_move(dx, dy):
            for block in self.blocks:
                x, y = block.pos
                block.pos = (x + dx * TILE, y + dy * TILE)
            return True
        return False

    def update_board(self, tetromino):
        for block in tetromino.blocks:
            x, y = block.pos
            grid_x, grid_y = int(x / TILE), int(y / TILE)
            self.board[grid_y][grid_x] = True

    def clear_lines(self):
        new_board = [row for row in self.board if not all(row)]
        lines_cleared = H - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [False for _ in range(W)])
        self.board = new_board

    def move_left(self):
        if all((block.pos[0] - TILE) >= 0 for block in self.blocks):
            for block in self.blocks:
                x, y = block.pos
                block.pos = (x - TILE, y)

    def move_right(self):
        if all((block.pos[0] + TILE) < W * TILE for block in self.blocks):
            for block in self.blocks:
                x, y = block.pos
                block.pos = (x + TILE, y)

    def rotate(self):
        pivot = self.blocks[0].pos  # Use the first block as the pivot
        new_positions = []
        for block in self.blocks:
            x, y = block.pos
            # Calculate relative positions
            rel_x, rel_y = x - pivot[0], y - pivot[1]
            # Rotate 90 degrees
            new_x = -rel_y + pivot[0]
            new_y = rel_x + pivot[1]
            # Check if the new position is valid
            grid_x, grid_y = int(new_x / TILE), int(new_y / TILE)
            if (
                grid_x < 0
                or grid_x >= W
                or grid_y < 0
                or grid_y >= H
                or self.parent.board[grid_y][grid_x]
            ):
                return  # Rotation is invalid
            new_positions.append((new_x, new_y))

        # Apply new positions after verifying all are valid
        for block, (new_x, new_y) in zip(self.blocks, new_positions):
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
        self.board = [[False for _ in range(W)] for _ in range(H)]
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self.current_tetromino = None
        self.cols, self.rows = W, H
        self.grid_layout = GridLayout(cols=self.cols)
        self.create_grid()
        self.add_widget(self.grid_layout)
        self.start_game()  # Start the game
        Clock.schedule_interval(self.game_tick, 1.0)
        self.score_label = Label(
            text="Score: 0", font_size=TILE, pos_hint={"right": 0.95, "top": 0.95}
        )
        self.add_widget(self.score_label)

    def start_game(self):
        self.current_tetromino = Tetromino(
            shape=random.choice(list(tetromino_shapes.keys()))
        )  # Create a new tetromino with a random shape
        self.add_widget(self.current_tetromino)

    def spawn_new_tetromino(self):
        shape = random.choice(list(tetromino_shapes.keys()))
        self.current_tetromino = Tetromino(shape=shape)
        self.current_tetromino.pos = ((W // 2) - 1) * TILE, (H + 1) * TILE
        self.add_widget(self.current_tetromino)

    # def check_game_over(self):
    #     # How the fack i do this ahhh hell
    #     for x in range(H):
    #         if self.board[0][]:
    #             print('Game Over Borad [0][x]!')
    #             return False  # Game is over
    #     return True and print('Game not over')  # Game is not over

    def try_move_down(self):
        moved_down = self.current_tetromino.move(0, -1)
        print("Moved down", moved_down)
        return moved_down

    def game_tick(self, dt):
        if not self.try_move_down():
            self.place_tetromino()
            self.clear_lines()
            # if self.check_game_over():
            #     self.end_game()
            # else:
            self.spawn_new_tetromino()  # Ensure game over check is negated correctly

    def place_tetromino(self):
        for block in self.current_tetromino.blocks:
            x, y = block.pos
            grid_x, grid_y = int(x / TILE), int(y / TILE)
            self.board[grid_y][grid_x] = True  # Mark the cell as occupied
            self.clear_lines()
            # if  self.check_game_over():
            self.spawn_new_tetromino()
            # else:
            self.end_game()

    def end_game(self):
        Clock.unschedule(self.game_tick)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if self.current_tetromino:
            if keycode[1] == "left":
                self.current_tetromino.move(-1, 0)
            elif keycode[1] == "right":
                self.current_tetromino.move(1, 0)
            elif keycode[1] == "up":
                self.current_tetromino.rotate()
            elif keycode[1] == "down":
                if not self.try_move_down():  # If the tetromino can't move down
                    print("Can't move down more Bro!")
                    self.place_tetromino()
        return True

    def create_grid(self):
        with self.canvas.before:
            Color(0.6, 0.6, 0.6, 1)  # Gray color for the grid lines
            # Vertical lines
            for i in range(W + 1):
                x = i * TILE
                Line(points=[x, 0, x, H * TILE])
            # Horizontal lines
            for i in range(H + 1):
                y = i * TILE
                Line(points=[0, y, W * TILE, y])

    def clear_lines(self):
        new_board = []
        lines_cleared = 0
        for row in self.board:
            if all(row):
                lines_cleared += 1
            else:
                new_board.append(row)
        for _ in range(lines_cleared):
            new_board.insert(0, [False for _ in range(W)])
        self.board = new_board  # Update the board


class TitleScreen(Screen):
    pass


class TetrisApp(App):
    def build(self):
        return GameManager()


if __name__ == "__main__":
    TetrisApp().run()
