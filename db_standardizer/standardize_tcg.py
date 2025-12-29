#!/usr/bin/env python3
"""
TCG Data Standardizer
Convierte CSV/JSON de todos los TCGs a un formato unificado
Crea: SQLite + CSV exportable
"""

import json
import csv
import sqlite3
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TCGStandardizer:
    """Standardiza todos los formatos de TCG a un esquema unificado"""
    
    def __init__(self, db_path: str = "tcg_unified.db"):
        self.db_path = db_path
        self.cards = []
        self.init_db()
    
    def init_db(self):
        """Crear tabla unificada en SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            DROP TABLE IF EXISTS cards
        ''')
        
        cursor.execute('''
            CREATE TABLE cards (
                card_id TEXT PRIMARY KEY,
                game TEXT NOT NULL,
                name TEXT NOT NULL,
                image_url TEXT,
                type TEXT,
                effect TEXT,
                rarity TEXT,
                set_name TEXT,
                price_usd REAL,
                
                power TEXT,
                toughness INTEGER,
                cost TEXT,
                color TEXT,
                hp INTEGER,
                abilities TEXT,
                weaknesses TEXT,
                resistances TEXT,
                archetype TEXT,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_game TEXT,
                source_file TEXT
            )
        ''')
        
        # Crear índices
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_game ON cards(game)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON cards(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_rarity ON cards(rarity)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_set ON cards(set_name)')
        
        conn.commit()
        conn.close()
        logger.info(f"✅ Database initialized: {self.db_path}")
    
    # ==================== ONE PIECE ====================
    
    def load_one_piece_csv(self, csv_file: str) -> List[Dict]:
        """Cargar y parsear CSV de One Piece"""
        logger.info(f"📥 Cargando One Piece CSV: {csv_file}")
        
        cards = []
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i == 0:  # Skip header if exists
                        if row[0] == 'id':
                            continue
                    
                    if len(row) < 10:
                        logger.warning(f"Fila incompleta: {row}")
                        continue
                    
                    card = self._parse_one_piece_row(row)
                    if card:
                        cards.append(card)
            
            logger.info(f"✅ Loaded {len(cards)} One Piece cards")
            return cards
        except Exception as e:
            logger.error(f"❌ Error loading One Piece CSV: {e}")
            return []
    
    def _parse_one_piece_row(self, row: List) -> Optional[Dict]:
        """Parsear fila CSV de One Piece"""
        try:
            # Estructura CSV correcta:
            # 0: id (OP01-024-2)
            # 1: card_id (OP01-024)
            # 2: rarity (SR, UC, R, etc)
            # 3: name/categories (Supernovas;Straw Hat Crew)
            # 4: image_url
            # 5: power (2, 3, 4, etc)
            # 6: character_name (Monkey.D.Luffy, Izo, etc)
            # 7: color (Red, Green, Blue, Black, Purple, Yellow)
            # 8: set (OP01)
            # 9: cost/don_cost (3000.0, empty, etc)
            # 10: card_level (1, 2, 3)
            # 11: price (1000.0, empty, etc)
            # 12: ability/effect (text, can be long)
            # 13: trigger_effect (text)
            # 14: unknown (0)
            
            card_id = row[1] if len(row) > 1 else row[0]
            
            # Combinar nombre y categorías
            name_parts = []
            if len(row) > 6 and row[6]:  # character_name
                name_parts.append(row[6])
            if len(row) > 3 and row[3]:  # categories
                name_parts.append(row[3])
            
            full_name = ' | '.join(name_parts) if name_parts else card_id
            
            # Combinar abilities
            abilities = []
            if len(row) > 12 and row[12]:
                abilities.append(row[12])
            if len(row) > 13 and row[13]:
                abilities.append(row[13])
            
            effect_text = ' | '.join(abilities) if abilities else ''
            
            return {
                'card_id': card_id,
                'game': 'one_piece',
                'name': full_name,
                'image_url': row[4] if len(row) > 4 else '',
                'type': 'Character',
                'effect': effect_text,
                'rarity': row[2] if len(row) > 2 else 'Unknown',
                'set_name': row[8] if len(row) > 8 else 'OP01',
                'price_usd': self._parse_price(row[11]) if len(row) > 11 and row[11] else None,
                
                # Extended fields
                'power': row[5] if len(row) > 5 and row[5] else None,
                'color': row[7] if len(row) > 7 else None,
                'cost': row[9] if len(row) > 9 and row[9] else None,
                'abilities': json.dumps(abilities) if abilities else None,
                'source_game': 'one_piece_csv'
            }
        except Exception as e:
            logger.error(f"Error parsing One Piece row: {e}")
            return None
    
    # ==================== YU-GI-OH ====================
    
    def load_yugioh_json(self, json_file: str) -> List[Dict]:
        """Cargar y parsear JSON de Yu-Gi-Oh"""
        logger.info(f"📥 Cargando Yu-Gi-Oh JSON: {json_file}")
        
        cards = []
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Puede ser {"data": [...]} o directamente [...]
            card_list = data.get('data', data) if isinstance(data, dict) else data
            
            for raw_card in card_list:
                card = self._parse_yugioh_json(raw_card)
                if card:
                    cards.append(card)
            
            logger.info(f"✅ Loaded {len(cards)} Yu-Gi-Oh cards")
            return cards
        except Exception as e:
            logger.error(f"❌ Error loading Yu-Gi-Oh JSON: {e}")
            return []
    
    def _parse_yugioh_json(self, raw_card: Dict) -> Optional[Dict]:
        """Parsear card JSON de Yu-Gi-Oh"""
        try:
            # Extraer imagen
            image_url = ''
            if raw_card.get('card_images'):
                image_url = raw_card['card_images'][0].get('image_url', '')
            
            # Extraer precio
            price_usd = None
            if raw_card.get('card_prices'):
                price_str = raw_card['card_prices'][0].get('tcgplayer_price', '0')
                price_usd = self._parse_price(price_str)
            
            # Extraer set
            set_name = ''
            if raw_card.get('card_sets'):
                set_name = raw_card['card_sets'][0].get('set_name', '')
            
            return {
                'card_id': str(raw_card.get('id', '')),
                'game': 'yugioh',
                'name': raw_card.get('name', ''),
                'image_url': image_url,
                'type': raw_card.get('type', ''),
                'effect': raw_card.get('desc', ''),
                'rarity': raw_card.get('card_sets', [{}])[0].get('set_rarity', 'Unknown') if raw_card.get('card_sets') else 'Unknown',
                'set_name': set_name,
                'price_usd': price_usd,
                
                # Extended fields
                'archetype': raw_card.get('archetype'),
                'source_game': 'yugioh_json'
            }
        except Exception as e:
            logger.error(f"Error parsing Yu-Gi-Oh card: {e}")
            return None
    
    # ==================== POKÉMON ====================
    
    def load_pokemon_json(self, json_file: str) -> List[Dict]:
        """Cargar y parsear JSON de Pokémon"""
        logger.info(f"📥 Cargando Pokémon JSON: {json_file}")
        
        cards = []
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            card_list = data.get('data', data) if isinstance(data, dict) else data
            
            for raw_card in card_list:
                card = self._parse_pokemon_json(raw_card)
                if card:
                    cards.append(card)
            
            logger.info(f"✅ Loaded {len(cards)} Pokémon cards")
            return cards
        except Exception as e:
            logger.error(f"❌ Error loading Pokémon JSON: {e}")
            return []
    
    def _parse_pokemon_json(self, raw_card: Dict) -> Optional[Dict]:
        """Parsear card JSON de Pokémon"""
        try:
            # Extraer imagen
            image_url = raw_card.get('images', {}).get('large', '')
            
            # Extraer precio
            price_usd = None
            tcgplayer = raw_card.get('tcgplayer', {})
            if tcgplayer.get('prices'):
                holofoil = tcgplayer['prices'].get('holofoil', {})
                if holofoil:
                    price_usd = self._parse_price(holofoil.get('market', '0'))
            
            # Extraer ataques
            abilities = []
            for attack in raw_card.get('attacks', []):
                abilities.append({
                    'name': attack.get('name'),
                    'damage': attack.get('damage'),
                    'cost': len(attack.get('cost', []))
                })
            
            # Extraer debilidades
            weaknesses = []
            for weak in raw_card.get('weaknesses', []):
                weaknesses.append({
                    'type': weak.get('type'),
                    'value': weak.get('value')
                })
            
            # Extraer resistencias
            resistances = []
            for resist in raw_card.get('resistances', []):
                resistances.append({
                    'type': resist.get('type'),
                    'value': resist.get('value')
                })
            
            return {
                'card_id': raw_card.get('id', ''),
                'game': 'pokemon',
                'name': raw_card.get('name', ''),
                'image_url': image_url,
                'type': raw_card.get('types', [''])[0] if raw_card.get('types') else 'Unknown',
                'effect': raw_card.get('flavorText', ''),
                'rarity': raw_card.get('rarity', 'Unknown'),
                'set_name': raw_card.get('set', {}).get('name', '') if raw_card.get('set') else '',
                'price_usd': price_usd,
                
                # Extended fields
                'hp': raw_card.get('hp'),
                'abilities': json.dumps(abilities),
                'weaknesses': json.dumps(weaknesses),
                'resistances': json.dumps(resistances),
                'source_game': 'pokemon_json'
            }
        except Exception as e:
            logger.error(f"Error parsing Pokémon card: {e}")
            return None
    
    # ==================== MAGIC ====================
    
    def load_magic_json(self, json_file: str) -> List[Dict]:
        """Cargar y parsear JSON de Magic"""
        logger.info(f"📥 Cargando Magic JSON: {json_file}")
        
        cards = []
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            card_list = data if isinstance(data, list) else [data]
            
            for raw_card in card_list:
                card = self._parse_magic_json(raw_card)
                if card:
                    cards.append(card)
            
            logger.info(f"✅ Loaded {len(cards)} Magic cards")
            return cards
        except Exception as e:
            logger.error(f"❌ Error loading Magic JSON: {e}")
            return []
    
    def _parse_magic_json(self, raw_card: Dict) -> Optional[Dict]:
        """Parsear card JSON de Magic"""
        try:
            # Extraer imagen
            image_url = raw_card.get('image_uris', {}).get('normal', '')
            
            # Extraer precio
            price_usd = None
            prices = raw_card.get('prices', {})
            if prices.get('usd'):
                price_usd = self._parse_price(prices['usd'])
            
            return {
                'card_id': raw_card.get('id', ''),
                'game': 'magic',
                'name': raw_card.get('name', ''),
                'image_url': image_url,
                'type': raw_card.get('type_line', ''),
                'effect': raw_card.get('oracle_text', ''),
                'rarity': raw_card.get('rarity', 'Unknown'),
                'set_name': raw_card.get('set_name', ''),
                'price_usd': price_usd,
                
                # Extended fields
                'power': raw_card.get('power'),
                'toughness': self._parse_int(raw_card.get('toughness')),
                'cost': raw_card.get('mana_cost'),
                'color': json.dumps(raw_card.get('color_identity', [])),
                'source_game': 'magic_json'
            }
        except Exception as e:
            logger.error(f"Error parsing Magic card: {e}")
            return None
    
    # ==================== UTILITIES ====================
    
    @staticmethod
    def _parse_price(price_str: Any) -> Optional[float]:
        """Parsear precio a float"""
        try:
            if price_str is None or price_str == '':
                return None
            return float(str(price_str).replace('$', '').strip())
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _parse_int(value: Any) -> Optional[int]:
        """Parsear entero"""
        try:
            if value is None:
                return None
            return int(value)
        except (ValueError, TypeError):
            return None
    
    def save_to_database(self, cards: List[Dict]):
        """Guardar cartas en SQLite"""
        logger.info(f"💾 Guardando {len(cards)} cartas en base de datos...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for card in cards:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO cards (
                        card_id, game, name, image_url, type, effect, rarity, 
                        set_name, price_usd, power, toughness, cost, color, hp, 
                        abilities, weaknesses, resistances, archetype, source_game
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    card.get('card_id'),
                    card.get('game'),
                    card.get('name'),
                    card.get('image_url'),
                    card.get('type'),
                    card.get('effect'),
                    card.get('rarity'),
                    card.get('set_name'),
                    card.get('price_usd'),
                    card.get('power'),
                    card.get('toughness'),
                    card.get('cost'),
                    card.get('color'),
                    card.get('hp'),
                    card.get('abilities'),
                    card.get('weaknesses'),
                    card.get('resistances'),
                    card.get('archetype'),
                    card.get('source_game')
                ))
            except Exception as e:
                logger.error(f"Error saving card {card.get('card_id')}: {e}")
        
        conn.commit()
        conn.close()
        logger.info("✅ Cards saved to database")
    
    def export_to_csv(self, csv_file: str = "tcg_unified.csv"):
        """Exportar base de datos a CSV"""
        logger.info(f"📤 Exportando a CSV: {csv_file}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM cards ORDER BY game, name')
        rows = cursor.fetchall()
        
        cursor.execute("PRAGMA table_info(cards)")
        columns = [col[1] for col in cursor.fetchall()]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)
        
        conn.close()
        logger.info(f"✅ Exported {len(rows)} cards to {csv_file}")
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas de la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM cards')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT game, COUNT(*) FROM cards GROUP BY game')
        by_game = dict(cursor.fetchall())
        
        cursor.execute('SELECT rarity, COUNT(*) FROM cards GROUP BY rarity')
        by_rarity = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            'total_cards': total,
            'by_game': by_game,
            'by_rarity': by_rarity
        }


def main():
    """Main execution"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           TCG DATA STANDARDIZER v1.0                      ║
║                                                           ║
║  Converts CSV/JSON from multiple TCGs to unified format  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    standardizer = TCGStandardizer()
    all_cards = []
    
    # Cargar datos (ajustar rutas según tus archivos)
    print("\n📂 Cargando archivos...\n")
    
    # One Piece CSV
    if Path("one_piece.csv").exists():
        one_piece_cards = standardizer.load_one_piece_csv("one_piece.csv")
        all_cards.extend(one_piece_cards)
    
    # Yu-Gi-Oh JSON
    if Path("yugioh.json").exists():
        yugioh_cards = standardizer.load_yugioh_json("yugioh.json")
        all_cards.extend(yugioh_cards)
    
    # Pokémon JSON
    if Path("pokemon.json").exists():
        pokemon_cards = standardizer.load_pokemon_json("pokemon.json")
        all_cards.extend(pokemon_cards)
    
    # Magic JSON
    if Path("magic.json").exists():
        magic_cards = standardizer.load_magic_json("magic.json")
        all_cards.extend(magic_cards)
    
    # Guardar en base de datos
    print("\n💾 Guardando en base de datos...\n")
    standardizer.save_to_database(all_cards)
    
    # Exportar a CSV
    standardizer.export_to_csv()
    
    # Estadísticas
    stats = standardizer.get_stats()
    
    print("\n" + "="*80)
    print("📊 ESTADÍSTICAS FINALES")
    print("="*80)
    print(f"\nTotal de cartas: {stats['total_cards']}")
    print("\nPor juego:")
    for game, count in stats['by_game'].items():
        print(f"  • {game:20s} - {count:5d} cartas")
    
    print("\n✅ ¡Standardización completada!")
    print(f"   📦 Base de datos: tcg_unified.db")
    print(f"   📄 CSV exportado: tcg_unified.csv")


if __name__ == "__main__":
    main()