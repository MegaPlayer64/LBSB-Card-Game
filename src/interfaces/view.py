# src/interfaces/view.py

class ConsoleView:
    @staticmethod
    def draw_board(game_state):
        board = game_state.board
        print("\n      TABLERITO LBSB 5x5")
        print("      0   1   2   3   4")
        print("    +---+---+---+---+---+")
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
            print("    +---+---+---+---+---+")
        print("\n")

    @staticmethod
    def show_message(message):
        print(f">> {message}")