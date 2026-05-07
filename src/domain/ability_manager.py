from src.domain import unit
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
        print(">> [Habilidad Josefa A]: Buscando aliado para proteger...")
        target = None

        if getattr(unit.owner, 'is_ai', False):
            # La IA busca al aliado con más vida para hacerlo un "tanque"
            aliados = [u for u in game_state.board.get_all_units() if u.owner_id == unit.owner_id and u != unit]
            if aliados:
                target = max(aliados, key=lambda u: u.health)
        else:
            try:
                tx = int(input("Aliado X: "))
                ty = int(input("Aliado Y: "))
                target = game_state.board.get_unit_at(tx, ty)
            except ValueError: return

        if target and target.owner_id == unit.owner_id:
            target.has_shield = True
            print(f">> ¡{target.name} recibió el Escudo de Josefa A!")
        else:
            print(">> No se encontró un aliado válido. El escudo se desperdició.")

    @staticmethod
    def _richi_on_enter(unit, game_state):
        # Escudo a si mismo
        unit.has_shield = True
        print(f">> ¡{unit.name} ha recibido un Escudo (mitad de daño en el próximo ataque)!")

    @staticmethod
    def _kapsi_on_attack(unit, game_state):
        print(f">> [Habilidad Kapsi]: Reubicación táctica activada.")
        pos = None
        for y in range(5):
            for x in range(6):
                if game_state.board.get_unit_at(x, y) == unit:
                    pos = (x, y)
                    break
            if pos: break
            
        fx, fy = pos
        tx, ty = None, None

        if getattr(unit.owner, 'is_ai', False):
            # La IA de Kapsi busca una casilla vacía cerca para retroceder
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = fx + dx, fy + dy
                    if game_state.board.is_within_bounds(nx, ny) and not game_state.board.is_occupied(nx, ny):
                        tx, ty = nx, ny
                        break
        else:
            try:
                tx = int(input("Nueva posición X: "))
                ty = int(input("Nueva posición Y: "))
            except ValueError: return

        if tx is not None and game_state.board.is_within_bounds(tx, ty) and not game_state.board.is_occupied(tx, ty):
            game_state.board.move_unit(unit, tx, ty)
            print(f">> Kapsi se retiró a ({tx}, {ty})")

    @staticmethod
    def _amira_presidenta_on_attack(unit, game_state):
        # Da +1 de daño a todas las unidades aliadas
        unit.static_abilities.append({"type": "buff_all_attack", "amount": 1})

    @staticmethod
    def _chino_quemadas_on_damage_received(unit, damage, game_state):
        if getattr(unit, 'ability_used_this_turn', False):
            return damage
        
        # Definimos el origen (donde está Chino ahora) 
        pos = None
        for y in range(5):
            for x in range(6):
                if game_state.board.get_unit_at(x, y) == unit:
                    pos = (x, y)
                    break
            if pos: break

        if not pos:
            return damage # Por si acaso no se encuentra
            
        fx, fy = pos # ¡Ahora sí tenemos fx y fy!
        effective_speed = game_state.get_effective_stats(unit)["speed"]

        # --- Lógica de Decisión ---
        tx, ty = None, None

        if getattr(unit.owner, 'is_ai', False):
            # LA IA BUSCA ESCAPAR: Busca la primera casilla válida en su rango de velocidad
            print(f">> [IA] Chino Quemadas está calculando una ruta de escape...")
            for dx in range(-effective_speed, effective_speed + 1):
                for dy in range(-effective_speed, effective_speed + 1):
                    temp_tx, temp_ty = fx + dx, fy + dy
                    dist = abs(fx - temp_tx) + abs(fy - temp_ty)
                    
                    # Usamos tus validaciones del board
                    if dist <= effective_speed and dist > 0:
                        if game_state.board.is_within_bounds(temp_tx, temp_ty) and not game_state.board.is_occupied(temp_tx, temp_ty):
                            tx, ty = temp_tx, temp_ty
                            break # Encontró un lugar y se escapa
                if tx is not None: break
        else:
            # JUGADOR HUMANO
            print(f">> [Habilidad Chino Quemadas]: ¡Recibiste daño! ¿Quieres moverte para anularlo?")
            try:
                if input("¿Moverse? (y/n): ").lower() == 'y':
                    tx = int(input("Nueva posición X: "))
                    ty = int(input("Nueva posición Y: "))
                else:
                    return damage
            except ValueError:
                return damage

        # --- Validación Final y Ejecución ---
        if tx is not None and ty is not None:
            dist = abs(fx - tx) + abs(fy - ty)
            
            # Aquí es donde usas la lógica que ya tienes en validate_action (pero manual)
            if game_state.board.is_within_bounds(tx, ty) and not game_state.board.is_occupied(tx, ty) and dist <= effective_speed:
                game_state.board.move_unit(unit, tx, ty)
                print(f">> ¡ESQUIVA! Chino se movió a ({tx}, {ty}) y anuló los {damage} de daño.")
                unit.ability_used_this_turn = True
                return 0
            else:
                print(">> [!] Movimiento de evasión inválido. Chino recibió el impacto.")
        
        return damage