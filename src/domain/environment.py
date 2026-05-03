class Environment:

    def __init__(self, card, owner_id):
        self.card = card
        self.owner_id = owner_id

    def apply_static(self, game_state):
        # Afecta a ambos jugadores revisando las unidades en el tablero
        for y in range(game_state.board.height):
            for x in range(game_state.board.width):
                unit = game_state.board.get_unit_at(x, y)
                if unit:
                    # Aquí comparamos los grupos/tags de la unidad con los del entorno (self.card)
                    # Ejemplo: if 'Fuerzas Especiales Valenzuela' in unit.groups:
                    #              aplicar_efecto()
                    pass

    def on_owner_turn_start(self, game_state):
        # Efecto específico al inicio del turno del dueño (si lo hubiera)
        pass