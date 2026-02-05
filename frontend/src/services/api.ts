import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor для добавления Telegram initData
api.interceptors.request.use((config) => {
  const initData = window.Telegram?.WebApp?.initData;
  if (initData) {
    config.headers['X-Telegram-Init-Data'] = initData;
  }

  // Добавить токен если есть
  const token = localStorage.getItem('token');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  return config;
});

// Interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Удалить токен и перенаправить на авторизацию
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export default api;

// Cities API
export const getCities = () => api.get('/cities');
export const getCity = (id: number) => api.get(`/cities/${id}`);

// Attractions API
export const getAttractions = (params?: {
  city_id?: number;
  category?: string;
  page?: number;
  page_size?: number;
}) => api.get('/attractions', { params });

export const getAttraction = (id: number) => api.get(`/attractions/${id}`);

// Favorites API
export const getFavorites = () => api.get('/favorites');
export const addToFavorites = (attractionId: number) =>
  api.post('/favorites', { attraction_id: attractionId });
export const removeFromFavorites = (attractionId: number) =>
  api.delete(`/favorites/${attractionId}`);

// Auth API
export const telegramAuth = (initData: string) =>
  api.post('/auth/telegram', { init_data: initData });
