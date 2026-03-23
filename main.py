# main.py
import os
import sys

import src.domain.game_state as gs
print(f"DEBUG: Cargando GameState desde: {gs.__file__}")

# Agregamos la carpeta 'src' al path para que Python encuentre tus módulos
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.infrastructure.loaders.card_loader import CardLoader
from src.domain.player import Player
from src.domain.game_state import GameState
from src.application.game_engine import GameEngine
from src.interfaces.controllers.human_controller import HumanController


def start_game():
    # 1. Preparar Datos
    csv_path = "src/data/cards.csv"
    units_data = CardLoader.load_units(csv_path)
    
    # En main.py
    p1 = Player(player_id=0, name="JoseIgnacio")
    p2 = Player(player_id=1, name="Carlitos")
    
    state = GameState([p1, p2])
    
    jose = next((u for u in units_data if u.id == 1), None)
    if jose:
        jose.owner_id = 0  # <--- IMPORTANTE: Debe ser 0 para que el Profe lo mueva
        jose.has_moved = False # Inicializamos por si acaso
        state.board.set_unit_at(1, 1, jose)
        print(f"--- ¡{jose.name} ha entrado al tablero en (1,1)! ---")

    # 5. Configurar Controladores
    # El Jugador 1 es Humano, el Jugador 2 podría ser IA (o también humano por ahora)
    controllers = [HumanController(), HumanController()]
    
    # 6. Ejecutar Motor
    engine = GameEngine(state, controllers)
    print("\nIniciando Motor de Juego LBSB...")
    engine.run()

# main.py

def main():
    while True: # <--- El bucle que mantiene viva la terminal
        # 1. Ejecutamos el juego
        start_game()
        
        # 2. Cuando el juego termina (porque se cerró el loop del engine)
        print("\n" + "="*30)
        print("   ¿PARTIDA TERMINADA?")
        print("="*30)
        
        opcion = input("Presiona 'r' para REINICIAR o cualquier otra tecla para SALIR: ").lower()
        
        if opcion != 'r':
            print("Cerrando el motor LBSB... ¡Nos vemos!")
            break 
        
        # Si eligió 'r', el bucle vuelve a empezar y llama a start_game()
        # Lo que limpia el tablero y recarga el CSV automáticamente.
        print("\n Reiniciando sistema...\n")

if __name__ == "__main__":
    main()