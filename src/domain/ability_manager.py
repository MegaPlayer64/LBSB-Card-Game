class AbilityManager:
    @staticmethod
    def trigger_on_enter(unit, game_state):
        if int(unit.id) == 28:
            AbilityManager._cristobal_on_enter(unit, game_state)
        elif int(unit.id) == 29:
            AbilityManager._najib_on_enter(unit, game_state)
        elif int(unit.id) == 30:
            AbilityManager._crisby_on_enter(unit, game_state)
        elif int(unit.id) == 31:
            AbilityManager._josefa_a_on_enter(unit, game_state)
        elif int(unit.id) == 17:
            AbilityManager._richi_on_enter(unit, game_state)

    @staticmethod
    def trigger_on_attack(unit, game_state):
        if int(unit.id) == 3:
            AbilityManager._kapsi_on_attack(unit, game_state)
        if int(unit.id) == 57:
            AbilityManager._amira_presidenta_on_attack(unit, game_state)

    @staticmethod
    def trigger_on_damage_received(unit, damage, game_state):
        if int(unit.id) == 61:
            AbilityManager._chino_quemadas_on_damage_received(unit, damage, game_state)

    @staticmethod
    def _cristobal_on_enter(unit, game_state):
        # Robar carta. Si es truco, cura 4 a un aliado.
        player = game_state.players[unit.owner_id]
        if player.deck:
            drawn_card = player.deck.pop(0)
            player.hand.append(drawn_card)
            print(f">> [Habilidad Cristobal]: Robaste {drawn_card.name}")
            if drawn_card.card_type.lower() in ('spell', 'trick'):
                # Curación de 4 a un aliado. Por simplicidad, se cura a sí mismo por ahora.
                unit.health += 4
                print(f">> ¡La carta es un truco! Cristobal se curó 4 HP. Vida actual: {unit.health}")
        else:
            print(">> [Habilidad Cristobal]: Mazo vacío, no se puede robar.")

    @staticmethod
    def _najib_on_enter(unit, game_state):
        # Mirar 3 cartas del mazo enemigo, poner 1 al fondo.
        enemy_id = 1 - unit.owner_id
        enemy = game_state.players[enemy_id]
        if len(enemy.deck) > 0:
            top_cards = enemy.deck[:3]
            print(">> [Habilidad Najib]: Cartas en el tope del mazo enemigo:")
            for i, c in enumerate(top_cards):
                print(f"[{i}] {c.name}")
            
            try:
                choice = int(input("Selecciona el índice de la carta a poner al fondo: "))
                if 0 <= choice < len(top_cards):
                    card_to_bottom = top_cards.pop(choice)
                    enemy.deck.remove(card_to_bottom)
                    enemy.deck.append(card_to_bottom)
                    print(f">> {card_to_bottom.name} enviada al fondo del mazo enemigo.")
                else:
                    print(">> Selección inválida, se omite el efecto.")
            except ValueError:
                print(">> Entrada inválida, se omite el efecto.")
    
    @staticmethod
    def _crisby_on_enter(unit, game_state):
        # Próxima carta coste 4 o menos cuesta 1 menos este turno
        player = game_state.players[unit.owner_id]
        # Dejamos la variable lista para ser leída por el sistema de maná
        player.cost_reduction_active = True 
        print(f">> [Habilidad Crisby]: Tu próxima carta de coste 4 o menos costará 1 menos este turno.")

    @staticmethod
    def _josefa_a_on_enter(unit, game_state):
        # Escudo a aliado
        print(">> [Habilidad Josefa A]: Selecciona a un aliado para darle Escudo.")
        try:
            tx = int(input("Aliado X: "))
            ty = int(input("Aliado Y: "))
            target = game_state.board.get_unit_at(tx, ty)
            if target and target.owner_id == unit.owner_id:
                target.has_shield = True
                print(f">> ¡{target.name} ha recibido un Escudo (mitad de daño en el próximo ataque)!")
            else:
                print(">> Objetivo inválido, el escudo se pierde.")
        except ValueError:
            print(">> Coordenadas inválidas, el escudo se pierde.")

    @staticmethod
    def richi_on_enter(unit, game_state):
        # Escudo a si mismo
        unit.has_shield = True
        print(f">> ¡{unit.name} ha recibido un Escudo (mitad de daño en el próximo ataque)!")

    @staticmethod
    def kapsi_on_attack(unit, game_state):
        # Se mueve posterior al ataque
        print(">> [Habilidad Kapsi]: Selecciona a dónde moverte.")
        try:
            tx = int(input("Nueva posición X: "))
            ty = int(input("Nueva posición Y: "))
            if game_state.board.is_valid_move(tx, ty, unit):
                game_state.board.move_unit(unit, tx, ty)
                print(f">> Kapsi se movió a ({tx}, {ty})")
            else:
                print(">> Movimiento inválido, Kapsi se queda donde está.")
        except ValueError:
            print(">> Coordenadas inválidas, Kapsi se queda donde está.")

    @staticmethod
    def _amira_presidenta_on_attack(unit, game_state):
        # Da +1 de daño a todas las unidades aliadas
        unit.static_abilities.append({"type": "buff_all_attack", "amount": 1})