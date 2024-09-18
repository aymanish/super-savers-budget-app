-- Create the database (if not already created)
CREATE DATABASE IF NOT EXISTS savings_app;

-- Use the database
USE savings_app;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create savings goals table
CREATE TABLE IF NOT EXISTS savings_goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item VARCHAR(255),
    target_amount DECIMAL(10, 2),
    saved_amount DECIMAL(10, 2) DEFAULT 0,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
