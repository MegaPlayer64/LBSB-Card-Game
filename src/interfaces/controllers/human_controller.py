# src/interfaces/controllers/human_controller.py
from .base_controller import BaseController
from domain.action import Action
from domain.action_type import ActionType

class HumanController(BaseController):
    def get_action(self, game_state) -> Action:
        print(f"\n--- Turno de {game_state.get_current_player().name} ---")
        
        while True:
            try:
                print("Opciones: [1] Mover Unidad, [2] Atacar, [3] Terminar Turno")
                opcion = input("Selecciona una opción: ")

                if opcion == "3":
                    return Action(ActionType.END_TURN, int(game_state.current_player_id), {})

                if opcion == "1":
                    # Pedimos coordenadas de origen y destino
                    fx = int(input("Desde X: "))
                    fy = int(input("Desde Y: "))
                    tx = int(input("Hacia X: "))
                    ty = int(input("Hacia Y: "))
                    
                    return Action(
                        type=ActionType.MOVE,
                        player_id=int(game_state.current_player_id), # <--- AQUÍ
                        payload={'from': (fx, fy), 'to': (tx, ty)}
                    )
                
                if opcion == "2":
                    fx = int(input("Atacante X: "))
                    fy = int(input("Atacante Y: "))
                    tx = int(input("Objetivo X: "))
                    ty = int(input("Objetivo Y: "))
                    
                    return Action(
                        type=ActionType.ATTACK,
                        player_id=game_state.current_player_id,
                        payload={'from': (fx, fy), 'target': (tx, ty)}
                    )

            except ValueError:
                print("Error: Por favor ingresa números válidos.")