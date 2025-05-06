from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

class RoundedLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Color blanco
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class RoundedApp(App):
    def build(self):
        # Ajusta el tamaño de la ventana para que simule bordes redondeados
        Window.size = (400, 300)
        layout = RoundedLayout()
        layout.add_widget(Label(text="Ventana con esquinas redondeadas"))
        return layout

if __name__ == '__main__':
    RoundedApp().run()
