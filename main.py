from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock

class TetrisGame(ScreenManager):
    def __init__(self, *args, **kwargs):
        super(TetrisGame, self).__init__(*args, **kwargs)
        self.title_screen = TitleScreen(name='title')
        self.game_screen = GameScreen(name='game')
        self.add_widget(self.title_screen)
        self.add_widget(self.game_screen)

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        label = Label(text='Game Screen', center=self.center)
        self.add_widget(label)


class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super(TitleScreen, self).__init__(**kwargs)
        # Create a Button widget
        start_button = Button(
            text='Start Game',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Center the button
        )
        start_button.bind(on_press=self.on_button_press)
        self.add_widget(start_button)
    def on_button_press(self, instance):
        print("The button has been pressed!!!")


class TetrisApp(App):
    def build(self):
        return TetrisGame()


if __name__ == "__main__":
    TetrisApp().run()
