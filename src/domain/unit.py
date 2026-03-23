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

    def take_damage(self, amount: int) -> bool:
        """Resta vida y devuelve True si la unidad murió."""
        self.health -= amount
        print(f">> {self.name} recibió {amount} de daño! (Vida restante: {self.health})")
        return self.health <= 0

    def reset_turn(self):
        """Limpia las banderas al final del turno."""
        self.has_moved = False
        self.has_attacked = False