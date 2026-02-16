-- ==========================================================
-- Seed Data for Library Desk Agent
-- Requirement: 10 books, 6 customers, 4 orders
-- ==========================================================

-- Insert 10 books into the catalog
INSERT INTO books (isbn, title, author, price, stock) VALUES
('978-0132350884', 'Clean Code', 'Robert C. Martin', 42.50, 15),
('978-0201616224', 'The Pragmatic Programmer', 'Andrew Hunt', 45.00, 10),
('978-0134494166', 'Clean Architecture', 'Robert C. Martin', 38.00, 12),
('978-0596007126', 'Head First Design Patterns', 'Eric Freeman', 50.00, 20),
('978-0137081073', 'The Clean Coder', 'Robert C. Martin', 35.00, 7),
('978-0201633610', 'Design Patterns', 'Erich Gamma', 55.00, 5),
('978-1617292231', 'Soft Skills', 'John Sonmez', 30.00, 18),
('978-0131103627', 'C Programming Language', 'Brian Kernighan', 40.00, 4),
('978-0321125217', 'Refactoring', 'Martin Fowler', 48.00, 9),
('978-0735619678', 'Code Complete', 'Steve McConnell', 52.00, 6);

-- Insert 6 customers
INSERT INTO customers (name, email) VALUES
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com'),
('Charlie Brown', 'charlie@example.com'),
('David Wilson', 'david@example.com'),
('Eve Adams', 'eve@example.com'),
('Frank Castle', 'frank@example.com');

-- Insert 4 initial orders
INSERT INTO orders (customer_id) VALUES (1), (2), (3), (4);

-- Insert items for the 4 orders
INSERT INTO order_items (order_id, isbn, quantity) VALUES
(1, '978-0132350884', 1), -- Alice ordered Clean Code
(2, '978-0201616224', 2), -- Bob ordered 2 copies of Pragmatic Programmer
(3, '978-0134494166', 1), -- Charlie ordered Clean Architecture
(4, '978-0596007126', 1); -- David ordered Head First Design Patterns