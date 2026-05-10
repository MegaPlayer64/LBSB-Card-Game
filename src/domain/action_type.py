from enum import Enum, auto


class ActionType(Enum):
    PLAY_UNIT = auto()
    PLAY_TRICK = auto()
    PLAY_ENVIRONMENT = auto()
    PLAY_CARD = auto()
    PLAY_SPELL = auto()
    ACTIVATE_ABILITY = auto()

    MOVE = auto()
    ATTACK = auto()
    ATTACK_BASE = auto()

    END_TURN = auto()