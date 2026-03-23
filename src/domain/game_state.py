# src/domain/game_state.py
from typing import List
# Imports directos ya que están en la misma carpeta domain/
from src.domain.player import Player
from src.domain.action import Action
from src.domain.action_type import ActionType
from src.domain.board import Board

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
        if self.game_over: return False
        if int(action.player_id) != int(self.current_player_id): return False

        if action.type.name == "END_TURN":
            return True

        if action.type.name == "MOVE":
            fx, fy = action.payload['from']
            tx, ty = action.payload['to']

            # 1. ¿Está dentro del mapa (0-4)?
            if not self.board.is_within_bounds(tx, ty):
                print(f">> [!] Fuera del tablero: ({tx}, {ty})")
                return False

            # 2. ¿Hay alguien en el origen?
            unit = self.board.get_unit_at(fx, fy)
            if not unit:
                print(f">> [!] No hay unidad en ({fx}, {fy})")
                return False

            # 3. ¿La unidad ya se movió este turno?
            if getattr(unit, 'has_moved', False):
                print(f">> [!] {unit.name} ya se movió en este turno.")
                return False

            # 4. ¿La casilla de destino está ocupada?
            if self.board.is_occupied(tx, ty):
                print(f">> [!] Casilla ({tx}, {ty}) ya está ocupada.")
                return False

            # 5. ¿Tiene suficiente velocidad (Manhattan Distance)?
            dist = abs(fx - tx) + abs(fy - ty)
            if dist > unit.speed:
                print(f">> [!] {unit.name} no llega. Distancia: {dist}, Velocidad: {unit.speed}")
                return False

            return True
        elif action.type.name == "END_TURN":
            self._end_turn()
            return True
        
        if action.type.name == "ATTACK":
            fx, fy = action.payload['from']
            tx, ty = action.payload['target']

            attacker = self.board.get_unit_at(fx, fy)
            target = self.board.get_unit_at(tx, ty)

            # 1. ¿Existen ambos?
            if not attacker or not target:
                print(">> [!] Atacante o blanco inexistente.")
                return False

            # 2. ¿El atacante es tuyo y el blanco NO?
            if attacker.owner_id != action.player_id:
                print(">> [!] No puedes ordenar atacar a una unidad que no es tuya.")
                return False
            if target.owner_id == action.player_id:
                print(">> [!] ¡Fuego amigo! No puedes atacar a tus aliados.")
                return False

            # 3. ¿Ya atacó?
            if getattr(attacker, 'has_attacked', False):
                print(f">> [!] {attacker.name} ya agotó su ataque este turno.")
                return False

            # 4. ¿Está en rango (Manhattan)?
            dist = abs(fx - tx) + abs(fy - ty)
            if dist > attacker.range_atk: # Usamos el nombre del CSV
                print(f">> [!] Objetivo fuera de rango. Distancia: {dist}, Rango: {attacker.range_atk}")
                return False

            return True
        
        return False
    
    def apply_action(self, action: Action) -> bool:
        if not self.validate_action(action):
            return False

        if action.type.name == "MOVE":
            fx, fy = action.payload['from']
            tx, ty = action.payload['to']
            
            # Realizamos el movimiento en el tablero
            unit = self.board.get_unit_at(fx, fy)
            self.board.move_unit(fx, fy, tx, ty)
            
            # Marcamos la unidad como "ya movida"
            unit.has_moved = True
            print(f">> {unit.name} se movió a ({tx}, {ty})")

        elif action.type.name == "ATTACK":
            fx, fy = action.payload['from']
            tx, ty = action.payload['target']
            
            attacker = self.board.get_unit_at(fx, fy)
            target = self.board.get_unit_at(tx, ty)

            # Aplicar daño
            murió = target.take_damage(attacker.attack)
            attacker.has_attacked = True
            
            if murió:
                print(f">>> ¡{target.name} ha sido derrotado! <<<")
                self.board.remove_unit(tx, ty)
            
        elif action.type.name == "END_TURN":
            self._end_turn()
            
        return True
    


    def _end_turn(self):
        # 1. Resetear el estado de todas las unidades antes de cambiar de jugador
        for y in range(self.board.height):
            for x in range(self.board.width):
                unit = self.board.get_unit_at(x, y)
                if unit:
                    unit.has_moved = False
                    # unit.has_attacked = False  <-- Lo usaremos pronto

        # 2. Cambiar de jugador
        self.current_player_id = 1 - self.current_player_id
        if self.current_player_id == 0:
            self.turn_number += 1
            
        self.get_current_player().refresh_energy()
        print(f"\n--- Turno finalizado. Ahora es el turno de {self.get_current_player().name} ---")