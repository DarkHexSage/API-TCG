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

  // ⭐ Use environment variable with fallback
  const API_URL = process.env.REACT_APP_API_URL || '/api';

  useEffect(() => {
    console.log('API URL:', API_URL);
    fetchGames();
  }, []);

  const fetchGames = async () => {
    try {
      const res = await fetch(`${API_URL}/games`);
      const data = await res.json();
      setGames(data.games);
    } catch (e) {
      console.error('Error fetching games:', e);
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
      const url = new URL(`${API_URL}/autocomplete`, window.location.origin);
      url.searchParams.append('q', value);
      url.searchParams.append('limit', '8');
      if (selectedGame) url.searchParams.append('game', selectedGame);

      const res = await fetch(url);
      const data = await res.json();
      setSuggestions(data.suggestions);
      setShowSuggestions(true);
    } catch (e) {
      console.error('Error fetching suggestions:', e);
    }
  };

  const handleSearch = async (query = searchQuery) => {
    if (!query) return;
    setLoading(true);

    try {
      const url = new URL(`${API_URL}/search`, window.location.origin);
      url.searchParams.append('q', query);
      url.searchParams.append('limit', '50');
      if (selectedGame) url.searchParams.append('game', selectedGame);

      const res = await fetch(url);
      const data = await res.json();
      setSearchResults(data.cards);
      setShowSuggestions(false);
      if (data.cards.length > 0) setSelectedCard(data.cards[0]);
    } catch (e) {
      console.error('Error searching:', e);
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
    <div className="tcg-container">
      <div className="tcg-header">
        <h1>Trading Card Database</h1>
        <p>Premium Collectible Card Search - One Piece, Pokémon, Yu-Gi-Oh & Magic</p>
      </div>

      <div className="tcg-search-box">
        <div className="tcg-search-controls">
          <div style={{ flex: 1, minWidth: '200px', position: 'relative' }}>
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
                  <div key={i} className="tcg-suggestion-item" onClick={() => {
                    setSearchQuery(s);
                    setShowSuggestions(false);
                    setTimeout(() => handleSearch(s), 0);
                  }}>
                    {s}
                  </div>
                ))}
              </div>
            )}
          </div>

          <select className="tcg-game-select" value={selectedGame} onChange={(e) => {
            setSelectedGame(e.target.value);
            if (searchQuery) handleSearch();
          }}>
            <option value="">All Games</option>
            {games.map(g => (
              <option key={g} value={g}>
                {gameIcons[g] || '🎮'} {g.replace('_', ' ').toUpperCase()}
              </option>
            ))}
          </select>

          <button className="tcg-btn-search" onClick={() => handleSearch()} disabled={!searchQuery || loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </div>
      </div>

      <div className="tcg-content">
        <div>
          {selectedCard ? (
            <div className="tcg-card-main">
              <div className="tcg-card-image">
                <img src={selectedCard.image_url} alt={selectedCard.name} />
              </div>
              <div className="tcg-card-details">
                <h2 className="tcg-card-name">{selectedCard.name}</h2>
                <div className="tcg-card-badge" style={{ backgroundColor: gameColors[selectedCard.game] }}>
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
                    <span className="tcg-detail-value" style={{ fontSize: '16px' }}>
                      ${selectedCard.price_usd.toFixed(2)}
                    </span>
                  </div>
                )}

                {selectedCard.effect && (
                  <div className="tcg-effect">
                    <div className="tcg-effect-title">Effect / Description</div>
                    <div className="tcg-effect-text">{selectedCard.effect.substring(0, 250)}...</div>
                  </div>
                )}
              </div>
            </div>
          ) : (
            <div className="tcg-card-main tcg-empty">
              <p>👀 Search for a card to see it here</p>
            </div>
          )}
        </div>

        {searchResults.length > 0 && (
          <div className="tcg-results">
            <div className="tcg-results-title">Results ({searchResults.length})</div>
            {searchResults.slice(0, 15).map(card => (
              <div key={card.card_id} className="tcg-result-item" onClick={() => setSelectedCard(card)}>
                <img src={card.image_url} alt="" className="tcg-result-image" />
                <div className="tcg-result-info">
                  <div className="tcg-result-name">{card.name}</div>
                  <div className="tcg-result-meta">
                    {gameIcons[card.game] || '🎮'} {card.rarity}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default TCGSearch;
