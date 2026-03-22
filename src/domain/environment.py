class Environment:

    def __init__(self, card, owner_id):
        self.card = card
        self.owner_id = owner_id

    def apply_static(self, game_state):
        pass

    def on_owner_turn_start(self, game_state):
        pass