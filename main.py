from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock


class GameManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(GameManager, self).__init__(*args, **kwargs)
        self.add_widget(TitleScreen())

class PianoApp(App):
   def build(self):
        return GameManager()
    
if __name__ == "__main__":
    PianoApp().run()