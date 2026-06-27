import random
import json
import os

class GachaSystem:
    @staticmethod
    def abrir_sobre_avanzado(tipo_banner="GENERAL", cantidad_cartas=3, costo=100, ruta_perfil="src/data/user_profile.json"):
        from src.infrastructure.loaders.card_loader import CardLoader

        if not os.path.exists(ruta_perfil):
            return {"exito": False, "mensaje": "Perfil no encontrado"}

        with open(ruta_perfil, "r", encoding="utf-8") as f:
            perfil = json.load(f)

        if perfil["coins"] < costo:
            return {"exito": False, "mensaje": "¡Monedas insuficientes! 🪙"}

        # 1. CARGAR TODAS LAS CARTAS DEL CSV
        todas_las_cartas = CardLoader.load_units("src/data/cards.csv")
        
        # 2. FILTRAR EL POOL SEGÚN EL BANNER ELEGIDO
        # Aquí mapeamos las temáticas o columnas de tu cards.csv
        if tipo_banner == "FEV":
            # Filtramos solo las que pertenezcan a Fuerzas Especiales Valenzuela
            pool_banner = [c for c in todas_las_cartas if "Fuerzas Especiales Valenzuela" in getattr(c, 'groups', '') or "FEV" in getattr(c, 'groups', '')]
        elif tipo_banner == "TRALALEROS":
            pool_banner = [c for c in todas_las_cartas if "Tralaleros" in getattr(c, 'groups', '')]
        elif tipo_banner == "TRUCOS":
            # Filtramos para que solo salgan cartas de tipo 'spell'
            pool_banner = [c for c in todas_las_cartas if getattr(c, 'card_type', 'unit') == 'spell']
        else:
            # Banner General: entran todas las cartas
            pool_banner = todas_las_cartas

        if not pool_banner:
            pool_banner = todas_las_cartas

        # 3. BUCLE PARA GENERAR LAS RECOMPENSAS
        cartas_ganadas = []
        
        for _ in range(cantidad_cartas):
            # Calculamos la rareza de cada carta individualmente en el sobre
            rareza_elegida = random.choices(
                population=["Común", "Especial", "Épica", "Excelencia"],
                weights=[70, 20, 8, 2],
                k=1
            )[0]
            
            # Filtramos el pool del banner por la rareza que tocó
            pool_rareza = [c for c in pool_banner if getattr(c, 'rarity', 'Común') == rareza_elegida]
            
            # Respaldo si no hay cartas de esa rareza en ese banner específico
            if not pool_rareza:
                pool_rareza = [c for c in todas_las_cartas if getattr(c, 'rarity', 'Común') == rareza_elegida]
            if not pool_rareza:
                pool_rareza = pool_banner
                
            carta_individual = random.choice(pool_rareza)
            cartas_ganadas.append(carta_individual)

            # 4. AGREGAR AL INVENTARIO DEL PERFIL
            card_id_str = str(carta_individual.id)
            if card_id_str in perfil["inventory"]:
                perfil["inventory"][card_id_str] += 1
            else:
                perfil["inventory"][card_id_str] = 1

        # 5. DESCONTAR DINERO Y GUARDAR
        perfil["coins"] -= costo
        with open(ruta_perfil, "w", encoding="utf-8") as f:
            json.dump(perfil, f, indent=2, ensure_ascii=False)

        return {
            "exito": True,
            "cartas": cartas_ganadas,
            "nuevas_monedas": perfil["coins"]
        }