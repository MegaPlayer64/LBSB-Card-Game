from domain.game_state import GameState
from domain.player import Player
from domain.action import Action
from domain.action_type import ActionType


def test_turn_alternation():
    p1 = Player(0, "P1")
    p2 = Player(1, "P2")

    game = GameState([p1, p2])

    assert game.current_player_id == 0
    assert game.turn_number == 1

    # P1 termina turno
    action = Action(ActionType.END_TURN, 0, {})
    game.apply_action(action)

    assert game.current_player_id == 1
    assert game.turn_number == 1

    # P2 termina turno
    action = Action(ActionType.END_TURN, 1, {})
    game.apply_action(action)

    assert game.current_player_id == 0
    assert game.turn_number == 2