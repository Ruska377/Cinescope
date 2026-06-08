from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.orm import  declarative_base
from typing import Dict, Any

Base = declarative_base()

class MovieDBModel(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    genre_id = Column(Integer)
    created_at = Column(String)
    rating = Column(Integer)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'imageUrl': self.imageUrl,
            'location': self.location,
            'published': self.published,
            'genreId': self.genreId,
            'createdAt': self.createdAt,
            'rating': self.rating
        }

    def __repr__(self):
        return f"<Movie(id='{self.id}', name='{self.name}')>"