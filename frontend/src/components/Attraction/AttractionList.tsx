import React from 'react';
import { Attraction } from '../../types';
import AttractionCard from './AttractionCard';
import './AttractionList.css';

interface AttractionListProps {
  attractions: Attraction[];
  onFavoriteToggle?: () => void;
}

const AttractionList: React.FC<AttractionListProps> = ({
  attractions,
  onFavoriteToggle,
}) => {
  if (attractions.length === 0) {
    return (
      <div className="empty-state">
        <p>Достопримечательности не найдены</p>
      </div>
    );
  }

  return (
    <div className="attraction-list">
      {attractions.map((attraction) => (
        <AttractionCard
          key={attraction.id}
          attraction={attraction}
          onFavoriteToggle={onFavoriteToggle}
        />
      ))}
    </div>
  );
};

export default AttractionList;
