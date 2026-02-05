from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Attraction(Base):
    __tablename__ = "attractions"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    address = Column(String)
    photo_url = Column(String)  # Одно фото (URL) для MVP
    category = Column(String, index=True)  # Музей, Парк, Памятник и т.д.
    rating = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    city = relationship("City", back_populates="attractions")
    favorites = relationship("Favorite", back_populates="attraction", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Attraction(id={self.id}, name={self.name}, city_id={self.city_id})>"
