import React, { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useTelegram } from './hooks/useTelegram';
import HomePage from './pages/HomePage';
import AttractionDetailPage from './pages/AttractionDetailPage';
import FavoritesPage from './pages/FavoritesPage';
import TestPage from './pages/TestPage';
import './App.css';

function App() {
  const { tg, themeParams } = useTelegram();

  useEffect(() => {
    if (themeParams) {
      document.documentElement.style.setProperty(
        '--tg-theme-bg-color',
        themeParams.bg_color || '#ffffff'
      );
      document.documentElement.style.setProperty(
        '--tg-theme-text-color',
        themeParams.text_color || '#000000'
      );
      document.documentElement.style.setProperty(
        '--tg-theme-hint-color',
        themeParams.hint_color || '#999999'
      );
      document.documentElement.style.setProperty(
        '--tg-theme-link-color',
        themeParams.link_color || '#3390ec'
      );
      document.documentElement.style.setProperty(
        '--tg-theme-button-color',
        themeParams.button_color || '#3390ec'
      );
      document.documentElement.style.setProperty(
        '--tg-theme-button-text-color',
        themeParams.button_text_color || '#ffffff'
      );
      document.documentElement.style.setProperty(
        '--tg-theme-secondary-bg-color',
        themeParams.secondary_bg_color || '#f5f5f5'
      );
    }

    if (tg) {
      document.body.style.backgroundColor = themeParams?.bg_color || '#ffffff';
    }
  }, [tg, themeParams]);

  return (
    <BrowserRouter>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/attractions/:id" element={<AttractionDetailPage />} />
          <Route path="/favorites" element={<FavoritesPage />} />
          <Route path="/test" element={<TestPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
