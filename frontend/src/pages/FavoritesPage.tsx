import React, { useEffect, useState } from 'react';
import Header from '../components/Layout/Header';
import Navigation from '../components/Layout/Navigation';
import AttractionList from '../components/Attraction/AttractionList';
import Loading from '../components/Loading';
import { getFavorites } from '../services/api';
import { Favorite, Attraction } from '../types';
import './FavoritesPage.css';

const FavoritesPage: React.FC = () => {
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(true);

  const loadFavorites = async () => {
    setLoading(true);
    try {
      const response = await getFavorites();
      setFavorites(response.data.items);
    } catch (error) {
      console.error('Error loading favorites:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFavorites();
  }, []);

  const handleFavoriteToggle = () => {
    loadFavorites();
  };

  if (loading) {
    return <Loading />;
  }

  const attractions: Attraction[] = favorites.map((fav) => ({
    ...fav.attraction,
    is_favorite: true,
  }));

  return (
    <div className="favorites-page">
      <Header title="Избранное" />

      {attractions.length === 0 ? (
        <div className="empty-favorites">
          <span className="empty-icon">❤️</span>
          <h3>Избранное пусто</h3>
          <p>
            Добавляйте достопримечательности в избранное, чтобы быстро находить
            их здесь
          </p>
        </div>
      ) : (
        <>
          <div className="favorites-count">
            Сохранено: {attractions.length}
          </div>
          <AttractionList
            attractions={attractions}
            onFavoriteToggle={handleFavoriteToggle}
          />
        </>
      )}

      <Navigation />
    </div>
  );
};

export default FavoritesPage;
