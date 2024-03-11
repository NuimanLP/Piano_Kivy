from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty


class AppManager(ScreenManager):

    def __init__(self, *args, **kwargs):
        super(AppManager, self).__init__(*args, **kwargs)
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
        return AppManager()


if __name__ == "__main__":
    PianoApp().run()
