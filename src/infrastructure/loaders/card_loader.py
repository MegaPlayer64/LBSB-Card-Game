file_path = "src/data/cards.csv"
import csv
from src.domain.unit import Unit
# from domain.skills.registry import SkillRegistry

class CardLoader:
    @staticmethod
    def load_units(file_path):
        units = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    c_type = str(row.get('CardType', '')).lower().strip()
                    if not c_type:
                        c_type = 'unit'

                    # Limpieza de datos numéricos (maneja el caso de los .0 del CSV y valores N/A)
                    def safe_int(val, default=0):
                        if not val or str(val).strip().upper() == 'N/A' or str(val).strip() == '-':
                            return default
                        try:
                            return int(float(val))
                        except:
                            return default

                    # Instanciamos la unidad con TODOS los argumentos que pide Unit.__init__
                    if c_type == 'unit':
                        new_unit = Unit(
                            id=safe_int(row['ID']),
                            name=row['Nombre'],
                            cost=safe_int(row['Coste']),
                            health=safe_int(row['Vida']),
                            attack=safe_int(row['Ataque']),
                            speed=safe_int(row['Velocidad']),
                            range_atk=safe_int(row['Rango_ataque'], default=1),
                            groups=row.get('Grupos', ''),
                            rarity=row.get('Rareza', 'Común'),
                            description=row.get('Descripción habilidad especial', '')
                        )
                        units.append(new_unit)
                    else:
                        from src.domain.card import Card
                        new_card = Card(
                            id=safe_int(row['ID']),
                            name=row['Nombre'],
                            card_type=c_type,
                            cost=safe_int(row['Coste']),
                            groups=row.get('Grupos', ''),
                            rarity=row.get('Rareza', 'Común'),
                            description=row.get('Descripción habilidad especial', '')
                        )
                        units.append(new_card)
            return units
        except Exception as e:
            print(f"Error al leer el CSV: {e}")
            return []

    @staticmethod
    def load_deck(deck_recipe_path, csv_path="src/data/cards.csv"):
        import json
        import copy
        try:
            with open(deck_recipe_path, 'r', encoding='utf-8') as f:
                card_ids = json.load(f)
            
            all_units = CardLoader.load_units(csv_path)
            units_by_id = {u.id: u for u in all_units}
            
            deck = []
            for cid in card_ids:
                if cid in units_by_id:
                    deck.append(copy.deepcopy(units_by_id[cid]))
                else:
                    print(f"[!] Warning: Carta con ID {cid} no encontrada en la base de datos.")
            return deck
        except Exception as e:
            print(f"Error al cargar el mazo {deck_recipe_path}: {e}")
            return []