# main.py
import os
import sys

# Agregamos la carpeta 'src' al path para que Python encuentre tus módulos
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    from src.infrastructure.loaders.card_loader import CardLoader
    from src.domain.player import Player
    from src.domain.game_state import GameState
    from src.application.game_engine import GameEngine
    from src.interfaces.controllers.human_controller import HumanController
    from src.interfaces.controllers.ai_controller import AIController
    from src.interfaces.view import ConsoleView
except ImportError as e:
    print(f"\n[ERROR CRITICO] Fallo de importación, posible dependencia circular: {e}\n")
    sys.exit(1)


def start_integration_test():
    print("\n" + "="*40)
    print("   INICIANDO TEST DE INTEGRACIÓN LBSB   ")
    print("="*40)

    # 1. Inicializar CardLoader
    print("\n[1] Cargando Base de Datos de Cartas...")
    csv_path = "src/data/cards.csv"
    all_cards = CardLoader.load_units(csv_path)
    print(f" -> Cartas cargadas exitosamente: {len(all_cards)} (Incluye Unidades, Spells y Buildings)")

    # 2. Configurar Jugadores
    print("\n[2] Configurando Jugadores...")
    p1 = Player(player_id=0, name="Jugador 1")
    p2 = Player(player_id=1, name="Jugador 2")
    
    # 3. Instanciar Motor y Estado
    print("\n[3] Instanciando GameState y Tablero 6x5...")
    # NOTA: Al instanciar GameState, internamente se cargan los mazos, se barajan y se roban 5 cartas a cada Jugador.
    state = GameState([p1, p2])
    controllers = [HumanController(), AIController(player_id=1)]
    engine = GameEngine(state, controllers)
    view = ConsoleView()

    # 4. Imprimir Estado Actual Post-Robo Inicial
    print("\n[4] Verificando Estado Inicial...")
    print(f" -> {p1.name} | Vida: {p1.health} HP | Cartas en mano: {len(p1.hand)} | Mazo restante: {len(p1.deck)}")
    print(f" -> {p2.name} | Vida: {p2.health} HP | Cartas en mano: {len(p2.hand)} | Mazo restante: {len(p2.deck)}")

    print("\n[5] Dibujando Tablero Inicial Limpio:")
    view.draw_board(state)

    print("\n[6] Iniciando Loop de Juego.")
    print(" -> INSTRUCCIÓN PARA TEST: Selecciona la acción [4] Jugar Carta.")
    print(" -> Prueba invocar una unidad para el J1 en X >= 2 (Debería fallar por restricción de zona).")
    print(" -> Prueba invocar una unidad para el J1 en X < 2  (Debería ser exitoso).")
    print("-" * 40 + "\n")

    # Arrancamos el motor
    engine.run()


def main():
    while True:
        try:
            start_integration_test()
        except Exception as e:
            print(f"\n[!] Error Inesperado durante la partida: {e}")
            
        print("\n" + "="*30)
        print("   ¿TEST FINALIZADO?")
        print("="*30)
        opcion = input("Presiona 'r' para REINICIAR el Test o cualquier otra tecla para SALIR: ").lower()
        
        if opcion != 'r':
            print("Cerrando el entorno de test... ¡Nos vemos!")
            break 
            
        print("\nReiniciando sistema...\n")


if __name__ == "__main__":
    main()