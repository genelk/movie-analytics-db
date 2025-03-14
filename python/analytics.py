import matplotlib.pyplot as plt
import pandas as pd
import os
from db_connector import DatabaseConnector

class MovieAnalytics:
    """Generate analytics insights from movie database."""
    
    def __init__(self, db_connector):
        """Initialize with a database connector."""
        self.db = db_connector
        self.output_dir = '../output'
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def genre_popularity_analysis(self):
        """Analyze genre popularity over time."""
        query = """
        SELECT 
            g.name AS genre,
            m.release_year AS year,
            COUNT(*) AS movie_count,
            AVG(m.vote_average) AS avg_rating,
            AVG(m.popularity) AS avg_popularity
        FROM 
            genres g
        JOIN 
            movie_genres mg ON g.id = mg.genre_id
        JOIN 
            movies m ON mg.movie_id = m.id
        WHERE 
            m.release_year IS NOT NULL AND m.release_year >= 2000
        GROUP BY 
            g.name, m.release_year
        ORDER BY 
            g.name, m.release_year
        """
        
        data = self.db.execute_query(query)
        
        if not data:
            print("No data available for genre popularity analysis")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Get top 5 genres by movie count
        top_genres = df.groupby('genre')['movie_count'].sum().nlargest(5).index.tolist()
        
        # Filter DataFrame for top genres
        df_top = df[df['genre'].isin(top_genres)]
        
        # Create pivot table for plotting
        pivot_df = df_top.pivot(index='year', columns='genre', values='avg_rating')
        
        # Plot
        plt.figure(figsize=(12, 6))
        pivot_df.plot(kind='line', marker='o', ax=plt.gca())
        
        plt.title('Average Rating by Genre Over Time')
        plt.xlabel('Year')
        plt.ylabel('Average Rating')
        plt.grid(True, alpha=0.3)
        plt.legend(title='Genre')
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'genre_ratings_over_time.png')
        plt.savefig(output_path)
        print(f"Saved genre popularity analysis to {output_path}")
        
        return pivot_df
    
    def movie_release_trends(self):
        """Analyze movie release trends over years."""
        query = """
        SELECT 
            release_year,
            COUNT(*) AS movie_count,
            AVG(vote_average) AS avg_rating,
            AVG(popularity) AS avg_popularity
        FROM 
            movies
        WHERE 
            release_year IS NOT NULL AND release_year >= 1980
        GROUP BY 
            release_year
        ORDER BY 
            release_year
        """
        
        data = self.db.execute_query(query)
        
        if not data:
            print("No data available for release trends analysis")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Plot
        fig, ax1 = plt.subplots(figsize=(14, 7))
        
        # Plot movie count
        ax1.set_xlabel('Year')
        ax1.set_ylabel('Number of Movies', color='tab:blue')
        ax1.bar(df['release_year'], df['movie_count'], alpha=0.6, color='tab:blue')
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        
        # Create second y-axis for average rating
        ax2 = ax1.twinx()
        ax2.set_ylabel('Average Rating', color='tab:red')
        ax2.plot(df['release_year'], df['avg_rating'], color='tab:red', 
                 marker='o', linestyle='-', linewidth=2)
        ax2.tick_params(axis='y', labelcolor='tab:red')
        
        plt.title('Movie Releases and Ratings by Year')
        fig.tight_layout()
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'movie_release_trends.png')
        plt.savefig(output_path)
        print(f"Saved movie release trends analysis to {output_path}")
        
        return df
    
    def top_rated_movies_report(self, limit=20):
        """Generate a report of top-rated movies."""
        query = f"""
        SELECT 
            id, 
            title,
            release_year,
            vote_average,
            vote_count,
            weighted_rating,
            popularity
        FROM 
            movies
        WHERE 
            vote_count > 100
        ORDER BY 
            weighted_rating DESC
        LIMIT {limit}
        """
        
        data = self.db.execute_query(query)
        
        if not data:
            print("No data available for top rated movies report")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Save to CSV
        output_path = os.path.join(self.output_dir, 'top_rated_movies.csv')
        df.to_csv(output_path, index=False)
        print(f"Saved top-rated movies report to {output_path}")
        
        return df
    
    def user_rating_distribution(self):
        """Analyze the distribution of user ratings."""
        query = """
        SELECT 
            ROUND(rating, 0) AS rating_bin,
            COUNT(*) AS count
        FROM 
            user_ratings
        GROUP BY 
            rating_bin
        ORDER BY 
            rating_bin
        """
        
        data = self.db.execute_query(query)
        
        if not data:
            print("No data available for user rating distribution analysis")
            return
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Plot
        plt.figure(figsize=(10, 6))
        bars = plt.bar(df['rating_bin'], df['count'], color='skyblue')
        
        # Add count labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom')
        
        plt.title('Distribution of User Ratings')
        plt.xlabel('Rating')
        plt.ylabel('Number of Ratings')
        plt.xticks(range(1, 11))
        plt.grid(True, alpha=0.3, axis='y')
        
        # Save plot
        output_path = os.path.join(self.output_dir, 'user_rating_distribution.png')
        plt.savefig(output_path)
        print(f"Saved user rating distribution analysis to {output_path}")
        
        return df
    
    def run_all_analytics(self):
        """Run all analytics functions."""
        print("Running genre popularity analysis...")
        self.genre_popularity_analysis()
        
        print("\nRunning movie release trends analysis...")
        self.movie_release_trends()
        
        print("\nGenerating top rated movies report...")
        self.top_rated_movies_report()
        
        print("\nAnalyzing user rating distribution...")
        self.user_rating_distribution()
        
        print("\nAll analytics completed successfully!")

if __name__ == "__main__":
    # Example usage
    connector = DatabaseConnector()
    analytics = MovieAnalytics(connector)
    
    try:
        # Connect to database
        connector.connect()
        
        # Run all analytics
        analytics.run_all_analytics()
        
    except Exception as e:
        print(f"Analytics failed: {e}")
    
    finally:
        # Close connection
        connector.disconnect()