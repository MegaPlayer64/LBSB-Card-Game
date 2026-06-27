from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        # Un botón simple para probar que levante la ventana de OpenGL
        return Button(text="¡Backend Blindado y Kivy Corriendo! 🚀")

if __name__ == '__main__':
    TestApp().run()