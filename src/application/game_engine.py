# src/application/game_engine.py
from interfaces.view import ConsoleView

class GameEngine:
    def __init__(self, game_state, controllers):
        self.game_state = game_state
        self.controllers = controllers
        self.view = ConsoleView() # Podríamos inyectar la vista que queramos

    def draw_card(self, player_id):
        player = self.game_state.players[player_id]
        if player.deck:
            if len(player.hand) < 10:
                card = player.deck.pop(0)
                player.hand.append(card)
                self.view.show_message(f">>> {player.name} ha robado una carta.")

    def _start_turn_phase(self, player):
        self.view.clear_screen()
        # 1. Validación de Energía ($Energía = Turno$)
        expected_energy = self.game_state.turn_number
        player.max_energy = expected_energy
        player.current_energy = player.max_energy
        
        # 2. Reset de unidades del jugador
        for y in range(self.game_state.board.height):
            for x in range(self.game_state.board.width):
                unit = self.game_state.board.get_unit_at(x, y)
                if unit and getattr(unit, 'owner_id', None) == player.id:
                    if hasattr(unit, 'reset_turn_state'):
                        unit.reset_turn_state()
                    
        # 3. Feedback en Consola
        self.view.show_message(f">> [Sistema] Las unidades de {player.name} están listas para la acción.")

    def run(self):
        self.view.show_message("¡El motor ha arrancado!")
        
        # Fase de Inicio de Turno (Primer Turno)
        first_player = self.game_state.get_current_player()
        self._start_turn_phase(first_player)
        self.draw_card(first_player.id)
        
        while not self.game_state.game_over:
            # Dibujamos usando la interfaz de vista
            self.view.draw_board(self.game_state)
            
            current_id = self.game_state.current_player_id
            player = self.game_state.get_current_player()
            controller = self.controllers[current_id]

            print(f"--- TURNO DE: {player.name} (Energía: {player.current_energy}) ---")

            action = None
            while True:
                try:
                    action = controller.get_action(self.game_state)
                    if self.game_state.validate_action(action):
                        break
                    else:
                        self.view.show_message("[!] Jugada inválida. Revisa las reglas.")
                except Exception as e:
                    self.view.show_message(f"[!] Error: {e}")

            unit_played = None
            if action.type.name == "PLAY_CARD":
                card_index = action.payload.get('card_index')
                if 0 <= card_index < len(player.hand):
                    card = player.hand[card_index]
                    if card.card_type.lower() in ('environment', 'building'):
                        from domain.environment import Environment
                        self.game_state.active_environment = Environment(card, player.id)
                        self.view.show_message(f"¡El entorno ha cambiado a {card.name}!")
                    elif card.card_type.lower() == 'unit':
                        unit_played = card

            self.game_state.apply_action(action)
            
            if unit_played and hasattr(unit_played, 'on_enter'):
                unit_played.on_enter(self.game_state)
            
            if action.type.name == "END_TURN":
                self.view.show_message(f"Fin del turno de {player.name}")
                # Fase de Inicio de Turno (Siguientes Turnos)
                next_player_id = self.game_state.current_player_id
                next_player = self.game_state.players[next_player_id]
                self._start_turn_phase(next_player)
                self.draw_card(next_player_id)