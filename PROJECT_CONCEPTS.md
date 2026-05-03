Nombre del Proyecto: LBSB-Card-Game (v2.0)

Género: TCG Táctico / Estrategia por turnos.

Ambientación: Entorno escolar basado en la convivencia grupal de un colegio de Santiago, Chile.

Pilar Creativo: El juego se basa en las interacciones y grupos sociales ("Tags") del mundo real, traduciéndolos a mecánicas de combate y sinergia.

Lenguaje: Python

Motor: Pygame
Persistencia de Datos: JSON
Plataformas objetivo: Windows, Linux, MacOS, Android y IOS.

Estado Actual: Desarrollo del motor base.

¿De qué se trata?
Es un juego de cartas coleccionables 1 vs 1, donde los jugadores pueden robar cartas de su deck y colocarlas en el campo de juego para atacar a su oponente. El objetivo es reducir la vida del oponente a 0.

¿Cómo funciona?
Los jugadores comienzan con una mano de cartas (5 en total) y un mazo (40 cartas en total). En cada turno, los jugadores pueden robar una carta de su mazo y colocarla en el campo de juego. Las cartas pueden ser de diferentes tipos, como criaturas, hechizos y entornos. Cada carta tiene diferentes estadísticas. Los jugadores pueden usar sus cartas para atacar a su oponente y defenderse de sus ataques. El tablero es de 5x6 casillas. Estando en cada extremo (Ancho) la base de cada jugador, teniendo sus primeras 2 columnas como su zona para invocar cartas, el resto son casillas neutrales. Los jugadores comienzan con 80 de vida, y el objetivo es reducir la vida del oponente a 0.

Cartas:
Las cartas son el núcleo del juego, habiendo 3 tipos: Unidades, Hechizos y Entornos. Cada carta tiene diferentes estadísticas y habilidades.

Unidades: Son los personajes que luchan en el campo de juego. Cada unidad tiene diferentes estadísticas, pudiendo atacar y ser movidas una vez por turno (Con excepciones si indica la habilidad).

Hechizos: Son cartas que realizan acciones especiales. Cada hechizo tiene diferentes efectos, como causar daño, curar unidades o robar cartas. Los jugadores pueden usar sus hechizos para obtener ventaja en el campo de juego.

Entornos: Son cartas que modifican las reglas del juego. Cada entorno tiene diferentes efectos, como aumentar el poder de las unidades. Los jugadores pueden usar sus entornos para obtener ventaja en el campo de juego. Solo puede haber uno activo, afectando ambos jugadores.

Estadísticas de las cartas.
    Costo: Esta indica cuanto poder cuesta jugar la carta.
    Vida: Esta indica cuanta salud posee cada carta
    Ataque: Esta indica cuanto daño puede hacer la carta al atacar
    Velocidad: Esta indica cuantas casillas se puede mover una carta (Calculado con la formula de Distancia de Manhattan)
    Rango de Ataque: Esta indica cuantas casillas puede atacar la carta (Calculado con la formula de la Máxima diferencia entre ejes, permitiendo alcance ortogonal y diagonal)
    Grupos/Tags: Esta indica a que grupos pertenece una carta, dando sinergias con otras cartas.
    Habilidades Especiales: Estas son efectos especiales que tiene la carta.

Otras Estadísticas de las cartas.
    Ilustrador: Esta indica quien dibujo la carta.
    Numero de Carta: Esta indica el numero de la carta.
    Rareza: Esta indica la rareza de la carta. (Habiendo comúnes, especiales, épicas, excelencias y de evento.)
    Imagen: Esta indica la imagen de la carta.
    Temática: Esta indica la temática de la carta.
    
### RESTRICTED TAGS & CONTENT (DO NOT OVERRIDE)

Tags permitidos: Solo etiquetas basadas en grupos sociales del colegio y pasatiempos (ej. "FEV", "CT", "3_NAI", "Tecnologíco", "Artista", "Aestetic", etc.).

Prohibido: No generar etiquetas basadas en orientaciones sexuales, identidades de género o relaciones sentimentales. El juego se enfoca estrictamente en la convivencia escolar y la amistad.

Fiel al CSV: Cualquier sugerencia de carta nueva debe derivar de la estética y los grupos ya definidos en la tabla de 61 cartas.