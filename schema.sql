CREATE DATABASE IF NOT EXISTS media_monitorings DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE media_monitorings;

CREATE TABLE IF NOT EXISTS channels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    channel_username VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    channel_id INT NOT NULL,
    telegram_post_id BIGINT NOT NULL,
    text TEXT,
    views INT DEFAULT 0,
    published_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    UNIQUE KEY unique_post (channel_id, telegram_post_id)
);

CREATE TABLE IF NOT EXISTS search_queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS matches (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query_id INT NOT NULL,
    post_id INT NOT NULL,
    similarity_score FLOAT NOT NULL,
    match_type ENUM('exact', 'rewrite', 'mention') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_original BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (query_id) REFERENCES search_queries(id) ON DELETE CASCADE,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);
