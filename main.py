from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import Clock

Key = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
]


class Piano(GridLayout):
    def __init__(self, **kwargs):
        super(Piano, self).__init__(**kwargs)
        self.cols = 10
        self.make_buttons()

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.is_pressed()


class PianoApp(App):
    def build(self):
        return


if __name__ == "__main__":
    PianoApp().run()
