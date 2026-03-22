# src/domain/game_state.py
from typing import List
from domain.player import Player
from domain.action import Action
from domain.action_type import ActionType
from domain.board import Board

class GameState:
    def __init__(self, players: List[Player]):
        self.players = players
        self.board = Board(width=5, height=5)
        self.current_player_id = 0
        self.turn_number = 1
        self.game_over = False

    def get_current_player(self) -> Player:
        return self.players[self.current_player_id]

    def validate_action(self, action: Action) -> bool:
        # Este print TE CONFIRMARÁ que estás en el archivo correcto
        print(f"\n>>> [SISTEMA] Validando: {action.type.name}")
        
        if action.type == ActionType.END_TURN:
            print(">>> [SISTEMA] Fin de turno ACEPTADO")
            return True

        if action.type == ActionType.MOVE:
            # Dejamos pasar el movimiento para probar que el Jose camina
            print(f">>> [SISTEMA] Movimiento ACEPTADO")
            return True 
            
        return False

    def apply_action(self, action: Action):
        if not self.validate_action(action):
            return False

        if action.type == ActionType.MOVE:
            fx, fy = action.payload['from']
            tx, ty = action.payload['to']
            self.board.move_unit(fx, fy, tx, ty)
        
        elif action.type == ActionType.END_TURN:
            self._end_turn()
            
        return True

    def _end_turn(self):
        self.current_player_id = 1 - self.current_player_id
        # Solo aumentamos turno cuando vuelve al jugador 0
        if self.current_player_id == 0:
            self.turn_number += 1
        self.get_current_player().refresh_energy()