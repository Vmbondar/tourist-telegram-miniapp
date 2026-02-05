from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    country = Column(String, default="Russia")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    attractions = relationship("Attraction", back_populates="city", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<City(id={self.id}, name={self.name})>"
