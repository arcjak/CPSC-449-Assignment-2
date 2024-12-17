-- Create the database
CREATE DATABASE IF NOT EXISTS book_management;

-- Use the created database
USE book_management;

-- Create the 'books' table
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    published_year INT,
    genre VARCHAR(100),
    price FLOAT
);

-- Insert sample data into the 'books' table
INSERT INTO books (title, author, published_year, genre, price) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'Fiction', 10.99),
('1984', 'George Orwell', 1949, 'Dystopian', 12.50),
('To Kill a Mockingbird', 'Harper Lee', 1960, 'Fiction', 8.99),
('Moby Dick', 'Herman Melville', 1851, 'Adventure', 15.20),
('War and Peace', 'Leo Tolstoy', 1869, 'Historical Fiction', 20.00);
