# Tourist Guide - Frontend

React приложение для Telegram Mini App.

## Требования

- Node.js 16+ и npm

## Установка

```bash
npm install
```

## Запуск в режиме разработки

```bash
npm start
```

Приложение откроется на `http://localhost:3000`

## Сборка для продакшена

```bash
npm run build
```

## Переменные окружения

Создайте файл `.env`:

```
REACT_APP_API_URL=http://localhost:8000/api/v1
```

Для продакшена используйте URL вашего backend API.

## Структура проекта

```
src/
├── components/          # React компоненты
│   ├── Layout/         # Header, Navigation
│   ├── Attraction/     # Компоненты достопримечательностей
│   └── Loading.tsx     # Индикатор загрузки
├── pages/              # Страницы приложения
│   ├── HomePage.tsx
│   ├── AttractionDetailPage.tsx
│   └── FavoritesPage.tsx
├── hooks/              # Custom React hooks
│   └── useTelegram.ts  # Хук для работы с Telegram
├── services/           # API сервисы
│   └── api.ts          # Axios клиент и API методы
├── store/              # Zustand хранилища
│   └── authStore.ts    # Состояние авторизации
├── types/              # TypeScript типы
│   └── index.ts
├── App.tsx             # Главный компонент
└── index.tsx           # Точка входа
```

## Основные функции

- Просмотр списка достопримечательностей по городам
- Детальная информация о достопримечательности
- Добавление в избранное
- Интеграция с Telegram Mini App SDK
- Автоматическая авторизация через Telegram
- Адаптивная верстка для мобильных устройств
- Использование цветовой схемы Telegram
