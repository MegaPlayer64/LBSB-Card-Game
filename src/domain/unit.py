from .card import Card

class Unit(Card):
    def __init__(self, id, name, cost, health, attack, speed, range_atk, groups, rarity, description):
        # Pasamos los datos a la clase madre Card
        super().__init__(
            id=id, 
            name=name, 
            card_type="unit", 
            cost=cost, 
            groups=groups, 
            rarity=rarity, 
            description=description
        )
        # Atributos específicos de la unidad en el tablero 5x5
        self.max_health = health
        self.current_health = health
        self.attack = attack
        self.speed = speed
        self.range_atk = range_atk
        
        # Posición inicial (fuera del tablero)
        self.pos_x = -1
        self.pos_y = -1

    def take_damage(self, amount: int):
        self.current_health -= amount
        return self.current_health <= 0