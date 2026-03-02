class GameEngine:

    def __init__(self, game_state, controllers):
        self.game_state = game_state
        self.controllers = controllers

    def run(self):
        while not self.game_state.game_over:
            current_id = self.game_state.current_player_id
            controller = self.controllers[current_id]

            action = controller.get_action(self.game_state)
            self.game_state.apply_action(action)