import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner

class PantallaSeleccion(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout_global = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Título
        layout_global.add_widget(Label(text="[b]CONFIGURAR PARTIDA[/b]", font_size='24sp', markup=True, size_hint_y=0.15))
        
        # Opciones Jugador 1
        panel_j1 = BoxLayout(orientation='vertical', spacing=10)
        panel_j1.add_widget(Label(text="Jugador 1", font_size='18sp'))
        
        self.spinner_tipo_j1 = Spinner(
            text='Humano',
            values=('Humano', 'IA Fácil', 'IA Normal', 'IA Difícil'),
            size_hint=(None, None), size=(200, 44), pos_hint={'center_x': 0.5}
        )
        
        # Cargar lista de mazos disponibles en la carpeta
        self.mazos = self.obtener_lista_mazos()
        opciones_mazo = [m['nombre'] for m in self.mazos]
        
        self.spinner_mazo_j1 = Spinner(
            text=opciones_mazo[0] if opciones_mazo else 'Sin Mazos',
            values=tuple(opciones_mazo),
            size_hint=(None, None), size=(300, 44), pos_hint={'center_x': 0.5}
        )
        
        panel_j1.add_widget(self.spinner_tipo_j1)
        panel_j1.add_widget(self.spinner_mazo_j1)
        layout_global.add_widget(panel_j1)
        
        # Opciones Jugador 2
        panel_j2 = BoxLayout(orientation='vertical', spacing=10)
        panel_j2.add_widget(Label(text="Jugador 2", font_size='18sp'))
        
        self.spinner_tipo_j2 = Spinner(
            text='Humano',
            values=('Humano', 'IA Fácil', 'IA Normal', 'IA Difícil'),
            size_hint=(None, None), size=(200, 44), pos_hint={'center_x': 0.5}
        )
        self.spinner_mazo_j2 = Spinner(
            text=opciones_mazo[0] if opciones_mazo else 'Sin Mazos',
            values=tuple(opciones_mazo),
            size_hint=(None, None), size=(300, 44), pos_hint={'center_x': 0.5}
        )
        
        panel_j2.add_widget(self.spinner_tipo_j2)
        panel_j2.add_widget(self.spinner_mazo_j2)
        layout_global.add_widget(panel_j2)
        
        # Botones de Acción
        layout_botones = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=0.2)
        btn_volver = Button(text="VOLVER", background_color=(0.8, 0.2, 0.2, 1))
        btn_volver.bind(on_release=lambda x: self.cambiar_pantalla('menu_screen'))
        
        btn_iniciar = Button(text="INICIAR PARTIDA", background_color=(0.2, 0.8, 0.2, 1))
        btn_iniciar.bind(on_release=self.iniciar_partida)
        
        layout_botones.add_widget(btn_volver)
        layout_botones.add_widget(btn_iniciar)
        layout_global.add_widget(layout_botones)
        
        self.add_widget(layout_global)

    def obtener_lista_mazos(self):
        # Escanea las carpetas de mazos predefinidos
        base_path = "src/data/premade_decks"
        mazos = []
        if os.path.exists(base_path):
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.json'):
                        full_path = os.path.join(root, file).replace('\\', '/')
                        mazos.append({'nombre': file.replace('.json', ''), 'ruta': full_path})
        
        # Mazo por defecto si no encuentra
        if not mazos:
            mazos.append({'nombre': 'Dermapatch', 'ruta': 'src/data/premade_decks/tag_theme/dermapatch_basic_deck.json'})
            
        return mazos

    def cambiar_pantalla(self, nombre_pantalla):
        self.manager.current = nombre_pantalla

    def iniciar_partida(self, instance):
        # Obtener rutas reales de los mazos seleccionados
        ruta_j1 = next((m['ruta'] for m in self.mazos if m['nombre'] == self.spinner_mazo_j1.text), None)
        ruta_j2 = next((m['ruta'] for m in self.mazos if m['nombre'] == self.spinner_mazo_j2.text), None)
        
        # Guardar en las variables globales de la App
        self.manager.app.game_settings = {
            'p1': {'tipo': self.spinner_tipo_j1.text, 'mazo': ruta_j1},
            'p2': {'tipo': self.spinner_tipo_j2.text, 'mazo': ruta_j2}
        }
        
        self.cambiar_pantalla('game_screen')
