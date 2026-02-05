export interface City {
  id: number;
  name: string;
  country: string;
  is_active: boolean;
  created_at: string;
}

export interface Attraction {
  id: number;
  city_id: number;
  name: string;
  description: string | null;
  address: string | null;
  photo_url: string | null;
  category: string | null;
  rating: number;
  is_active: boolean;
  created_at: string;
  is_favorite?: boolean;
}

export interface Favorite {
  id: number;
  user_id: number;
  attraction_id: number;
  created_at: string;
  attraction: Attraction;
}
