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
                    # Filtramos solo las que son tipo 'unit' (ignoramos spells por ahora)
                    c_type = str(row.get('CardType', '')).lower().strip()
                    if c_type != 'unit':
                        continue

                    # Limpieza de datos numéricos (maneja el caso de los .0 del CSV)
                    def safe_int(val, default=0):
                        try:
                            return int(float(val)) if val and val.strip() != "" else default
                        except:
                            return default

                    # Instanciamos la unidad con TODOS los argumentos que pide Unit.__init__
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
            return units
        except Exception as e:
            print(f"Error al leer el CSV: {e}")
            return []