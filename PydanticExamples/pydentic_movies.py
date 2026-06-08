from pydantic import BaseModel, Field
from typing import Optional

class Movies(BaseModel):
    pageSize: int = 10
    page: int = 1
    minPrice: int = 1
    maxPrice: int = 1000
    locations: list[str] = Field(default_factory=lambda: ["MSK", "SPB"])
    published: bool = True
    genreId: int| None = None
    createdAt: str = "asc"


class Genre(BaseModel):
    name: str

class Movie(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: str
    published: bool
    genreId: int
    genre: Genre
    createdAt: str
    rating: float

class MoviesResponse(BaseModel):
    movies: list[Movie]
    count: int
    page: int
    pageSize: int
    pageCount: int

class User(BaseModel):
    fullName: str

class Review(BaseModel):
    userId: str
    rating: int
    text: str
    hidden: bool
    createdAt: str
    user: User

class GetMovie(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: str
    published: bool
    genreId: int
    genre: Genre
    createdAt: str
    rating: float
    reviews: list[Review]