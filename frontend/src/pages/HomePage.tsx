import React, { useEffect, useState } from 'react';
import Header from '../components/Layout/Header';
import Navigation from '../components/Layout/Navigation';
import AttractionList from '../components/Attraction/AttractionList';
import Loading from '../components/Loading';
import { useTelegram } from '../hooks/useTelegram';
import { useAuthStore } from '../store/authStore';
import { getCities, getAttractions, telegramAuth } from '../services/api';
import { City, Attraction } from '../types';
import './HomePage.css';

const HomePage: React.FC = () => {
  const { initData } = useTelegram();
  const { setAuth } = useAuthStore();
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState<City | null>(null);
  const [attractions, setAttractions] = useState<Attraction[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initialize = async () => {
      try {
        if (initData) {
          const authResponse = await telegramAuth(initData);
          setAuth(authResponse.data.user, authResponse.data.access_token);
        }

        const citiesResponse = await getCities();
        setCities(citiesResponse.data.items);

        if (citiesResponse.data.items.length > 0) {
          setSelectedCity(citiesResponse.data.items[0]);
        }
      } catch (error: any) {
        console.error('Initialization error:', error);
        setError(`Ошибка загрузки: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    initialize();
  }, [initData, setAuth]);

  useEffect(() => {
    const loadAttractions = async () => {
      if (!selectedCity) return;

      setLoading(true);
      try {
        const response = await getAttractions({
          city_id: selectedCity.id,
          page,
          page_size: 10,
        });

        if (page === 1) {
          setAttractions(response.data.items);
          setHasMore(response.data.items.length === 10 && response.data.items.length < response.data.total);
        } else {
          setAttractions((prev) => {
            const newAttractions = [...prev, ...response.data.items];
            setHasMore(response.data.items.length === 10 && newAttractions.length < response.data.total);
            return newAttractions;
          });
        }
      } catch (error: any) {
        console.error('Error loading attractions:', error);
        setError(`Ошибка загрузки достопримечательностей: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    loadAttractions();
  }, [selectedCity, page]);

  const handleCityChange = (city: City) => {
    setSelectedCity(city);
    setPage(1);
    setAttractions([]);
  };

  const handleLoadMore = () => {
    if (hasMore && !loading) {
      setPage((prev) => prev + 1);
    }
  };

  const handleFavoriteToggle = () => {
    if (selectedCity) {
      setPage(1);
      setAttractions([]);
    }
  };

  if (loading && attractions.length === 0) {
    return <Loading />;
  }

  if (error) {
    return (
      <div className="home-page">
        <Header title="Ошибка" />
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <p style={{ color: 'red', marginBottom: '20px' }}>{error}</p>
          <button onClick={() => window.location.reload()}>Перезагрузить</button>
          <br /><br />
          <a href="/test" style={{ color: '#3390ec' }}>Открыть тестовую страницу</a>
        </div>
        <Navigation />
      </div>
    );
  }

  return (
    <div className="home-page">
      <Header title="Достопримечательности" />

      {cities.length > 1 && (
        <div className="city-selector">
          {cities.map((city) => (
            <button
              key={city.id}
              className={`city-button ${
                selectedCity?.id === city.id ? 'active' : ''
              }`}
              onClick={() => handleCityChange(city)}
            >
              {city.name}
            </button>
          ))}
        </div>
      )}

      <AttractionList
        attractions={attractions}
        onFavoriteToggle={handleFavoriteToggle}
      />

      {hasMore && !loading && (
        <div className="load-more-container">
          <button className="load-more-button" onClick={handleLoadMore}>
            Загрузить ещё
          </button>
        </div>
      )}

      {loading && attractions.length > 0 && (
        <div className="loading-more">
          <Loading />
        </div>
      )}

      <Navigation />
    </div>
  );
};

export default HomePage;
