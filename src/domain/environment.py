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

    def on_turn_start(self, game_state, current_player_id):
        # Efectos que se disparan al inicio de cada turno
        if int(self.card.id) == 55: # Sala STEAM
            # Cura 2 a los Dermapatch del jugador actual
            count = 0
            for y in range(game_state.board.height):
                for x in range(game_state.board.width):
                    unit = game_state.board.get_unit_at(x, y)
                    if unit and unit.owner_id == current_player_id:
                        tags = str(getattr(unit, 'groups', '')).lower()
                        if 'dermapatch' in tags or 'derma-patch' in tags:
                            player = game_state.players[current_player_id]
                            if getattr(player, 'cant_heal_turns', 0) == 0:
                                unit.health = min(unit.max_health, unit.health + 2)
                                count += 1
            if count > 0:
                print(f">> [Sala STEAM] ¡{count} aliados Dermapatch se han curado 2 PV al inicio del turno!")