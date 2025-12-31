cd ~/API\ TCG/TCG-API/tcg-frontend

# Remove everything
rm -rf src public node_modules build

# Create directories
mkdir -p src public

# Create public/index.html
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="theme-color" content="#000000" />
  <meta name="description" content="Trading Card Database" />
  <title>Trading Card Database</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
</head>
<body>
  <noscript>You need to enable JavaScript to run this app.</noscript>
  <div id="root"></div>
</body>
</html>
EOF

echo "✅ public/index.html created"

# Create src/index.js
cat > src/index.js << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOF

echo "✅ src/index.js created"

# Create src/index.css
cat > src/index.css << 'EOF'
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', 'Roboto', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  background-attachment: fixed;
  min-height: 100vh;
  color: #ffffff;
}

#root {
  min-height: 100vh;
}

.tcg-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.tcg-header {
  text-align: center;
  margin-bottom: 50px;
  padding: 50px 20px;
  border-bottom: 2px solid rgba(251, 191, 36, 0.3);
}

.tcg-header h1 {
  font-size: 48px;
  color: #fbbf24;
  margin-bottom: 12px;
  font-weight: 700;
}

.tcg-header p {
  font-size: 15px;
  color: rgba(255, 255, 255, 0.85);
}

.tcg-search-box {
  background: rgba(30, 41, 59, 0.25);
  border: 1px solid rgba(251, 191, 36, 0.2);
  padding: 35px;
  border-radius: 16px;
  margin-bottom: 35px;
  backdrop-filter: blur(20px);
}

.tcg-search-controls {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.tcg-search-input {
  flex: 1;
  min-width: 200px;
  padding: 14px 18px;
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 10px;
  background: rgba(51, 65, 85, 0.4);
  color: #ffffff;
  font-family: inherit;
  font-size: 14px;
}

.tcg-search-input:focus {
  outline: none;
  border-color: #fbbf24;
  box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.15);
}

.tcg-game-select {
  padding: 14px 18px;
  border: 1px solid rgba(251, 191, 36, 0.3);
  border-radius: 10px;
  background: rgba(51, 65, 85, 0.4);
  color: #ffffff;
  font-family: inherit;
  font-size: 14px;
  min-width: 160px;
  cursor: pointer;
}

.tcg-game-select option {
  background: #1a1a2e;
  color: #ffffff;
}

.tcg-btn-search {
  padding: 14px 32px;
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  color: #1a1a2e;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
}

.tcg-btn-search:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(251, 191, 36, 0.3);
}

.tcg-btn-search:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.tcg-suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(30, 41, 59, 0.95);
  border: 1px solid rgba(251, 191, 36, 0.3);
  max-height: 250px;
  overflow-y: auto;
  z-index: 100;
}

.tcg-suggestion-item {
  padding: 12px 18px;
  cursor: pointer;
  border-bottom: 1px solid rgba(251, 191, 36, 0.1);
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.tcg-suggestion-item:hover {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.tcg-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 25px;
}

.tcg-card-main {
  background: rgba(30, 41, 59, 0.25);
  border: 1px solid rgba(251, 191, 36, 0.2);
  border-radius: 16px;
  padding: 45px;
  display: flex;
  gap: 45px;
  backdrop-filter: blur(20px);
}

.tcg-card-image {
  flex: 0 0 280px;
}

.tcg-card-image img {
  width: 100%;
  height: auto;
  border-radius: 12px;
  border: 1px solid rgba(251, 191, 36, 0.3);
}

.tcg-card-details {
  flex: 1;
}

.tcg-card-name {
  font-size: 36px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 16px;
}

.tcg-card-badge {
  display: inline-block;
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 24px;
}

.tcg-detail-row {
  display: flex;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid rgba(251, 191, 36, 0.1);
  font-size: 14px;
}

.tcg-detail-label {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
}

.tcg-detail-value {
  color: #fbbf24;
  font-weight: 500;
}

.tcg-results {
  background: rgba(30, 41, 59, 0.25);
  border: 1px solid rgba(251, 191, 36, 0.2);
  border-radius: 16px;
  padding: 24px;
  max-height: 600px;
  overflow-y: auto;
  backdrop-filter: blur(20px);
}

.tcg-results-title {
  font-size: 16px;
  font-weight: 700;
  color: #fbbf24;
  margin-bottom: 18px;
}

.tcg-result-item {
  display: flex;
  gap: 14px;
  padding: 12px;
  border-radius: 10px;
  cursor: pointer;
  border: 1px solid rgba(251, 191, 36, 0.1);
  margin-bottom: 8px;
}

.tcg-result-item:hover {
  background: rgba(251, 191, 36, 0.1);
}

.tcg-result-image {
  width: 50px;
  height: 70px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid rgba(251, 191, 36, 0.2);
}

.tcg-result-info {
  flex: 1;
}

.tcg-result-name {
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tcg-result-meta {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 3px;
}

.tcg-empty {
  text-align: center;
  padding: 80px 40px;
  color: rgba(251, 191, 36, 0.6);
}

.tcg-empty p {
  font-size: 18px;
  font-weight: 500;
}

@media (max-width: 768px) {
  .tcg-content {
    grid-template-columns: 1fr;
  }

  .tcg-card-main {
    flex-direction: column;
    gap: 25px;
  }

  .tcg-card-image {
    flex: 0 0 auto;
    max-width: 200px;
  }

  .tcg-header h1 {
    font-size: 32px;
  }

  .tcg-search-controls {
    flex-direction: column;
  }

  .tcg-search-input, .tcg-game-select {
    width: 100%;
  }
}
EOF

echo "✅ src/index.css created"

# Create src/App.js (minimal version)
cat > src/App.js << 'EOF'
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

  const API_URL = process.env.REACT_APP_API_URL || '/api';

  useEffect(() => {
    fetchGames();
  }, []);

  const fetchGames = async () => {
    try {
      const res = await fetch(`${API_URL}/games`);
      const data = await res.json();
      setGames(data.games);
    } catch (e) {
      console.error('Error:', e);
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
      console.error('Error:', e);
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
      console.error('Error:', e);
    } finally {
      setLoading(false);
    }
  };

  const gameIcons = {
    one_piece: '🏴‍☠️',
    pokemon: '⚡',
    yugioh: '🎴',
    magic: '✨'
  };

  const gameColors = {
    one_piece: '#FF6B6B',
    pokemon: '#FFD700',
    yugioh: '#4169E1',
    magic: '#A020F0'
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
                    <span className="tcg-detail-value">${selectedCard.price_usd.toFixed(2)}</span>
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
                  <div className="tcg-result-meta">{gameIcons[card.game] || '🎮'} {card.rarity}</div>
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
EOF

echo "✅ src/App.js created"

# Test locally
npm install
npm run build

echo "✅ All files created and build tested!"
