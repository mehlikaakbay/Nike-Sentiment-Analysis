-- ===============================
-- A. Sentiment & Engagement Metrics
-- ===============================

-- Query 1: Average score, engagement, and comments
SELECT 
  ROUND(AVG(score), 2) AS avg_score,
  ROUND(AVG(engagement_score), 2) AS avg_engagement,
  ROUND(AVG(num_comments), 2) AS avg_comments
FROM nike_posts;

-- Query 2: Top 5 most-commented posts
SELECT title, num_comments, score
FROM nike_posts
ORDER BY num_comments DESC
LIMIT 5;

-- ===============================
-- B. User & Platform Trends
-- ===============================

-- Query 3: Top 10 most active users
SELECT author, COUNT(*) AS post_count
FROM nike_posts
GROUP BY author
ORDER BY post_count DESC
LIMIT 10;

-- Query 4: Most active days of the week
SELECT day_of_week, COUNT(*) AS posts
FROM nike_posts
GROUP BY day_of_week
ORDER BY posts DESC;

-- Query 5: Most used search keywords
SELECT search_keyword, COUNT(*) AS usage
FROM nike_posts
GROUP BY search_keyword
ORDER BY usage DESC;

-- ===============================
-- C. Anomalies & Patterns
-- ===============================

-- Query 6: Posts with unusually high scores (possible virality)
SELECT id, title, score
FROM nike_posts
WHERE score > 20000
ORDER BY score DESC;

-- Query 7: Days with the highest average engagement
SELECT date_only, COUNT(*) AS post_count, AVG(engagement_score) AS avg_engagement
FROM nike_posts
GROUP BY date_only
ORDER BY avg_engagement DESC
LIMIT 5;
