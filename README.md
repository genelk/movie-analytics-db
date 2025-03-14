# Movie Analytics Database

A PostgreSQL-based movie analytics system that demonstrates database design, data analysis, and SQL reporting capabilities. This project showcases the implementation of a relational database with Python integration for movie data analytics.

## Project Overview

This project is a proof of concept demonstrating PostgreSQL database skills, SQL analytics, and Python integration. It features:

* Robust database schema with properly designed tables and relationships
* Advanced SQL queries and analytical views
* Python integration for data loading and analysis
* Data visualization capabilities
* Sample data generation for testing

## Features

* **Database Schema**: Well-structured PostgreSQL schema with proper constraints and relationships
* **Analytics Views**: Pre-defined SQL views for common analytical queries
* **Data Generator**: Python script to generate sample movie data for testing
* **Data Loader**: Utilities to populate database from CSV files
* **Visual Analytics**: Python scripts to generate visualizations from database queries
* **Query Tool**: Simple interface to run custom SQL queries

## Tech Stack

* **PostgreSQL**: For database storage and analytics
* **Python**: For data processing and visualization
* **psycopg2**: For Python-PostgreSQL connection
* **pandas**: For data manipulation
* **matplotlib/seaborn**: For data visualization

## Project Structure

```
movie_analytics_db/
├── sql/                    # SQL scripts
│   ├── schema.sql          # Database schema definition
│   └── analytics_views.sql # Pre-defined analytical views
├── python/                 # Python scripts
│   ├── db_connector.py     # Database connection utility
│   ├── data_loader.py      # Data loading functionality
│   ├── sample_data_generator.py # Sample data creation
│   ├── analytics.py        # Analytics and visualization
│   └── run_query.py        # Custom query runner
├── data/                   # Sample data (not tracked in git)
├── output/                 # Generated reports and visualizations
├── .env                    # Database configuration (not tracked in git)
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites

* PostgreSQL 12 or higher
* Python 3.8 or higher
* pip package manager

### Database Setup

1. Install PostgreSQL if not already installed
2. Create a new database:
   ```sql
   CREATE DATABASE movie_analytics;
   ```
3. Create a `.env` file in the project root with your database configuration:
   ```
   DB_NAME=movie_analytics
   DB_USER=postgres
   DB_PASSWORD=your_actual_password
   DB_HOST=localhost
   DB_PORT=5432
   ```
4. Run the schema setup script:
   ```bash
   psql -U postgres -d movie_analytics -f sql/schema.sql
   ```
   Or use the Python script which will handle this for you:
   ```bash
   cd python
   python data_loader.py
   ```

### Python Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate  # On Windows
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

### Generate Sample Data

1. Generate sample movie data:
   ```bash
   cd python
   python sample_data_generator.py
   ```

## Usage

### Loading Data

```bash
cd python
python data_loader.py
```

### Running Analytics

```bash
cd python
python analytics.py
```

This will generate several reports and visualizations in the `output` directory.

### Running Custom Queries

```bash
cd python
python run_query.py "SELECT title, release_year, vote_average FROM movies ORDER BY vote_average DESC LIMIT 10;"
```

## Example Queries

Here are some example SQL queries you can try with this database:

### Top Rated Movies
```sql
SELECT 
    title, 
    release_year, 
    vote_average, 
    vote_count 
FROM 
    movies 
WHERE 
    vote_count > 100 
ORDER BY 
    vote_average DESC 
LIMIT 10;
```

### Movies by Genre
```sql
SELECT 
    g.name AS genre, 
    COUNT(*) AS movie_count,
    AVG(m.vote_average) AS avg_rating
FROM 
    genres g
JOIN 
    movie_genres mg ON g.id = mg.genre_id
JOIN 
    movies m ON mg.movie_id = m.id
GROUP BY 
    g.name
ORDER BY 
    movie_count DESC;
```

### Yearly Trends
```sql
SELECT 
    release_year,
    COUNT(*) AS movie_count,
    AVG(vote_average) AS avg_rating,
    AVG(popularity) AS avg_popularity
FROM 
    movies
WHERE 
    release_year IS NOT NULL
GROUP BY 
    release_year
ORDER BY 
    release_year DESC;
```

## Contributing

This is a portfolio project, but suggestions and improvements are welcome. Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.