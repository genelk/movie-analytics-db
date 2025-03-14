-- Top rated movies
CREATE OR REPLACE VIEW vw_top_rated_movies AS
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
    weighted_rating DESC;

-- Movies by genre
CREATE OR REPLACE VIEW vw_movies_by_genre AS
SELECT 
    g.name AS genre,
    COUNT(mg.movie_id) AS movie_count,
    AVG(m.vote_average) AS avg_rating,
    AVG(m.popularity) AS avg_popularity
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

-- Yearly trends
CREATE OR REPLACE VIEW vw_yearly_trends AS
SELECT 
    release_year,
    COUNT(*) AS movie_count,
    AVG(vote_average) AS avg_rating,
    AVG(popularity) AS avg_popularity,
    SUM(revenue) AS total_revenue,
    SUM(budget) AS total_budget
FROM 
    movies
WHERE 
    release_year IS NOT NULL
GROUP BY 
    release_year
ORDER BY 
    release_year DESC;

-- User activity
CREATE OR REPLACE VIEW vw_user_activity AS
SELECT 
    u.id AS user_id,
    u.username,
    COUNT(ur.id) AS rating_count,
    AVG(ur.rating) AS avg_rating,
    MIN(ur.rated_at) AS first_rating,
    MAX(ur.rated_at) AS last_rating
FROM 
    users u
LEFT JOIN 
    user_ratings ur ON u.id = ur.user_id
GROUP BY 
    u.id, u.username
ORDER BY 
    rating_count DESC;