# src/interfaces/controllers/human_controller.py
from .base_controller import BaseController
from domain.action import Action
from domain.action_type import ActionType

class HumanController(BaseController):
    def get_action(self, game_state) -> Action:
        print(f"\n--- Turno de {game_state.get_current_player().name} ---")
        
        while True:
            try:
                print("Opciones: [1] Mover Unidad, [2] Atacar, [3] Terminar Turno, [4] Jugar Carta")
                opcion = input("Selecciona una opción: ")

                if opcion == "3":
                    return Action(ActionType.END_TURN, int(game_state.current_player_id), {})

                if opcion == "4":
                    player = game_state.get_current_player()
                    if not player.hand:
                        print(">> No tienes cartas en la mano.")
                        continue
                        
                    print("--- Mano ---")
                    for i, card in enumerate(player.hand):
                        print(f"[{i}] {card.name} (Coste: {card.cost}, Tipo: {card.card_type})")
                        
                    card_idx = int(input("Selecciona el índice de la carta a jugar: "))
                    if not (0 <= card_idx < len(player.hand)):
                        print(">> Índice inválido.")
                        continue
                        
                    card = player.hand[card_idx]
                    tx, ty = -1, -1
                    if card.card_type.lower() == 'unit':
                        print(f">> Invocando unidad. Recuerda las zonas (Jugador 1: X<2, Jugador 2: X>3)")
                        tx = int(input("Hacia X (invocación): "))
                        ty = int(input("Hacia Y (invocación): "))
                    else:
                        print(f">> Jugando {card.card_type} '{card.name}'. Costará {card.cost} de energía.")
                        
                    return Action(
                        type=ActionType.PLAY_CARD,
                        player_id=int(game_state.current_player_id),
                        payload={'card_index': card_idx, 'to': (tx, ty)}
                    )

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
                    
                    target_str = input("Objetivo X (o 'B' para Base Enemiga): ").strip().upper()
                    if target_str == 'B':
                        tx, ty = 'B', 'B'
                    else:
                        tx = int(target_str)
                        ty = int(input("Objetivo Y: "))
                    
                    return Action(
                        type=ActionType.ATTACK,
                        player_id=game_state.current_player_id,
                        payload={'from': (fx, fy), 'target': (tx, ty)}
                    )

            except ValueError:
                print("Error: Por favor ingresa números válidos.")