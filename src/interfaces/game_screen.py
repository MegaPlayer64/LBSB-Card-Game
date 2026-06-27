from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.clock import Clock

# Importamos tu cerebro real (ajusta las rutas si están en otra carpeta)
from src.domain.game_state import GameState
from src.domain.action import Action, ActionType
# También podrías necesitar importar tu base de datos de cartas aquí para el setup
class CartaDraggable(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drag_widget = None

    def on_touch_down(self, touch):
        # Si el toque es dentro de este botón
        if self.collide_point(*touch.pos):
            print(">> Iniciando arrastre...")
            # Aquí crearías un widget visual pequeño (la carta) que sigue al touch
            self.drag_widget = Image(source='carta_placeholder.png', size=(100, 150))
            self.add_widget(self.drag_widget)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.drag_widget:
            self.drag_widget.pos = (touch.x - 50, touch.y - 75)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.drag_widget:
            # AQUÍ ES LA MAGIA: Verificamos dónde soltó la carta
            # ¿El mouse está sobre el tablero?
            if self.parent.parent.grilla_tablero.collide_point(*touch.pos):
                print(">> Carta soltada en el tablero, invocando...")
                # Llamamos a tu lógica de apply_action aquí
            
            # Limpiamos el rastro
            self.remove_widget(self.drag_widget)
            self.drag_widget = None
            return True
        return super().on_touch_up(touch)

class PantallaJuego(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout_tablero_global = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.unidad_seleccionada_coords = None # Almacenará (x, y) de la unidad que quieres mover
        # 1. BARRA SUPERIOR (Datos de la partida)
        barra_info = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        self.lbl_j1 = Label(text="J1 (Tú): 80 HP\nEnergía: 1/1", halign='left')
        self.lbl_j2 = Label(text="J2 (Rival): 80 HP\nEnergía: 1/1", halign='right')
        btn_rendirse = Button(text="Rendirse", size_hint_x=0.2)
        btn_rendirse.bind(on_release=lambda x: self.volver_al_menu())
        btn_reiniciar = Button(text="Reiniciar", size_hint_x=0.15, background_color=(0.2, 0.6, 0.8, 1))
        btn_reiniciar.bind(on_release=self.reiniciar_partida)
        btn_pasar_turno = Button(text="Pasar\nTurno", size_hint_x=0.15, background_color=(0.8, 0.6, 0.1, 1))
        btn_pasar_turno.bind(on_release=self.pasar_turno)
        
        self.btn_atacar_base = Button(text="Atacar\nBase", size_hint_x=0.15, background_color=(0.8, 0.2, 0.2, 1))
        self.btn_atacar_base.bind(on_release=self.atacar_base)
        
        barra_info.add_widget(self.lbl_j1)
        barra_info.add_widget(btn_rendirse)
        barra_info.add_widget(btn_reiniciar)
        barra_info.add_widget(self.btn_atacar_base)
        barra_info.add_widget(btn_pasar_turno)
        barra_info.add_widget(self.lbl_j2)
        layout_tablero_global.add_widget(barra_info)
        
        # 2. CUADRÍCULA DE JUEGO (6x5 Matriz de Botones/Celdas)
        # Nota: Kivy organiza por columnas primero, para un 6x5 (Columnas=6, Filas=5)
        grilla_tablero = GridLayout(cols=6, rows=5, spacing=4, size_hint_y=0.6)
        
        # Guardaremos las celdas en una matriz en memoria para interactuar con ellas después
        self.celdas_graficas = {}
        for y in range(5):
            for x in range(6):
                btn_celda = Button(text=".", font_size='14sp')
                # Guardamos la coordenada en el botón usando propiedades dinámicas de Kivy
                btn_celda.coordenadas = (x, y)
                btn_celda.bind(on_release=self.celda_clickeada)
                
                grilla_tablero.add_widget(btn_celda)
                self.celdas_graficas[(x, y)] = btn_celda
                
        layout_tablero_global.add_widget(grilla_tablero)
        
        # 3. ZONA INFERIOR (Tu mano de cartas)
        self.layout_mano = BoxLayout(orientation='horizontal', size_hint_y=0.25, spacing=5)
        # Espacio reservado temporalmente para renderizar los botones de las cartas robadas
        self.layout_mano.add_widget(Label(text="[Zona de Mano - Esperando Cartas]", markup=True))
        
        layout_tablero_global.add_widget(self.layout_mano)
        self.add_widget(layout_tablero_global)
        
        # El GameState se crea en on_pre_enter, cuando ya tenemos las settings
        self.game_state = None
        self.ai_controller = None  # Controlador de IA (si aplica)
        self.carta_seleccionada_index = None

    def celda_clickeada(self, instance):
        x, y = instance.coordenadas
        jugador = self.game_state.get_current_player()
        unidad_en_celda = self.game_state.board.get_unit_at(x, y)
        
        # MODO: RESOLVIENDO HABILIDAD PENDIENTE
        if getattr(self.game_state, 'pending_ability', None):
            accion = Action(player_id=jugador.id, type=ActionType.RESOLVE_ABILITY, payload={'target': (x, y)})
            if self.game_state.apply_action(accion):
                print(f">> Habilidad resuelta en ({x}, {y})")
            else:
                print(f">> [!] Resolución inválida en ({x}, {y})")
            self.actualizar_interfaz_completa()
            return
        
        # 1. MODO: CARTA SELECCIONADA (Invocación o Truco)
        if self.carta_seleccionada_index is not None:
            carta = jugador.hand[self.carta_seleccionada_index]
            is_spell = getattr(carta, 'card_type', 'unit').lower() == 'spell'
            tipo_accion = ActionType.PLAY_SPELL if is_spell else ActionType.PLAY_CARD
            payload = {'card_index': self.carta_seleccionada_index, 'target' if is_spell else 'to': (x, y)}
            
            accion = Action(player_id=jugador.id, type=tipo_accion, payload=payload)
            if self.game_state.apply_action(accion):
                self.carta_seleccionada_index = None
                self.actualizar_interfaz_completa()
            return

        # 2. MODO: UNIDAD SELECCIONADA (¿Mover, Atacar o Habilidad?)
        if self.unidad_seleccionada_coords:
            origen = self.unidad_seleccionada_coords
            
            if origen == (x, y):
                # Si clica de nuevo en la misma unidad -> Activar Habilidad
                accion = Action(player_id=jugador.id, type=ActionType.ACTIVATE_ABILITY, payload={'from': origen})
            elif unidad_en_celda and unidad_en_celda.owner_id != jugador.id:
                # Si clica en enemigo -> Atacar
                accion = Action(player_id=jugador.id, type=ActionType.ATTACK, payload={'from': origen, 'target': (x, y)})
            else:
                # Si clica en vacío u otra casilla -> Mover
                accion = Action(player_id=jugador.id, type=ActionType.MOVE, payload={'from': origen, 'to': (x, y)})
            
            # Ejecutamos la acción y limpiamos selección
            if self.game_state.apply_action(accion):
                print(f">> Acción realizada desde {origen} hacia {(x, y)}")
            else:
                print(f">> [!] Acción denegada desde {origen}")
                
            self.unidad_seleccionada_coords = None
            self.actualizar_interfaz_completa()
            return

        # 3. MODO: SELECCIÓN (Click inicial)
        if unidad_en_celda and unidad_en_celda.owner_id == jugador.id:
            self.unidad_seleccionada_coords = (x, y)
            # Pista visual: pintamos la celda de verde para indicar que está seleccionada
            self.celdas_graficas[(x, y)].background_color = (0.2, 0.8, 0.2, 1)

    def atacar_base(self, instance):
        if not self.unidad_seleccionada_coords:
            print(">> [!] Selecciona una unidad tuya primero para atacar la base.")
            return
            
        jugador = self.game_state.get_current_player()
        origen = self.unidad_seleccionada_coords
        
        accion = Action(player_id=jugador.id, type=ActionType.ATTACK, payload={'from': origen, 'target': 'B'})
        
        if self.game_state.apply_action(accion):
            print(f">> ¡Ataque a la base ejecutado desde {origen}!")
        else:
            print(f">> [!] Ataque a la base denegado.")
            
        self.unidad_seleccionada_coords = None
        self.actualizar_interfaz_completa()

    def enviar_accion_movimiento(self, origen, destino):
        """
        Envía la acción de movimiento al motor para que la valide y ejecute.
        """
        from src.domain.action import Action, ActionType
        
        # 1. Crear la orden oficial
        accion = Action(
            player_id=self.game_state.current_player_id,
            type=ActionType.MOVE_UNIT,
            payload={'from': origen, 'to': destino}
        )
        
        # 2. Preguntar al backend si es legal
        exito = self.game_state.validate_action(accion)
        
        if exito:
            print(">> ¡Movimiento autorizado y ejecutado!")
        else:
            print(">> [!] Movimiento denegado. Verifica distancias o casillas ocupadas.")
            
        # 3. Refrescar la pantalla siempre
        self.actualizar_interfaz_completa()

        
    def actualizar_celda(self, x, y, texto, color_rgba):
        # Esta es tu función maestra para pintar el tablero.
        # Buscamos el botón exacto en nuestro diccionario usando las coordenadas
        boton = self.celdas_graficas[(x, y)]
        
        # Le cambiamos el texto (puedes usar \n para poner la vida abajo)
        boton.text = texto
        
        # Le cambiamos el color de fondo usando formato RGBA (Red, Green, Blue, Alpha)
        # Los valores van de 0 a 1. Ej: (1, 0, 0, 1) es Rojo puro.
        boton.background_color = color_rgba

    def actualizar_tablero(self, estado_juego):
        # Ocultar tu mano si el estado es None (pantalla vacía inicial)
        if estado_juego is None:
            self.layout_mano.clear_widgets()
            self.layout_mano.add_widget(Label(text="[Mano de Cartas Vacia]"))
            return

        # 1. Actualizar Información de Jugadores
        p1 = estado_juego.players[0]
        p2 = estado_juego.players[1]
        
        # Nota: Asumimos que el jugador local es el 0 para la UI de la barra superior
        self.lbl_j1.text = f"{p1.name}: {p1.health} HP | Energía: {p1.current_energy}/{p1.max_energy}"
        self.lbl_j2.text = f"{p2.name}: {p2.health} HP | Energía: {p2.current_energy}/{p2.max_energy}"
        
        # 2. Actualizar Tablero de Juego
        # Limpiamos todo por seguridad para redibujar encima
        self.layout_mano.clear_widgets()
        
        for y in range(5):
            for x in range(6):
                celda = estado_juego.board[x][y]
                boton = self.celdas_graficas[(x, y)]
                
                if celda is None:
                    boton.text = "."
                    boton.background_color = (0.5, 0.5, 0.5, 1) # Gris neutro
                else:
                    # Mostramos Nombre / ATK / DEF / HP
                    boton.text = f"{celda.name}\n{celda.attack}/{celda.health}"
                    # Color según dueño
                    if celda.owner_id == 0: # Player 1 (Tú)
                        boton.background_color = (0.2, 0.6, 1, 1) # Azul
                    else: # Player 2
                        boton.background_color = (1, 0.4, 0.4, 1) # Rojo/Naranja

        # 3. Actualizar Mano
        self.layout_mano.clear_widgets()
        mano = estado_juego.players[0].hand
        if not mano:
             self.layout_mano.add_widget(Label(text="[Mano Vacia]"))
        else:
            for carta in mano:
                # Creamos un botón representativo para la carta
                # En una versión real, aquí would cargarias la imagen de la carta
                btn_carta = Button(
                    text=f"{carta.name}\n{carta.cost}E",
                    size_hint_x=0.15,
                    background_color=(0.1, 0.1, 0.3, 1)
                )
                
                # BINDING CRITICO: Al tocar la carta, le decimos al controlador que la seleccione
                def on_carta_release(btn_carta, carta_obj=carta):
                    # Esta función "captura" la instancia de la carta en memoria
                    # y la pasa al controlador para que sepa qué invocar
                    print(f"-> Carta seleccionada en mano: {carta_obj.name}")
                    # Aquí iría la lógica de selección del controlador humano
                
                btn_carta.bind(on_release=on_carta_release)
                self.layout_mano.add_widget(btn_carta)
    def volver_al_menu(self):
        self.manager.current = 'menu_screen'

    def cargar_mano_prueba(self):
        # Guardamos la lista en "self" para poder borrarle cartas después
        self.mano_falsa_memoria = [
            {"nombre": "Darío", "coste": 1, "tipo": "unit"},
            {"nombre": "Margarita", "coste": 5, "tipo": "unit"},
            {"nombre": "Charla Vocacional", "coste": 4, "tipo": "spell"},
            {"nombre": "Chino", "coste": 4, "tipo": "unit"}
        ]
        self.dibujar_mano(self.mano_falsa_memoria)

    def dibujar_mano(self, mano_jugador):
        # 1. Limpiamos la zona de la mano por si ya había cartas antes
        self.layout_mano.clear_widgets()
        self.carta_seleccionada_index = None # Reseteamos la selección

        if not mano_jugador:
            self.layout_mano.add_widget(Label(text="[Mano Vacía]"))
            return

        # 2. Creamos un botón por cada carta en la lista
        for i, carta in enumerate(mano_jugador):
            texto_carta = f"{carta['nombre']}\nCoste: {carta['coste']}"
            
            btn_carta = Button(
                text=texto_carta,
                font_size='14sp',
                background_color=(0.3, 0.3, 0.3, 1), # Gris oscuro por defecto
                halign='center'
            )
            
            # Le "escondemos" el índice al botón para saber cuál es cuando lo clickeen
            btn_carta.indice_mano = i 
            btn_carta.bind(on_release=self.seleccionar_carta)
            
            self.layout_mano.add_widget(btn_carta)

    def seleccionar_carta(self, instance):
        # 1. Despintamos TODAS las cartas de la mano devolviéndolas a gris
        for btn in self.layout_mano.children:
            btn.background_color = (0.3, 0.3, 0.3, 1)

        # 2. Pintamos de dorado/naranja la carta que acabamos de clickear
        instance.background_color = (0.8, 0.6, 0.1, 1) 
        
        # 3. Guardamos el índice en la memoria de la pantalla
        self.carta_seleccionada_index = instance.indice_mano
        
        # Sacamos el salto de línea para imprimir bonito en consola
        nombre_limpio = instance.text.replace('\n', ' | ')
        print(f">> Carta en espera: [{self.carta_seleccionada_index}] {nombre_limpio}")
    def actualizar_interfaz_completa(self):
        if not self.game_state:
            return
        jugador_actual = self.game_state.get_current_player()
        
        # A) Actualizar barra superior (Energía y Vida real)
        p1 = self.game_state.players[0]
        p2 = self.game_state.players[1]
        
        pending = getattr(self.game_state, 'pending_ability', None)
        lbl_estado = "\n[color=ff3333][b]¡SELECCIONA OBJETIVO![/b][/color]" if pending else ""
        
        self.lbl_j1.text = f"J1: {p1.health} HP\nEnergía: {getattr(p1, 'current_energy', 0)}/{getattr(p1, 'max_energy', 0)}" + (lbl_estado if self.game_state.current_player_id == 0 else "")
        self.lbl_j1.markup = True
        self.lbl_j2.text = f"J2: {p2.health} HP\nEnergía: {getattr(p2, 'current_energy', 0)}/{getattr(p2, 'max_energy', 0)}" + (lbl_estado if self.game_state.current_player_id == 1 else "")
        self.lbl_j2.markup = True
        
        # B) Limpiar el tablero visual por completo
        for (cx, cy), btn in self.celdas_graficas.items():
            btn.text = "."
            btn.background_color = (1, 1, 1, 1) # Gris neutro
            
        # C) Redibujar las tropas que realmente están vivas en el GameState
        for (cx, cy), unit in self.game_state.board.grid.items():
            boton = self.celdas_graficas[(cx, cy)]
            boton.text = f"{unit.name}\n{unit.health}/{unit.max_health} HP"
            # Pintamos azul para J1, rojo para J2
            boton.background_color = (0.1, 0.5, 0.8, 1) if unit.owner_id == 1 else (0.8, 0.2, 0.2, 1)

        # D) Redibujar la mano traduciendo las cartas reales a los botones
        mano_formateada = []
        for carta in jugador_actual.hand:
            # Extraemos la data real de tu objeto Carta
            mano_formateada.append({
                "nombre": carta.name, 
                "coste": carta.cost, 
                "tipo": getattr(carta, 'card_type', 'unit')
            })
        
        self.dibujar_mano(mano_formateada)

    def on_pre_enter(self, *args):
        """Se ejecuta justo antes de mostrar esta pantalla. Construye el GameState."""
        from src.domain.player import Player
        from src.interfaces.controllers.ai_controller import AIController

        # Leer las configuraciones elegidas en PantallaSeleccion
        app = self.manager.app
        settings = getattr(app, 'game_settings', None)

        # Fallback: si se llega aquí sin pasar por selección, usar valores por defecto
        if not settings:
            settings = {
                'p1': {'tipo': 'Humano', 'mazo': 'src/data/premade_decks/challenges/imagine_a_cool_name.json'},
                'p2': {'tipo': 'Humano', 'mazo': 'src/data/premade_decks/tag_theme/fev_basic_deck.json'}
            }

        nombre_j1 = "Jugador 1"
        nombre_j2 = "Jugador 2" if 'Humano' in settings['p2']['tipo'] else f"IA ({settings['p2']['tipo']})"

        p1 = Player(player_id=0, name=nombre_j1)
        p2 = Player(player_id=1, name=nombre_j2)

        # Definir si P2 (y opcionalmente P1) son IA
        def _dificultad(tipo):
            if 'Fácil' in tipo: return 'EASY'
            if 'Normal' in tipo: return 'MEDIUM'
            return 'HARD'

        self.ai_controller = None
        p1.is_ai = 'Humano' not in settings['p1']['tipo']
        p2.is_ai = 'Humano' not in settings['p2']['tipo']

        if p2.is_ai:
            self.ai_controller = AIController(player_id=1, difficulty=_dificultad(settings['p2']['tipo']), delay=0)
        elif p1.is_ai:
            # IA vs IA (o IA como P1)
            self.ai_controller = AIController(player_id=0, difficulty=_dificultad(settings['p1']['tipo']), delay=0)

        self.game_state = GameState([p1, p2], settings['p1']['mazo'], settings['p2']['mazo'])

        # Limpiar estado de selección previo
        self.carta_seleccionada_index = None
        self.unidad_seleccionada_coords = None
        self._ia_corriendo = False  # Flag para evitar múltiples ticks simultáneos
        self._ia_fallos_consecutivos = 0

        self.actualizar_interfaz_completa()
        self._ejecutar_turno_ia_si_toca()

    def pasar_turno(self, instance):
        from src.domain.action import Action, ActionType
        
        jugador_actual = self.game_state.get_current_player()
        accion = Action(player_id=jugador_actual.id, type=ActionType.END_TURN, payload={})
        
        self.game_state.apply_action(accion)
        self.carta_seleccionada_index = None
        self.unidad_seleccionada_coords = None
        self.actualizar_interfaz_completa()
        # Si el turno pasó a la IA, programar su turno
        self._ejecutar_turno_ia_si_toca()

    def _ejecutar_turno_ia_si_toca(self):
        """Verifica si es el turno de la IA y programa su acción. Evita doble-scheduling."""
        if not self.ai_controller or not self.game_state:
            return
        if getattr(self, '_ia_corriendo', False):
            return  # Ya hay un tick programado, no agregar otro
        jugador_actual = self.game_state.get_current_player()
        es_turno_ia = (
            jugador_actual.id == self.ai_controller.player_id
            and getattr(jugador_actual, 'is_ai', False)
        )
        if es_turno_ia:
            self._ia_corriendo = True
            self._ia_fallos_consecutivos = 0
            Clock.schedule_once(self._tick_ia, 0.6)

    def _tick_ia(self, dt):
        """Ejecuta una sola acción de la IA. Maneja fallos y fin de turno."""
        if not self.ai_controller or not self.game_state:
            self._ia_corriendo = False
            return

        jugador_actual = self.game_state.get_current_player()
        # Guard estricto: verificar que sea el jugador correcto y sea IA
        es_turno_ia = (
            jugador_actual.id == self.ai_controller.player_id
            and getattr(jugador_actual, 'is_ai', False)
        )
        if not es_turno_ia:
            self._ia_corriendo = False
            return

        # Si lleva demasiados fallos, forzar END_TURN para romper el bloqueo
        if self._ia_fallos_consecutivos >= 3:
            print(">> [IA] Demasiados fallos. Forzando fin de turno.")
            accion = Action(player_id=self.ai_controller.player_id, type=ActionType.END_TURN, payload={})
            self.game_state.apply_action(accion)
            self.actualizar_interfaz_completa()
            self._ia_corriendo = False
            return

        accion = self.ai_controller.get_action(self.game_state)
        exito = self.game_state.apply_action(accion)
        self.actualizar_interfaz_completa()

        if accion.type == ActionType.END_TURN:
            self._ia_corriendo = False
            return  # La IA terminó su turno limpiamente

        if not exito:
            # La acción fue rechazada: contar fallo y reintentar pronto
            self._ia_fallos_consecutivos += 1
            print(f">> [IA] Acción rechazada ({self._ia_fallos_consecutivos}/3). Reintentando.")
        else:
            self._ia_fallos_consecutivos = 0

        # Verificar que siga siendo turno de la IA antes de reprogramar
        jugador_tras_accion = self.game_state.get_current_player()
        sigue_siendo_ia = (
            jugador_tras_accion.id == self.ai_controller.player_id
            and getattr(jugador_tras_accion, 'is_ai', False)
        )
        if sigue_siendo_ia:
            Clock.schedule_once(self._tick_ia, 0.4)
        else:
            self._ia_corriendo = False  # El turno cambio al humano

    def reiniciar_partida(self, instance):
        """Vuelve a la pantalla de selección para reiniciar configurando una nueva partida."""
        self._ia_corriendo = False
        self.manager.current = 'selection_screen'

    def volver_al_menu(self):
        self._ia_corriendo = False
        self.manager.current = 'menu_screen'