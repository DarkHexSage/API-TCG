#!/usr/bin/env python3
"""
TCG Data Format Analyzer
Analiza las estructuras de One Piece, Yu-Gi-Oh, Pokémon y Magic
para crear un estándar unificado
"""

import json
import csv
from typing import Dict, List, Any
from pathlib import Path

class TCGAnalyzer:
    """Analiza formatos de TCG"""
    
    def __init__(self):
        self.formats = {
            'one_piece': {},
            'yugioh': {},
            'pokemon': {},
            'magic': {}
        }
    
    def analyze_one_piece(self, csv_sample: str):
        """Analizar formato CSV de One Piece"""
        print("\n" + "="*80)
        print("🔍 ONE PIECE CSV FORMAT")
        print("="*80)
        
        # Parsing CSV
        reader = csv.reader([csv_sample])
        headers = [
            'id', 'card_id', 'rarity', 'name', 'image_url', 
            'power', 'character_name', 'color', 'set', 'cost', 
            'card_level', 'price', 'ability', 'unknown', 'unknown2'
        ]
        
        data = next(reader)
        
        print("\nEstructura detectada:")
        for i, (header, value) in enumerate(zip(headers, data)):
            print(f"  {i:2d}. {header:20s} = {value[:50]}")
        
        self.formats['one_piece'] = {
            'source': 'CSV',
            'key_fields': ['id', 'name', 'image_url', 'power', 'color', 'rarity'],
            'optional_fields': ['ability', 'cost', 'character_name'],
            'example': {
                'id': data[1],
                'name': data[3],
                'image_url': data[4],
                'power': data[10],
                'color': data[7],
                'rarity': data[2],
                'card_level': data[9],
                'ability': data[11]
            }
        }
        
        return data
    
    def analyze_yugioh(self, json_sample: Dict):
        """Analizar formato JSON de Yu-Gi-Oh"""
        print("\n" + "="*80)
        print("🔍 YU-GI-OH JSON FORMAT")
        print("="*80)
        
        card = json_sample['data'][0]
        
        print("\nEstructura detectada:")
        for key, value in card.items():
            if isinstance(value, (dict, list)):
                print(f"  {key:25s} = {type(value).__name__}")
            else:
                print(f"  {key:25s} = {str(value)[:50]}")
        
        self.formats['yugioh'] = {
            'source': 'JSON',
            'key_fields': ['id', 'name', 'type', 'desc', 'card_images'],
            'optional_fields': ['archetype', 'ygoprodeck_url', 'card_sets', 'card_prices'],
            'example': {
                'id': card.get('id'),
                'name': card.get('name'),
                'type': card.get('type'),
                'humanReadableType': card.get('humanReadableCardType'),
                'effect': card.get('desc'),
                'image_url': card['card_images'][0]['image_url'] if card.get('card_images') else None,
                'archetype': card.get('archetype'),
                'price': card['card_prices'][0]['tcgplayer_price'] if card.get('card_prices') else None
            }
        }
        
        return card
    
    def analyze_pokemon(self, json_sample: List):
        """Analizar formato JSON de Pokémon"""
        print("\n" + "="*80)
        print("🔍 POKÉMON JSON FORMAT")
        print("="*80)
        
        card = json_sample[0]
        
        print("\nEstructura detectada:")
        for key, value in card.items():
            if isinstance(value, (dict, list)):
                print(f"  {key:25s} = {type(value).__name__}")
            else:
                print(f"  {key:25s} = {str(value)[:50]}")
        
        self.formats['pokemon'] = {
            'source': 'JSON',
            'key_fields': ['id', 'name', 'hp', 'types', 'attacks', 'images'],
            'optional_fields': ['weaknesses', 'resistances', 'evolvesFrom', 'set', 'tcgplayer'],
            'example': {
                'id': card.get('id'),
                'name': card.get('name'),
                'hp': card.get('hp'),
                'type': card.get('types')[0] if card.get('types') else None,
                'image_url': card.get('images', {}).get('large'),
                'attacks': [
                    {
                        'name': atk.get('name'),
                        'damage': atk.get('damage'),
                        'cost': len(atk.get('cost', []))
                    } for atk in card.get('attacks', [])
                ],
                'rarity': card.get('rarity'),
                'price': card.get('tcgplayer', {}).get('prices', {}).get('holofoil', {}).get('market')
            }
        }
        
        return card
    
    def analyze_magic(self, json_sample: List):
        """Analizar formato JSON de Magic"""
        print("\n" + "="*80)
        print("🔍 MAGIC: THE GATHERING JSON FORMAT")
        print("="*80)
        
        card = json_sample[0]
        
        print("\nEstructura detectada:")
        for key, value in card.items():
            if isinstance(value, (dict, list)):
                print(f"  {key:25s} = {type(value).__name__}")
            else:
                print(f"  {key:25s} = {str(value)[:50]}")
        
        self.formats['magic'] = {
            'source': 'JSON',
            'key_fields': ['id', 'name', 'type_line', 'oracle_text', 'image_uris', 'set_name'],
            'optional_fields': ['mana_cost', 'power', 'toughness', 'rarity', 'prices'],
            'example': {
                'id': card.get('id'),
                'name': card.get('name'),
                'type': card.get('type_line'),
                'image_url': card.get('image_uris', {}).get('normal'),
                'effect': card.get('oracle_text'),
                'mana_cost': card.get('mana_cost'),
                'power': card.get('power'),
                'toughness': card.get('toughness'),
                'rarity': card.get('rarity'),
                'set': card.get('set_name'),
                'price': card.get('prices', {}).get('usd')
            }
        }
        
        return card
    
    def find_common_fields(self):
        """Encontrar campos comunes entre todos los TCG"""
        print("\n" + "="*80)
        print("📊 COMMON FIELDS ACROSS ALL TCGs")
        print("="*80)
        
        # Campos que TODOS tienen
        common = {
            'id': 'Identificador único de la carta',
            'name': 'Nombre de la carta',
            'image_url': 'URL de la imagen PNG/JPG',
            'rarity': 'Rareza (Common, Rare, etc)',
            'set_name': 'Set/Expansión',
            'price': 'Precio en mercado',
        }
        
        # Campos específicos por tipo
        print("\n✅ MANDATORY FIELDS (Todos los TCGs):")
        for field, desc in common.items():
            print(f"  • {field:20s} - {desc}")
        
        print("\n📌 GAME-SPECIFIC FIELDS:")
        print("\n  One Piece:")
        print("    • power         - Poder del personaje")
        print("    • color         - Color de la carta")
        print("    • ability       - Habilidad especial")
        
        print("\n  Yu-Gi-Oh:")
        print("    • type          - Tipo de carta (Monster, Spell, Trap)")
        print("    • effect        - Descripción del efecto")
        print("    • archetype     - Arquetipo (ej: Dragon)")
        
        print("\n  Pokémon:")
        print("    • hp            - Puntos de vida")
        print("    • type          - Tipo (Fire, Water, etc)")
        print("    • attacks       - Lista de ataques")
        print("    • weakness      - Debilidad")
        print("    • retreat_cost  - Costo de retiro")
        
        print("\n  Magic:")
        print("    • type          - Tipo de carta (Creature, Spell, etc)")
        print("    • mana_cost     - Costo de maná")
        print("    • effect        - Texto del oráculo")
        print("    • power         - Poder (creatures)")
        print("    • toughness     - Resistencia (creatures)")
        
        return common
    
    def propose_unified_schema(self):
        """Proponer esquema unificado"""
        print("\n" + "="*80)
        print("🎯 PROPOSED UNIFIED SCHEMA")
        print("="*80)
        
        schema = {
            # CORE FIELDS (Todos los TCGs)
            'card_id': 'str - Identificador único',
            'game': 'str - Juego (one_piece, yugioh, pokemon, magic)',
            'name': 'str - Nombre de la carta',
            'image_url': 'str - URL de imagen',
            'type': 'str - Tipo de carta',
            'effect': 'str - Descripción/efecto',
            'rarity': 'str - Rareza',
            'set_name': 'str - Nombre del set',
            'price_usd': 'float - Precio en USD',
            
            # EXTENDED FIELDS (Según el juego)
            'power': 'str/int - Poder/ATK (Pokémon, Magic, OneP)',
            'toughness': 'int - Resistencia/DEF (Magic, Pokémon)',
            'cost': 'int/str - Costo (maná, energía, etc)',
            'color': 'str - Color (Magic, OneP)',
            'hp': 'int - Puntos de vida (Pokémon)',
            'abilities': 'list - Habilidades/ataques',
            'weaknesses': 'list - Debilidades',
            'resistances': 'list - Resistencias',
            'archetype': 'str - Arquetipo/familia (Yu-Gi-Oh)',
            
            # METADATA
            'created_at': 'datetime - Fecha de ingreso',
            'source_file': 'str - Archivo original',
            'source_url': 'str - URL de descarga',
        }
        
        print("\nCORE FIELDS (Required for all TCGs):")
        core = ['card_id', 'game', 'name', 'image_url', 'type', 'effect', 'rarity', 'set_name', 'price_usd']
        for field in core:
            print(f"  ✓ {field:20s} - {schema[field]}")
        
        print("\nEXTENDED FIELDS (Game-specific):")
        extended = [k for k in schema.keys() if k not in core and k not in ['created_at', 'source_file', 'source_url']]
        for field in extended:
            print(f"  ◆ {field:20s} - {schema[field]}")
        
        return schema

def main():
    """Main execution"""
    analyzer = TCGAnalyzer()
    
    # Muestras de datos
    one_piece_csv = "OP01-006-1,OP01-006,UC,Land of Wano,https://en.onepiece-cardgame.com/images/cardlist/card/OP01-006_p1.png?250502,1,Otama,Red,OP01,,1,2000.0,[On Play] Give up to 1 of your opponent's Characters −2000 power during this turn.,,0"
    
    yugioh_json = {
        "data": [
            {
                "id": 34541863,
                "name": "\"A\" Cell Breeding Device",
                "type": "Spell Card",
                "humanReadableCardType": "Continuous Spell",
                "frameType": "spell",
                "desc": "During each of your Standby Phases, put 1 A-Counter on 1 face-up monster your opponent controls.",
                "race": "Continuous",
                "archetype": "Alien",
                "ygoprodeck_url": "https://ygoprodeck.com/card/a-cell-breeding-device-9766",
                "card_sets": [{"set_name": "Force of the Breaker", "set_code": "FOTB-EN043", "set_rarity": "Common"}],
                "card_images": [{"id": 34541863, "image_url": "https://images.ygoprodeck.com/images/cards/34541863.jpg"}],
                "card_prices": [{"tcgplayer_price": "0.19"}]
            }
        ]
    }
    
    pokemon_json = [
        {
            "id": "hgss4-1",
            "name": "Aggron",
            "supertype": "Pokémon",
            "subtypes": ["Stage 2"],
            "hp": "140",
            "types": ["Metal"],
            "evolvesFrom": "Lairon",
            "attacks": [
                {
                    "name": "Second Strike",
                    "cost": ["Metal", "Metal", "Colorless"],
                    "convertedEnergyCost": 3,
                    "damage": "40",
                    "text": "If the Defending Pokémon already has any damage counters on it..."
                }
            ],
            "weaknesses": [{"type": "Fire", "value": "×2"}],
            "images": {"large": "https://images.pokemontcg.io/hgss4/1_hires.png"},
            "tcgplayer": {"prices": {"holofoil": {"market": 2.33}}},
            "rarity": "Rare Holo"
        }
    ]
    
    magic_json = [
        {
            "id": "0000419b-0bba-4488-8f7a-6194544ce91e",
            "name": "Forest",
            "type_line": "Basic Land — Forest",
            "oracle_text": "({T}: Add {G}.)",
            "mana_cost": "",
            "image_uris": {
                "normal": "https://cards.scryfall.io/normal/front/0/0/0000419b-0bba-4488-8f7a-6194544ce91e.jpg"
            },
            "set_name": "Bloomburrow",
            "rarity": "common",
            "prices": {"usd": "0.22"}
        }
    ]
    
    # Analizar cada formato
    analyzer.analyze_one_piece(one_piece_csv)
    analyzer.analyze_yugioh(yugioh_json)
    analyzer.analyze_pokemon(pokemon_json)
    analyzer.analyze_magic(magic_json)
    
    # Encontrar campos comunes
    analyzer.find_common_fields()
    
    # Proponer esquema unificado
    schema = analyzer.propose_unified_schema()
    
    # Resumen
    print("\n" + "="*80)
    print("📋 SUMMARY")
    print("="*80)
    
    print("\n✅ Formatos analizados:")
    for game, data in analyzer.formats.items():
        print(f"\n  {game.upper()}:")
        print(f"    Source: {data['source']}")
        print(f"    Key fields: {', '.join(data['key_fields'][:3])}...")
    
    print("\n📊 Recomendación:")
    print("""
    Usar una combinación de:
    1. CSV/Parquet para almacenamiento eficiente
    2. SQLite para queries rápidas
    3. JSON para estructura flexible
    
    Vamos a crear un script que:
    ✓ Lee CSV de One Piece
    ✓ Lee JSON de Yu-Gi-Oh, Pokémon, Magic
    ✓ Normaliza todo al esquema unificado
    ✓ Guarda en: SQLite + CSV exportable
    """)

if __name__ == "__main__":
    main()
