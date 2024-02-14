from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager


class TetrisGame(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(TetrisGame, self).__init__(*args, **kwargs)
        self.add_widget(TitleScreen())


class TitleScreen(Screen):
    pass


class TetrisApp(App):
    def build(self):
        return TetrisGame()


if __name__ == "__main__":
    TetrisApp().run()
