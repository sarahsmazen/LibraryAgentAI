-- Database Schema for Library Desk Agent

-- Enable Foreign Key support for SQLite to ensure data integrity
PRAGMA foreign_keys = ON;

-- 1. Books table: Stores inventory and catalog details
CREATE TABLE books (
    isbn TEXT PRIMARY KEY,          -- Standard book identifier
    title TEXT NOT NULL,           -- Book title
    author TEXT NOT NULL,          -- Author name
    price REAL NOT NULL,           -- Unit price
    stock INTEGER NOT NULL DEFAULT 0 -- Current inventory level (used for create_order and restock)
);

-- 2. Customers table: Stores library member details
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- 3. Orders table: Tracks transaction headers
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- 4. Order Items table: Junction table for Order-to-Book relationship (Many-to-Many)
CREATE TABLE order_items (
    order_id INTEGER NOT NULL,
    isbn TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, isbn),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE RESTRICT
);

-- 5. Chat History: Stores conversation messages for LLM context
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,       -- Unique ID for each chat session
    role TEXT NOT NULL,             -- 'user', 'assistant', or 'system'
    content TEXT NOT NULL,          -- The text message
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tool Calls: Logs LLM tool executions and results
CREATE TABLE tool_calls (
    id TEXT PRIMARY KEY,            -- ID provided by the LLM
    session_id TEXT NOT NULL,
    name TEXT NOT NULL,             -- Tool function name (e.g., find_books)
    args_json TEXT,                 -- Input arguments in JSON format
    result_json TEXT,               -- Execution output/return value in JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);