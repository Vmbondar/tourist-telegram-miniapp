import { useEffect, useState } from 'react';

declare global {
  interface Window {
    Telegram?: any;
  }
}

interface TelegramUser {
  id: number;
  first_name: string;
  last_name?: string;
  username?: string;
  language_code?: string;
  photo_url?: string;
}

export const useTelegram = () => {
  const [tg, setTg] = useState<any>(null);
  const [user, setUser] = useState<TelegramUser | null>(null);

  useEffect(() => {
    const telegram = window.Telegram?.WebApp;
    if (telegram) {
      telegram.ready();
      telegram.expand();
      setTg(telegram);
      setUser(telegram.initDataUnsafe?.user || null);
    }
  }, []);

  return {
    tg,
    user,
    initData: tg?.initData,
    themeParams: tg?.themeParams,
    colorScheme: tg?.colorScheme,
    isReady: !!tg,
  };
};
