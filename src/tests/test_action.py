from domain.action import Action
from domain.action_type import ActionType


def test_action_creation():
    action = Action(ActionType.END_TURN, 0, {})

    assert action.type == ActionType.END_TURN
    assert action.player_id == 0
    assert action.payload == {}