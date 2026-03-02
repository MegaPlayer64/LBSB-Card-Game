from .board import Board
from .player import Player
from .environment import Environment


class GameState:

    def __init__(self, players):
        self.players = players
        self.board = Board()

        self.current_player_id = 0
        self.turn_number = 1

        self.environment = None

        self.game_over = False
        
    def apply_action(self, action):
        if action.player_id != self.current_player_id:
            return False

        if action.type == "end_turn":
            self._end_turn()
            return True

        if action.type == "move":
            return self._move(action)

        if action.type == "attack":
            return self._attack(action)

        if action.type == "attack_base":
            return self._attack_base(action)

        if action.type == "play_environment":
            return self._play_environment(action)

        return False
    
    def _end_turn(self):
        self.current_player_id = 1 - self.current_player_id
        self.turn_number += 1

        player = self.players[self.current_player_id]
        player.refresh_energy()

        # Reset unidades
        for x in range(self.board.width):
            for y in range(self.board.height):
                unit = self.board.grid[x][y]
                if unit and unit.owner_id == self.current_player_id:
                    unit.has_moved = False
                    unit.has_attacked = False

        # Trigger entorno
        if self.environment and self.environment.owner_id == self.current_player_id:
            self.environment.on_owner_turn_start(self)