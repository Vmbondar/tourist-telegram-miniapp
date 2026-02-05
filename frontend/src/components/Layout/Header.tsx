import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Header.css';

interface HeaderProps {
  title: string;
  showBackButton?: boolean;
}

const Header: React.FC<HeaderProps> = ({ title, showBackButton = false }) => {
  const navigate = useNavigate();

  return (
    <header className="header">
      <div className="header-content">
        {showBackButton && (
          <button className="back-button" onClick={() => navigate(-1)}>
            ← Назад
          </button>
        )}
        <h1 className="header-title">{title}</h1>
      </div>
    </header>
  );
};

export default Header;
