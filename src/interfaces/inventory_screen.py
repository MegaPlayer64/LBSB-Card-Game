import json
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from src.infrastructure.loaders.card_loader import CardLoader

class TarjetaAlbum(BoxLayout):
    def __init__(self, nombre, coste, rareza, tipo, cantidad, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=180, **kwargs)
        
        if tipo == 'spell':
            color_fondo = (0.5, 0.2, 0.6, 1) # Morado
        elif tipo == 'building':
            color_fondo = (0.2, 0.5, 0.3, 1) # Verde
        else:
            color_fondo = (0.1, 0.4, 0.6, 1) # Azul Unidades

        btn_visual = Button(
            text=f"{nombre}\nCoste: {coste}E\n[{rareza}]", 
            background_color=color_fondo,
            halign='center'
        )
        
        lbl_cant = Label(text=f"Poseídas: x{cantidad}", size_hint_y=0.2, color=(1, 1, 1, 1))
        
        self.add_widget(btn_visual)
        self.add_widget(lbl_cant)


class PantallaInventario(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ruta_perfil = "src/data/user_profile.json"
        
        layout_principal = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Guardamos el label del título/monedas como atributo para poder actualizarlo luego
        self.lbl_titulo = Label(text="ÁLBUM DE COLECCIÓN", size_hint_y=0.1, font_size='20sp')
        layout_principal.add_widget(self.lbl_titulo)
        
        scroll = ScrollView(size_hint_y=0.8)
        self.grilla_cartas = GridLayout(cols=4, spacing=10, size_hint_y=None)
        self.grilla_cartas.bind(minimum_height=self.grilla_cartas.setter('height'))
        
        scroll.add_widget(self.grilla_cartas)
        layout_principal.add_widget(scroll)
        
        btn_volver = Button(text="Volver al Menú", size_hint_y=0.1)
        btn_volver.bind(on_release=lambda x: self.cambiar_a_menu())
        layout_principal.add_widget(btn_volver)
        
        self.add_widget(layout_principal)

    def on_enter(self):
        """Este método de Kivy se ejecuta automáticamente CADA VEZ que entras a esta pantalla"""
        self.cargar_inventario_desde_json()

    def cargar_inventario_desde_json(self):
        self.grilla_cartas.clear_widgets()
        
        # 1. Intentar leer el archivo JSON real
        if not os.path.exists(self.ruta_perfil):
            print(f"[!] Error: No se encontró el archivo en {self.ruta_perfil}")
            self.lbl_titulo.text = "ÁLBUM DE COLECCIÓN (Perfil no encontrado)"
            return
            
        try:
            with open(self.ruta_perfil, "r", encoding="utf-8") as f:
                perfil_data = json.load(f)
        except Exception as e:
            print(f"[!] Error al parsear el JSON del perfil: {e}")
            return

        # 2. Actualizar el encabezado con el nombre y las monedas actuales del jugador
        usuario = perfil_data.get("username", "Jugador")
        monedas = perfil_data.get("coins", 0)
        self.lbl_titulo.text = f"ÁLBUM DE {usuario.upper()}  |  🪙 Monedas: {monedas}"

        # 3. Extraer el diccionario de inventario
        inventario_usuario = perfil_data.get("inventory", {})
        
        # 4. Consultar las IDs al CardLoader real y meterlas a la grilla
        for card_id_str, cantidad in inventario_usuario.items():
            card_id = int(card_id_str)
            carta_objeto = CardLoader.get_card_stats_by_id(card_id)
            
            if carta_objeto and cantidad > 0:
                nombre = carta_objeto.name
                coste = carta_objeto.cost
                rareza = getattr(carta_objeto, 'rarity', 'Común')
                tipo = 'unit' if hasattr(carta_objeto, 'attack') else getattr(carta_objeto, 'card_type', 'unit')

                tarjeta = TarjetaAlbum(
                    nombre=nombre, 
                    coste=coste, 
                    rareza=rareza, 
                    tipo=tipo, 
                    cantidad=cantidad
                )
                self.grilla_cartas.add_widget(tarjeta)

    def cambiar_a_menu(self):
        self.manager.current = 'menu_screen'