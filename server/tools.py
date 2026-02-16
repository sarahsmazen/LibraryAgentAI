import sqlite3
import os
import json
from langchain.tools import tool


DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "library.db"))

def run_query(query, params=()):
    """
    Executes a SELECT query and returns the results as a list of dictionaries.
    This helper ensures consistent data structure across all tools.
    """
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row  # Access columns by name
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

def run_commit(query, params=()):
    """
    Executes INSERT/UPDATE queries and commits changes to the database.
    Returns the ID of the last row inserted.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

@tool
def find_books(query_str: str, search_by: str = "title"):
    """
    Search for books in the library by title or author.
    Returns a list of matching books.
    """
    # Validating search field to prevent query errors
    column = "title" if search_by.lower() == "title" else "author"
    sql = f"SELECT * FROM books WHERE {column} LIKE ?"
    return run_query(sql, (f"%{query_str}%",))

@tool
def create_order(customer_id: int, items: list):
    """
    Registers a new book order and automatically reduces stock levels for multiple items.
    'items' should be a list of dictionaries: [{"isbn": "...", "qty": 3}]
    Required for Scenario 1 and general order processing.
    """
    # 1. Initialize the order in the orders table
    order_id = run_commit("INSERT INTO orders (customer_id) VALUES (?)", (customer_id,))
    
    order_summary = []
    
    for item in items:
        isbn = item['isbn']
        quantity = item['qty']
        
        # Check if the book exists and verify stock availability
        book = run_query("SELECT title, stock FROM books WHERE isbn = ?", (isbn,))
        if not book or book[0]['stock'] < quantity:
            # Skip items that are unavailable or out of stock
            continue 
            
        # 2. Record individual items in the order_items junction table
        run_commit("INSERT INTO order_items (order_id, isbn, quantity) VALUES (?, ?, ?)", 
                   (order_id, isbn, quantity))
        
        # 3. Decrement stock levels as required by the assessment [cite: 21, 35]
        new_stock = book[0]['stock'] - quantity
        run_commit("UPDATE books SET stock = ? WHERE isbn = ?", (new_stock, isbn))
        
        order_summary.append({
            "title": book[0]['title'], 
            "new_stock": new_stock
        })

    return {
        "order_id": order_id,
        "items_processed": order_summary,
        "status": "Order placed successfully"
    }

@tool
def restock_book(isbn: str, qty: int):
    """
    Increments the stock quantity for a specific book.
    Useful for inventory management tasks.
    """
    run_commit("UPDATE books SET stock = stock + ? WHERE isbn = ?", (qty, isbn))
    updated_info = run_query("SELECT title, stock FROM books WHERE isbn = ?", (isbn,))
    return dict(updated_info[0]) if updated_info else "Book not found."

@tool
def update_price(isbn: str, price: float):
    """
    Updates the selling price of a book.
    Requirement from assessment page 2.
    """
    run_commit("UPDATE books SET price = ? WHERE isbn = ?", (price, isbn))
    return f"Price for {isbn} updated to ${price}"

@tool
def order_status(order_id: int):
    """
    Provides a summary of a specific order including customer and book details.
    """
    sql = """
    SELECT o.id, c.name as customer, b.title, oi.quantity
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    JOIN order_items oi ON o.id = oi.order_id
    JOIN books b ON oi.isbn = b.isbn
    WHERE o.id = ?
    """
    results = run_query(sql, (order_id,))
    return [dict(row) for row in results]

@tool
def inventory_summary():
    """
    Identifies books with low stock (less than 5 units).
    Helpful for proactive restocking.
    """
    return run_query("SELECT title, stock FROM books WHERE stock < 5")