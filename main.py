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
        
class PianoApp(App):
   def build(self):
        return GameManager()
    
if __name__ == "__main__":
    PianoApp().run()