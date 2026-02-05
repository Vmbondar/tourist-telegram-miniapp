import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import Header from '../components/Layout/Header';
import Navigation from '../components/Layout/Navigation';
import Loading from '../components/Loading';
import { getAttraction, addToFavorites, removeFromFavorites } from '../services/api';
import { Attraction } from '../types';
import './AttractionDetailPage.css';

const AttractionDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [attraction, setAttraction] = useState<Attraction | null>(null);
  const [loading, setLoading] = useState(true);
  const [favoriteLoading, setFavoriteLoading] = useState(false);

  useEffect(() => {
    const loadAttraction = async () => {
      if (!id) return;

      setLoading(true);
      try {
        const response = await getAttraction(parseInt(id));
        setAttraction(response.data);
      } catch (error) {
        console.error('Error loading attraction:', error);
      } finally {
        setLoading(false);
      }
    };

    loadAttraction();
  }, [id]);

  const handleFavoriteToggle = async () => {
    if (!attraction) return;

    setFavoriteLoading(true);
    try {
      if (attraction.is_favorite) {
        await removeFromFavorites(attraction.id);
      } else {
        await addToFavorites(attraction.id);
      }

      setAttraction({
        ...attraction,
        is_favorite: !attraction.is_favorite,
      });
    } catch (error) {
      console.error('Error toggling favorite:', error);
    } finally {
      setFavoriteLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
  }

  if (!attraction) {
    return (
      <div className="attraction-detail-page">
        <Header title="Ошибка" showBackButton />
        <div className="error-message">
          Достопримечательность не найдена
        </div>
        <Navigation />
      </div>
    );
  }

  const placeholderImage = 'https://via.placeholder.com/800x400?text=No+Image';

  return (
    <div className="attraction-detail-page">
      <Header title={attraction.name} showBackButton />

      <div className="detail-content">
        <div className="detail-image-container">
          <img
            src={attraction.photo_url || placeholderImage}
            alt={attraction.name}
            className="detail-image"
            onError={(e) => {
              (e.target as HTMLImageElement).src = placeholderImage;
            }}
          />
          <button
            className={`detail-favorite-button ${
              attraction.is_favorite ? 'active' : ''
            }`}
            onClick={handleFavoriteToggle}
            disabled={favoriteLoading}
          >
            {attraction.is_favorite ? '❤️ В избранном' : '🤍 Добавить в избранное'}
          </button>
        </div>

        <div className="detail-info">
          <div className="detail-header">
            <h1 className="detail-title">{attraction.name}</h1>
            {attraction.category && (
              <span className="detail-category">{attraction.category}</span>
            )}
          </div>

          <div className="detail-rating">
            ⭐ {attraction.rating.toFixed(1)} / 5.0
          </div>

          {attraction.address && (
            <div className="detail-address">
              <span className="address-icon">📍</span>
              {attraction.address}
            </div>
          )}

          {attraction.description && (
            <div className="detail-description">
              <h3>Описание</h3>
              <p>{attraction.description}</p>
            </div>
          )}
        </div>
      </div>

      <Navigation />
    </div>
  );
};

export default AttractionDetailPage;
