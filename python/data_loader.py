import csv
import os
import json
import random
from datetime import datetime
from db_connector import DatabaseConnector

class MovieDataLoader:
    """Load movie data into the PostgreSQL database."""
    
    def __init__(self, db_connector):
        """Initialize with a database connector."""
        self.db = db_connector
    
    def load_movies_from_csv(self, csv_path):
        """Load movies from a CSV file."""
        if not os.path.exists(csv_path):
            print(f"CSV file not found: {csv_path}")
            return 0
        
        inserted = 0
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    # Insert movie
                    query = """
                    INSERT INTO movies (
                        title, original_title, release_year, overview, 
                        popularity, vote_average, vote_count, runtime,
                        budget, revenue, language, poster_path, backdrop_path
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) ON CONFLICT (id) DO UPDATE SET
                        title = EXCLUDED.title,
                        original_title = EXCLUDED.original_title,
                        release_year = EXCLUDED.release_year,
                        overview = EXCLUDED.overview,
                        popularity = EXCLUDED.popularity,
                        vote_average = EXCLUDED.vote_average,
                        vote_count = EXCLUDED.vote_count,
                        runtime = EXCLUDED.runtime,
                        budget = EXCLUDED.budget,
                        revenue = EXCLUDED.revenue,
                        language = EXCLUDED.language,
                        poster_path = EXCLUDED.poster_path,
                        backdrop_path = EXCLUDED.backdrop_path,
                        updated_at = CURRENT_TIMESTAMP
                    RETURNING id
                    """
                    
                    # Handle potential missing or malformed fields
                    release_year = int(row.get('release_year', 0)) if row.get('release_year', '').isdigit() else None
                    vote_average = float(row.get('vote_average', 0)) if row.get('vote_average', '') else None
                    vote_count = int(row.get('vote_count', 0)) if row.get('vote_count', '').isdigit() else 0
                    
                    params = (
                        row.get('title', ''),
                        row.get('original_title', ''),
                        release_year,
                        row.get('overview', ''),
                        float(row.get('popularity', 0)) if row.get('popularity', '') else 0,
                        vote_average,
                        vote_count,
                        int(row.get('runtime', 0)) if row.get('runtime', '').isdigit() else None,
                        int(row.get('budget', 0)) if row.get('budget', '').isdigit() else 0,
                        int(row.get('revenue', 0)) if row.get('revenue', '').isdigit() else 0,
                        row.get('language', ''),
                        row.get('poster_path', ''),
                        row.get('backdrop_path', '')
                    )
                    
                    result = self.db.execute_query(query, params)
                    
                    if result:
                        movie_id = result[0]['id']
                        
                        # Handle genres if present
                        genre_str = row.get('genres', '')
                        if genre_str:
                            genres = [g.strip() for g in genre_str.split(',')]
                            self._add_genres_to_movie(movie_id, genres)
                        
                        inserted += 1
                        
                        if inserted % 100 == 0:
                            print(f"Inserted {inserted} movies...")
            
            print(f"Successfully loaded {inserted} movies from {csv_path}")
            return inserted
                    
        except Exception as e:
            print(f"Error loading movies from CSV: {e}")
            raise
    
    def _add_genres_to_movie(self, movie_id, genres):
        """Add genres to a movie, creating genres if they don't exist."""
        for genre_name in genres:
            if not genre_name:
                continue
                
            # Get or create genre
            query = """
            INSERT INTO genres (name)
            VALUES (%s)
            ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
            RETURNING id
            """
            result = self.db.execute_query(query, (genre_name,))
            genre_id = result[0]['id']
            
            # Associate genre with movie
            query = """
            INSERT INTO movie_genres (movie_id, genre_id)
            VALUES (%s, %s)
            ON CONFLICT (movie_id, genre_id) DO NOTHING
            """
            self.db.execute_query(query, (movie_id, genre_id), fetch=False)
    
    def generate_sample_users(self, count=100):
        """Generate sample users for testing."""
        inserted = 0
        
        try:
            for i in range(count):
                username = f"user{i+1}"
                email = f"user{i+1}@example.com"
                password_hash = f"dummy_hash_{i+1}"  # In real scenario, use proper hashing
                
                query = """
                INSERT INTO users (username, email, password_hash)
                VALUES (%s, %s, %s)
                ON CONFLICT (username) DO NOTHING
                """
                
                result = self.db.execute_query(query, (username, email, password_hash), fetch=False)
                inserted += result
            
            print(f"Successfully generated {inserted} sample users")
            return inserted
        
        except Exception as e:
            print(f"Error generating sample users: {e}")
            raise
    
    def generate_sample_ratings(self, rating_count=1000):
        """Generate sample ratings for testing."""
        try:
            # Get all user IDs
            user_query = "SELECT id FROM users"
            users = self.db.execute_query(user_query)
            
            if not users:
                print("No users found. Please generate sample users first.")
                return 0
            
            # Get all movie IDs
            movie_query = "SELECT id FROM movies"
            movies = self.db.execute_query(movie_query)
            
            if not movies:
                print("No movies found. Please load movies first.")
                return 0
            
            # Extract IDs from results
            user_ids = [user['id'] for user in users]
            movie_ids = [movie['id'] for movie in movies]
            
            inserted = 0
            
            for _ in range(rating_count):
                user_id = random.choice(user_ids)
                movie_id = random.choice(movie_ids)
                rating = round(random.uniform(1, 10), 1)  # Random rating between 1.0 and 10.0
                
                query = """
                INSERT INTO user_ratings (user_id, movie_id, rating)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, movie_id) DO UPDATE SET
                    rating = EXCLUDED.rating,
                    rated_at = CURRENT_TIMESTAMP
                """
                
                result = self.db.execute_query(query, (user_id, movie_id, rating), fetch=False)
                inserted += result
                
                if inserted % 100 == 0:
                    print(f"Inserted {inserted} ratings...")
            
            print(f"Successfully generated {inserted} sample ratings")
            return inserted
        
        except Exception as e:
            print(f"Error generating sample ratings: {e}")
            raise

if __name__ == "__main__":
    # Example usage
    connector = DatabaseConnector()
    loader = MovieDataLoader(connector)
    
    try:
        # Connect to database
        connector.connect()
        
        # Create schema
        connector.execute_script("../sql/schema.sql")
        
        # Load data
        # Uncomment and modify these lines to load your data
        # loader.load_movies_from_csv("../data/movies.csv")
        # loader.generate_sample_users(100)
        # loader.generate_sample_ratings(1000)
        
        # Create analytics views
        connector.execute_script("../sql/analytics_views.sql")
        
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Database setup failed: {e}")
    
    finally:
        # Close connection
        connector.disconnect()