import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Attraction } from '../../types';
import { addToFavorites, removeFromFavorites } from '../../services/api';
import './AttractionCard.css';

interface AttractionCardProps {
  attraction: Attraction;
  onFavoriteToggle?: () => void;
}

const AttractionCard: React.FC<AttractionCardProps> = ({
  attraction,
  onFavoriteToggle,
}) => {
  const navigate = useNavigate();
  const [isFavorite, setIsFavorite] = React.useState(
    attraction.is_favorite || false
  );
  const [loading, setLoading] = React.useState(false);

  const handleCardClick = () => {
    navigate(`/attractions/${attraction.id}`);
  };

  const handleFavoriteClick = async (e: React.MouseEvent) => {
    e.stopPropagation();
    setLoading(true);

    try {
      if (isFavorite) {
        await removeFromFavorites(attraction.id);
      } else {
        await addToFavorites(attraction.id);
      }
      setIsFavorite(!isFavorite);
      if (onFavoriteToggle) {
        onFavoriteToggle();
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
    } finally {
      setLoading(false);
    }
  };

  const placeholderImage =
    'https://via.placeholder.com/300x200?text=No+Image';

  return (
    <div className="attraction-card" onClick={handleCardClick}>
      <div className="attraction-image-container">
        <img
          src={attraction.photo_url || placeholderImage}
          alt={attraction.name}
          className="attraction-image"
          onError={(e) => {
            (e.target as HTMLImageElement).src = placeholderImage;
          }}
        />
        <button
          className={`favorite-button ${isFavorite ? 'active' : ''}`}
          onClick={handleFavoriteClick}
          disabled={loading}
        >
          {isFavorite ? '❤️' : '🤍'}
        </button>
      </div>
      <div className="attraction-info">
        <h3 className="attraction-name">{attraction.name}</h3>
        {attraction.category && (
          <span className="attraction-category">{attraction.category}</span>
        )}
        <div className="attraction-rating">
          ⭐ {attraction.rating.toFixed(1)}
        </div>
        {attraction.address && (
          <p className="attraction-address">📍 {attraction.address}</p>
        )}
      </div>
    </div>
  );
};

export default AttractionCard;
