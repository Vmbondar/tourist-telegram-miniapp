from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    attraction_id = Column(Integer, ForeignKey("attractions.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    attraction = relationship("Attraction", back_populates="favorites")

    # Уникальный constraint - пользователь не может добавить одну достопримечательность дважды
    __table_args__ = (
        UniqueConstraint('user_id', 'attraction_id', name='unique_user_attraction'),
    )

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, attraction_id={self.attraction_id})>"
