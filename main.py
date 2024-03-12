from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# Define key mappings for piano keys to keyboard keys
Key = ['1', '2', '3', '4', '5', '6', '7', '8']

class Piano(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 8  # Adjust to fit all piano keys in one or more rows
        self.make_buttons()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard:
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def make_buttons(self):
        # Create more buttons to fulfill the widget requirement
        for i in range(30):  # Adjusted to create 30 buttons
            btn = Button(text=str(i+1), size_hint=(0.1, 0.1))
            btn.bind(on_press=self.callback)
            self.add_widget(btn)

    def callback(self, instance):
        index = int(instance.text) - 1
        self.play_sound(index)

    def play_sound(self, index):
        # Assuming you have 30 WAV files named '0.wav' to '29.wav'
        sound = SoundLoader.load(f'wav/{index}.wav')
        if sound:
            sound.play()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def my_callback(self, dt, btn):
        btn.background_color = (1, 1, 1, 1)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # This method maps keyboard keys to piano keys
        if text in Key:
            index = Key.index(text)
            btn = self.children[-(index + 1)]  # Access the corresponding button
            btn.background_color = (0, 1, 1, 1)  # Change color to indicate press
            self.play_sound(index)
            Clock.schedule_once(lambda dt: self.my_callback(dt, btn), 0.1)

class TestApp(App):
    def build(self):
        return Piano()

if __name__ == '__main__':
    TestApp().run()
