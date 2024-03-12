from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.clock import Clock

Key = ["1", "2", "3", "4", "5", "6", "7", "8"]

class Piano(GridLayout):
    def __init__(self, **kwargs):
        super(Piano, self).__init__(**kwargs)
        self.cols = 1 

        self.volume_control = Slider(min=0, max=1, value=0.5, orientation='horizontal', size_hint_y=None, height=50)
        self.add_widget(self.volume_control)

        self.keys_layout = GridLayout(cols=8, size_hint_y=100, height=600)
        self.make_buttons()
        self.add_widget(self.keys_layout)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.is_pressed()

    # Make Buttons
    def make_buttons(self):
        for text in range(1, 25):
            self.keys_layout.add_widget(Button(text=str(text), size_hint=(0.1, 0.1)))

    # Check to clicked buttons
    def is_pressed(self):
        for child in self.keys_layout.children:
            child.bind(on_press=self.callback)

    # callback for pressing buttons
    def callback(self, instance):
        self.Sound(int(instance.text) - 1)

    # play sounds
    def Sound(self, index):
        sound = SoundLoader.load(f"wav/{index}.wav")
        if sound:
            sound.volume = self.volume_control.value
            sound.play()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    # callback for change color of Buttons
    def my_callback(self, dt):
        for child in self.keys_layout.children:
            child.background_color = [1, 1, 1, 1]

    # event when we push keyboard keys
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        for index, item in enumerate(Key):
            if keycode[1] == item:
                self.keys_layout.children[-index - 1].background_color = (0, 2, 2, 1)
                self.Sound(index)
                Clock.schedule_once(self.my_callback, 0.4)


class PianoApp(App):
    def build(self):
        return Piano()


if __name__ == "__main__":
    PianoApp().run()
