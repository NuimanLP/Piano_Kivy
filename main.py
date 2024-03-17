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
    
    current_index = 12

    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.update_key()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
    def update_key(self):
        current_note = [
            self.note_list[self.current_index + 0],
            self.note_list[self.current_index + 2],
            self.note_list[self.current_index + 4],
            self.note_list[self.current_index + 5],
            self.note_list[self.current_index + 7],
            self.note_list[self.current_index + 9],
            self.note_list[self.current_index + 11],
            self.note_list[self.current_index + 12],
            self.note_list[self.current_index + 14],
            self.note_list[self.current_index + 16],
            self.note_list[self.current_index + 17],
            self.note_list[self.current_index + 19],
            self.note_list[self.current_index + 21],
            self.note_list[self.current_index + 23],
            self.note_list[self.current_index + 24],
            self.note_list[self.current_index + 1],
            self.note_list[self.current_index + 3],
            self.note_list[self.current_index + 6],
            self.note_list[self.current_index + 8],
            self.note_list[self.current_index + 10],
            self.note_list[self.current_index + 13],
            self.note_list[self.current_index + 15],
            self.note_list[self.current_index + 18],
            self.note_list[self.current_index + 20],
            self.note_list[self.current_index + 22], ]
        for i in range(25):
            self.children[i].text = current_note[24 - i]
        self.children[26].text = f"[b]KEY {self.note_list[self.current_index]}[/b]"
        
    def on_press(self, key):
        key.background_color = (0.5, 0.5, 0.5, 1)
        self.make_sound(key)
        print(key.text)
        
    def make_sound(self, key):
        sound = SoundLoader.load(f"wav/{key.text}.wav")
        if sound:
            sound.play()
        return True
    
    def make_sound_keyboard(self, note):
        sound = SoundLoader.load(f"wav/{note}.wav")
        if sound:
            sound.play()
            Clock.schedule_once(lambda dt: sound.stop(), 0.5)
        return True

    def on_release_w(self, key):
        key.background_color = (255, 255, 255, 1)
        
    def on_release_b(self, key):
        key.background_color = (0, 0, 0, 1)
        
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] in self.Key:
            index = self.Key.index(keycode[1])
            self.make_sound_keyboard(self.note_list[index + self.current_index])
            # self.children[index].background_color = (0, 2, 2, 1)
            # # Clock.schedule_once(self.my_callback(self.children[index]), 0.4)
        
class SettingScreen(Screen):
    pass

class PianoApp(App):
   def build(self):
        return GameManager()
    
if __name__ == "__main__":
    PianoApp().run()