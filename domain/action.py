from dataclasses import dataclass
from typing import Dict


@dataclass
class Action:
    type: str
    player_id: int
    payload: Dict
    
    #Play_unit
    #play_trick
    #play_environment
    #move
    #attack
    #attack_base
    #end_turn