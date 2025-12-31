import React, { useState, useEffect } from 'react';

function TCGSearch() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedGame, setSelectedGame] = useState('');
  const [games, setGames] = useState([]);
  const [suggestions, setSuggestions] = useState([]);
  const [selectedCard, setSelectedCard] = useState(null);
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const getApiUrl = () => {
    const hostname = window.location.hostname;
    const pathname = window.location.pathname;

    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
      if (pathname.startsWith('/tcg')) {
        return '/tcg/api';
      }
    }
    return '/api';
  };

  const API_URL = getApiUrl();

  useEffect(() => {
    fetchGames();
  }, []);

  const fetchGames = async () => {
    try {
      const response = await fetch(`${API_URL}/games`);
      const data = await response.json();
      setGames(data.games || []);
    } catch (e) {
      console.error('❌ Error fetching games:', e);
    }
  };

  const handleSearchChange = async (value) => {
    setSearchQuery(value);
    if (value.length < 1) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    try {
      const params = new URLSearchParams();
      params.append('q', value);
      params.append('limit', '10');
      if (selectedGame) params.append('game', selectedGame);

      const response = await fetch(`${API_URL}/autocomplete?${params}`);
      const data = await response.json();
      setSuggestions(data.suggestions || []);
      setShowSuggestions(true);
    } catch (e) {
      console.error('❌ Autocomplete error:', e);
    }
  };

  const handleSearch = async (query = searchQuery) => {
    if (!query.trim()) return;
    setLoading(true);
    setHasSearched(true);
    setSelectedCard(null);
    setShowSuggestions(false);

    try {
      const params = new URLSearchParams();
      params.append('q', query);
      params.append('limit', '50');
      if (selectedGame) params.append('game', selectedGame);

      const response = await fetch(`${API_URL}/search?${params}`);
      const data = await response.json();
      
      const results = data.cards || [];
      setSearchResults(results);
      setShowSuggestions(false);
      
      if (results.length > 0) {
        setSelectedCard(results[0]);
      }
    } catch (e) {
      console.error('❌ Search error:', e);
    } finally {
      setLoading(false);
    }
  };

  const gameColors = {
    one_piece: '#FF6B6B',
    pokemon: '#FFD700',
    yugioh: '#4169E1',
    magic: '#A020F0'
  };

  const gameIcons = {
    one_piece: '🏴‍☠️',
    pokemon: '⚡',
    yugioh: '🎴',
    magic: '✨'
  };

  return (
    <div className="tcg-wrapper">
      <div className="tcg-container">
        <div className="tcg-header">
          <h1>Trading Card Database</h1>
          <p>Premium Collectible Card Search - One Piece, Pokémon, Yu-Gi-Oh & Magic</p>
        </div>

        <div className="tcg-search-box">
          <div className="tcg-search-controls">
            <div className="tcg-search-input-wrapper">
              <input
                type="text"
                className="tcg-search-input"
                placeholder="Search for a card..."
                value={searchQuery}
                onChange={(e) => handleSearchChange(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              />
              {showSuggestions && suggestions.length > 0 && (
                <div className="tcg-suggestions">
                  {suggestions.map((s, i) => (
                    <div
                      key={i}
                      className="tcg-suggestion-item"
                      onClick={() => {
                        setSearchQuery(s);
                        setShowSuggestions(false);
                        setTimeout(() => handleSearch(s), 0);
                      }}
                    >
                      {s}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <select
              className="tcg-game-select"
              value={selectedGame}
              onChange={(e) => {
                setSelectedGame(e.target.value);
                if (searchQuery) handleSearch();
              }}
            >
              <option value="">All Games ({games.length})</option>
              {games.map((g) => (
                <option key={g} value={g}>
                  {gameIcons[g] || '🎮'} {g.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>

            <button
              className="tcg-btn-search"
              onClick={() => handleSearch()}
              disabled={!searchQuery.trim() || loading}
            >
              {loading ? '🔍 SEARCHING...' : 'SEARCH'}
            </button>
          </div>
        </div>

        <div className="tcg-content">
          <div className="tcg-main-content">
            {!hasSearched ? (
              <div className="tcg-card-main tcg-empty">
                <p>👀 Search for a card to see it here</p>
              </div>
            ) : searchResults.length === 0 ? (
              <div className="tcg-card-main tcg-empty">
                <p>📭 No cards found. Try a different search!</p>
              </div>
            ) : selectedCard ? (
              <div className="tcg-card-main">
                <div className="tcg-card-image">
                  <img
                    src={selectedCard.image_url}
                    alt={selectedCard.name}
                    onError={(e) =>
                      (e.target.src =
                        'https://via.placeholder.com/300x400?text=' +
                        encodeURIComponent(selectedCard.name))
                    }
                  />
                </div>
                <div className="tcg-card-details">
                  <h2 className="tcg-card-name">{selectedCard.name}</h2>
                  <div
                    className="tcg-card-badge"
                    style={{ backgroundColor: gameColors[selectedCard.game] || '#999' }}
                  >
                    {gameIcons[selectedCard.game] || '🎮'} {selectedCard.game}
                  </div>

                  {selectedCard.type && (
                    <div className="tcg-detail-row">
                      <span className="tcg-detail-label">Type</span>
                      <span className="tcg-detail-value">{selectedCard.type}</span>
                    </div>
                  )}

                  {selectedCard.rarity && (
                    <div className="tcg-detail-row">
                      <span className="tcg-detail-label">Rarity</span>
                      <span className="tcg-detail-value">{selectedCard.rarity}</span>
                    </div>
                  )}

                  {selectedCard.hp && (
                    <div className="tcg-detail-row">
                      <span className="tcg-detail-label">HP</span>
                      <span className="tcg-detail-value">{selectedCard.hp}</span>
                    </div>
                  )}

                  {selectedCard.price_usd && (
                    <div className="tcg-detail-row">
                      <span className="tcg-detail-label">Price</span>
                      <span className="tcg-detail-value">
                        ${selectedCard.price_usd.toFixed(2)}
                      </span>
                    </div>
                  )}

                  {selectedCard.effect && (
                    <div className="tcg-effect">
                      <div className="tcg-effect-title">✨ EFFECT / DESCRIPTION</div>
                      <div className="tcg-effect-text">{selectedCard.effect}</div>
                    </div>
                  )}
                </div>
              </div>
            ) : null}
          </div>

          {searchResults.length > 0 && (
            <div className="tcg-results">
              <div className="tcg-results-title">📊 RESULTS ({searchResults.length})</div>
              <div className="tcg-results-list">
                {searchResults.slice(0, 30).map((card) => (
                  <div
                    key={card.card_id}
                    className={`tcg-result-item ${selectedCard?.card_id === card.card_id ? 'tcg-result-item-active' : ''}`}
                    onClick={() => setSelectedCard(card)}
                  >
                    <img
                      src={card.image_url}
                      alt=""
                      className="tcg-result-image"
                      onError={(e) =>
                        (e.target.src =
                          'https://via.placeholder.com/55x75?text=' +
                          encodeURIComponent(card.name))
                      }
                    />
                    <div className="tcg-result-info">
                      <div className="tcg-result-name">{card.name}</div>
                      <div className="tcg-result-meta">
                        {gameIcons[card.game] || '🎮'} {card.rarity}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default TCGSearch;
