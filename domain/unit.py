class Unit:

    def __init__(self, card, owner_id):
        self.card = card
        self.owner_id = owner_id

        self.base_attack = card.attack
        self.base_health = card.health

        self.speed = card.speed
        self.range = card.range

        self.current_health = self.base_health

        self.has_moved = False
        self.has_attacked = False

    def is_alive(self):
        return self.current_health > 0