class Player:

    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name

        self.health = 30

        self.deck = []
        self.hand = []

        self.max_energy = 0
        self.current_energy = 0

    def refresh_energy(self):
        self.max_energy += 1
        self.current_energy = self.max_energy