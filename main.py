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
        
    def start_app(self):
        if self.has_screen("piano"):
            self.remove_widget(self.get_screen("piano"))
        self.add_widget(GameScreen())
        self.current = "piano"
        
    def setting_app(self):
        if self.has_screen("setting"):
            self.remove_widget(self.get_screen("setting"))
        self.add_widget(SettingScreen())
        self.current = "setting"
            
    def exit_app(self):
        App.get_running_app().stop()
        
    def back(self):
            if self.has_screen("setting") or self.has_screen("piano"):
                self.remove_widget(self.get_screen("title"))
            self.add_widget(TitleScreen())
            self.current = "title"
                 
class TitleScreen(Screen):
    pass

class GameScreen(Screen, GridLayout):
    note_list = [ "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
                  "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
                  "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
                  "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5" ]
    
    Key = [ "tab", "1", "q", "2", "w", "e", "4", "r", "5", "t", "6", "y",
            "u", "8", "i", "9", "o", "p", "-", "[", "=", "]", "backspace", "z", "x", ]

class SettingScreen(Screen):
    pass

class PianoApp(App):
   def build(self):
        return GameManager()
    
if __name__ == "__main__":
    PianoApp().run()