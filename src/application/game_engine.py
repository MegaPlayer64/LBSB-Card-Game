# src/application/game_engine.py
from interfaces.view import ConsoleView

class GameEngine:
    def __init__(self, game_state, controllers):
        self.game_state = game_state
        self.controllers = controllers
        self.view = ConsoleView() # Podríamos inyectar la vista que queramos

    def run(self):
        self.view.show_message("¡El motor ha arrancado!")
        
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

            self.game_state.apply_action(action)
            
            if action.type.name == "END_TURN":
                self.view.show_message(f"Fin del turno de {player.name}")