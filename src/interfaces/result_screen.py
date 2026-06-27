from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class PantallaResultado(Screen):
    """Pantalla de Victoria / Derrota que se muestra al terminar la partida."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        # Labels dinámicos que se actualizan antes de mostrar la pantalla
        self.lbl_titulo = Label(
            text="",
            font_size='48sp',
            markup=True,
            size_hint_y=0.35,
            halign='center'
        )
        self.lbl_detalle = Label(
            text="",
            font_size='20sp',
            markup=True,
            size_hint_y=0.25,
            halign='center'
        )

        btn_revancha = Button(
            text="REVANCHA\n(Volver a selección)",
            font_size='18sp',
            size_hint_y=0.2,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        btn_revancha.bind(on_release=lambda x: self._ir_a('selection_screen'))

        btn_menu = Button(
            text="MENÚ PRINCIPAL",
            font_size='18sp',
            size_hint_y=0.2,
            background_color=(0.4, 0.4, 0.4, 1)
        )
        btn_menu.bind(on_release=lambda x: self._ir_a('menu_screen'))

        self.layout.add_widget(self.lbl_titulo)
        self.layout.add_widget(self.lbl_detalle)
        self.layout.add_widget(btn_revancha)
        self.layout.add_widget(btn_menu)
        self.add_widget(self.layout)

    def configurar(self, ganador_nombre: str, perdedor_nombre: str, jugador_local_id: int, ganador_id: int):
        """Llamar antes de hacer la transición para personalizar el texto."""
        victoria = (jugador_local_id == ganador_id) or jugador_local_id < 0
        if victoria:
            self.lbl_titulo.text = "[color=00ff88][b]¡VICTORIA![/b][/color]"
        else:
            self.lbl_titulo.text = "[color=ff4444][b]DERROTA[/b][/color]"
        self.lbl_detalle.text = (
            f"[b]{ganador_nombre}[/b] ganó la partida.\n"
            f"La base de [b]{perdedor_nombre}[/b] fue destruida."
        )

    def _ir_a(self, pantalla):
        self.manager.current = pantalla
