from faker import Faker

fake = Faker(locale='en_US')

class MoviesData:

    @staticmethod
    def search_data_movies():
        return {
            "pageSize": 10,
            "page": 1,
            "minPrice": 1,
            "maxPrice": 1000,
            "locations": ["SPB"],
            "published": True,
            "genreId": 1,
            "createdAt": "asc"
        }

    @staticmethod
    def search_data_movies_without_locations():
        return {
            "pageSize": 10,
            "page": 1,
            "minPrice": 1,
            "maxPrice": 1000,
            "published": True,
            "genreId": 1,
            "createdAt": "asc"
        }

    @staticmethod
    def created_movie_data():
        return {
            "name": fake.name(),
            "description": fake.text(),
            "imageUrl": "https://image.url",
            "price": fake.random_int(min=1, max=1000),
            "location": fake.random_element(elements=("MSK", "SPB")),
            "published": fake.boolean(),
            "genreId": fake.random_int(min=1, max=5)
        }

    @staticmethod
    def updated_data():
        return {"name": "new name", "price": 999}