#!/usr/bin/env python3
"""
Trading Card Game API
Búsqueda y filtrado de cartas de One Piece, Yu-Gi-Oh, Pokémon y Magic
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3
import json
from pathlib import Path

app = FastAPI(
    title="Trading Card API",
    description="API para buscar cartas de TCG",
    version="1.0.0"
)

# CORS para que el frontend pueda llamar desde cualquier lado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta de la base de datos
DB_PATH = Path("tcg_unified.db")

# ==================== MODELS ====================

class Card(BaseModel):
    card_id: str
    name: str
    game: str
    type: str
    rarity: str
    image_url: str
    effect: Optional[str]
    price_usd: Optional[float]
    power: Optional[str]
    hp: Optional[int]
    toughness: Optional[int]
    cost: Optional[str]
    color: Optional[str]
    abilities: Optional[str]
    archetype: Optional[str]

class SearchResult(BaseModel):
    total: int
    cards: List[Card]

class GameStats(BaseModel):
    game: str
    count: int

# ==================== DATABASE HELPERS ====================

def get_db_connection():
    """Conectar a base de datos"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def row_to_card(row) -> Card:
    """Convertir fila de SQLite a objeto Card"""
    return Card(
        card_id=row['card_id'],
        name=row['name'],
        game=row['game'],
        type=row['type'] or '',
        rarity=row['rarity'] or 'Unknown',
        image_url=row['image_url'] or '',
        effect=row['effect'],
        price_usd=row['price_usd'],
        power=row['power'],
        hp=row['hp'],
        toughness=row['toughness'],
        cost=row['cost'],
        color=row['color'],
        abilities=row['abilities'],
        archetype=row['archetype']
    )

# ==================== ENDPOINTS ====================

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

@app.get("/api/games")
async def get_games():
    """Obtener lista de juegos disponibles"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT DISTINCT game FROM cards ORDER BY game
    ''')
    
    games = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return {
        "games": games,
        "total": len(games)
    }

@app.get("/api/stats")
async def get_stats():
    """Obtener estadísticas de cartas por juego"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT game, COUNT(*) as count 
        FROM cards 
        GROUP BY game 
        ORDER BY count DESC
    ''')
    
    stats = [
        GameStats(game=row['game'], count=row['count'])
        for row in cursor.fetchall()
    ]
    
    cursor.execute('SELECT COUNT(*) FROM cards')
    total = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total_cards": total,
        "by_game": [s.dict() for s in stats]
    }

@app.get("/api/search")
async def search_cards(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    game: Optional[str] = Query(None, description="Filtrar por juego"),
    rarity: Optional[str] = Query(None, description="Filtrar por rareza"),
    limit: int = Query(20, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación")
):
    """
    Buscar cartas por nombre
    
    Ejemplos:
    - /api/search?q=dragon
    - /api/search?q=pikachu&game=pokemon
    - /api/search?q=rare&game=magic&rarity=rare
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM cards WHERE name LIKE ?"
    params = [f"%{q}%"]
    
    if game:
        query += " AND game = ?"
        params.append(game)
    
    if rarity:
        query += " AND rarity = ?"
        params.append(rarity)
    
    # Contar total
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Obtener resultados
    query += " ORDER BY name LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    cards = [row_to_card(row) for row in rows]
    conn.close()
    
    return SearchResult(total=total, cards=cards)

@app.get("/api/autocomplete")
async def autocomplete(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    game: Optional[str] = Query(None, description="Filtrar por juego"),
    limit: int = Query(10, ge=1, le=50, description="Máximo de sugerencias")
):
    """
    Autocompletar nombres de cartas
    
    Retorna solo nombres para el autocomplete en el frontend
    
    Ejemplos:
    - /api/autocomplete?q=dra&limit=5
    - /api/autocomplete?q=pik&game=pokemon&limit=10
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT DISTINCT name FROM cards WHERE name LIKE ?"
    params = [f"%{q}%"]
    
    if game:
        query += " AND game = ?"
        params.append(game)
    
    query += " ORDER BY name LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    suggestions = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return {
        "query": q,
        "suggestions": suggestions,
        "count": len(suggestions)
    }

@app.get("/api/cards/{card_id}", response_model=Card)
async def get_card(card_id: str):
    """
    Obtener carta por ID
    
    Ejemplo:
    - /api/cards/OP01-024
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cards WHERE card_id = ?", (card_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Card not found")
    
    return row_to_card(row)

@app.get("/api/cards/by-name/{name}", response_model=List[Card])
async def get_cards_by_name(
    name: str,
    game: Optional[str] = Query(None, description="Filtrar por juego"),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Obtener cartas por nombre exacto
    
    Ejemplo:
    - /api/cards/by-name/Dragon?game=pokemon
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM cards WHERE name LIKE ?"
    params = [f"%{name}%"]
    
    if game:
        query += " AND game = ?"
        params.append(game)
    
    query += " LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="No cards found")
    
    return [row_to_card(row) for row in rows]

@app.get("/api/rarities")
async def get_rarities(game: Optional[str] = Query(None)):
    """
    Obtener lista de rarezas disponibles
    
    Ejemplos:
    - /api/rarities
    - /api/rarities?game=pokemon
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT DISTINCT rarity FROM cards WHERE rarity IS NOT NULL AND rarity != ''"
    params = []
    
    if game:
        query += " AND game = ?"
        params.append(game)
    
    query += " ORDER BY rarity"
    
    cursor.execute(query, params)
    rarities = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return {
        "rarities": rarities,
        "count": len(rarities)
    }

@app.get("/api/filter")
async def filter_cards(
    game: Optional[str] = Query(None),
    rarity: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Filtrar cartas por criterios múltiples
    
    Ejemplos:
    - /api/filter?game=pokemon&rarity=Rare
    - /api/filter?min_price=100&max_price=500
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM cards WHERE 1=1"
    params = []
    
    if game:
        query += " AND game = ?"
        params.append(game)
    
    if rarity:
        query += " AND rarity = ?"
        params.append(rarity)
    
    if min_price is not None:
        query += " AND price_usd >= ?"
        params.append(min_price)
    
    if max_price is not None:
        query += " AND price_usd <= ?"
        params.append(max_price)
    
    # Contar
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total = cursor.fetchone()[0]
    
    # Obtener resultados
    query += " ORDER BY name LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    cards = [row_to_card(row) for row in rows]
    conn.close()
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "cards": [c.dict() for c in cards]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005, reload=True)
