import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Navigation.css';

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="navigation">
      <button
        className={`nav-button ${isActive('/') ? 'active' : ''}`}
        onClick={() => navigate('/')}
      >
        <span className="nav-icon">🏛️</span>
        <span className="nav-label">Главная</span>
      </button>
      <button
        className={`nav-button ${isActive('/favorites') ? 'active' : ''}`}
        onClick={() => navigate('/favorites')}
      >
        <span className="nav-icon">❤️</span>
        <span className="nav-label">Избранное</span>
      </button>
    </nav>
  );
};

export default Navigation;
