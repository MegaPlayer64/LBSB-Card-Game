from abc import ABC, abstractmethod
from domain.game_state import GameState
from domain.action import Action # <--- FALTA ESTO

class BaseController(ABC):
    @abstractmethod
    def get_action(self, game_state: GameState) -> Action:
        pass