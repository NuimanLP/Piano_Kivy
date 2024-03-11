from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import Clock


class GameManager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(GameManager, self).__init__(*args, **kwargs)
        self.add_widget(TitleScreen())

    def start_app(self):
        if self.has_screen("piano"):
            self.remove_widget(self.get_screen("piano"))
        self.add_widget(GameScreen())
        self.current = "piano"


class TitleScreen(Screen):
    pass


class GameScreen(Screen):
    pass


class PianoApp(App):
    def build(self):
        return GameManager()


if __name__ == "__main__":
    PianoApp().run()
