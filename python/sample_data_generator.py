import csv
import random
import os
from datetime import datetime, timedelta

def generate_sample_movies(count=100, output_file='../data/sample_movies.csv'):
    """Generate sample movie data for testing."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Sample genres
    genres = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror', 'Romance', 
              'Adventure', 'Fantasy', 'Animation', 'Thriller', 'Mystery']
    
    # Sample languages
    languages = ['en', 'es', 'fr', 'de', 'ja', 'ko', 'zh', 'it', 'ru']
    
    # Generate random movies
    movies = []
    for i in range(1, count+1):
        release_year = random.randint(1980, 2023)
        release_date = datetime(release_year, random.randint(1, 12), random.randint(1, 28))
        
        # Select 1-3 random genres
        movie_genres = random.sample(genres, random.randint(1, 3))
        
        movie = {
            'id': i,
            'title': f"Sample Movie {i}",
            'original_title': f"Original Title {i}",
            'release_year': release_year,
            'release_date': release_date.strftime('%Y-%m-%d'),
            'overview': f"This is a sample overview for movie {i}.",
            'popularity': round(random.uniform(0.5, 500.0), 1),
            'vote_average': round(random.uniform(1.0, 10.0), 1),
            'vote_count': random.randint(10, 10000),
            'runtime': random.randint(80, 180),
            'budget': random.randint(1000000, 200000000),
            'revenue': random.randint(0, 500000000),
            'language': random.choice(languages),
            'genres': ','.join(movie_genres)
        }
        movies.append(movie)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=movies[0].keys())
        writer.writeheader()
        writer.writerows(movies)
    
    print(f"Generated {count} sample movies and saved to {output_file}")
    return output_file

if __name__ == "__main__":
    generate_sample_movies()