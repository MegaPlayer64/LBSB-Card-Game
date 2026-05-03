# --> ACTION TYPES
#
# play_unit         payload: { card_id: str, position: (x,y) }
# play_trick        payload: { card_id: str, targets: ... }
# play_environment  payload: { card_id: str }
# move              payload: { from: (x,y), to: (x,y) }
# attack            payload: { from: (x,y), to: (x,y) }
# attack_base       payload: { from: (x,y) }
# end_turn          payload: {}

from dataclasses import dataclass
from typing import Dict, Any

from .action_type import ActionType


@dataclass(frozen=True)
class Action:
    type: ActionType
    player_id: int
    payload: Dict[str, Any]
    
    def __post_init__(self):
        if self.type == ActionType.MOVE:
            self.payload['from'] = (self.payload['from'][0], self.payload['from'][1])
            self.payload['to'] = (self.payload['to'][0], self.payload['to'][1])

        if self.type == ActionType.ATTACK:
            self.payload['from'] = (self.payload['from'][0], self.payload['from'][1])
            if self.payload['target'] != 'B':
                self.payload['target'] = (self.payload['target'][0], self.payload['target'][1])

    #Play_unit
    #play_trick
    #play_environment
    #move
    #attack
    #attack_base
    #end_turn