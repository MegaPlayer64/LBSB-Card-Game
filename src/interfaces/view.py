# src/interfaces/view.py
import os

class ConsoleView:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def draw_board(game_state):
        board = game_state.board
        print("\n      TABLERITO LBSB 6x5")
        print("      0   1   2   3   4   5")
        print("    +---+---+---+---+---+---+")
        for y in range(board.height):
            row_str = f"  {y} |"
            for x in range(board.width):
                unit = board.get_unit_at(x, y)
                if unit:
                    # 'J' para Jose, 'K' para Kapsi, etc.
                    char = unit.name[0].upper() 
                    row_str += f" {char} |"
                else:
                    row_str += " . |"
            print(row_str)
            print("    +---+---+---+---+---+---+")
            
        def get_hp_bar(hp, max_hp=80):
            hp = max(0, hp)
            bars = int((hp / max_hp) * 10)
            return f"[{'=' * bars}{' ' * (10 - bars)}] {hp}/{max_hp} HP"
            
        print(f"\n{game_state.players[0].name} Base: {get_hp_bar(game_state.players[0].health)}")
        print(f"{game_state.players[1].name} Base: {get_hp_bar(game_state.players[1].health)}")
        
        p1 = game_state.players[0]
        print(f"\n--- Mano de {p1.name} ---")
        if p1.hand:
            for i, card in enumerate(p1.hand):
                print(f"[{i}] {card.name} (Coste: {card.cost})")
        else:
            print("(Mano vacía)")
        print("\n")

    @staticmethod
    def show_message(message):
        print(f">> {message}")