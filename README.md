# 📚 Library Desk AI Agent

A professional AI-powered Library Management System that allows a Desk Agent to manage books, customers, and orders using Natural Language.

This project utilizes **LangChain**, **FastAPI**, and **Streamlit** to provide a seamless interface for database interactions through an LLM agent.

---

## 🏗️ Project Structure

The project is organized into dedicated modules to ensure clean code and scalability:

```
Library-Desk-AI-Agent/
│
├── app/              # Streamlit Frontend (Chat UI)
├── server/           # FastAPI Backend + LangChain Agent + Tools
├── db/               # SQLite Database + schema + seed files
│   ├── schema.sql
│   ├── seed.sql
│   └── library.db
├── prompts/          # System prompts & LLM instructions
├── requirements.txt
└── README.md
```

- **`/app`** → Frontend Chat UI built with Streamlit  
- **`/server`** → Backend FastAPI server, LangChain Agent, and database tools  
- **`/db`** → Database schema, seed scripts, and SQLite file  
- **`/prompts`** → System prompts and LLM configuration  

---

## 🛠️ Tech Stack

- **LLM**: GPT-4o (OpenAI)  
- **Framework**: LangChain (Agentic Workflow & Tool Calling)  
- **API**: FastAPI (REST Endpoints)  
- **Frontend**: Streamlit  
- **Database**: SQLite  

---

## 🚀 Setup & Installation


### 1️⃣ Environment Variables

Create a `.env` file in the root directory (refer to `.env.example`) and add your OpenAI API Key:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

⚠️ Do not push your `.env` file to GitHub.

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Database Initialization

The database is pre-seeded according to the assessment requirements:

- ✅ 10 Books (Standard catalog items)
- ✅ 6 Customers (Library members)
- ✅ 4 Orders (Initial transaction history)

If you need to reinitialize the database:

```bash
sqlite3 db/library.db < db/schema.sql
sqlite3 db/library.db < db/seed.sql
```

---

## 🏃 Running the Project

### ▶ Step 1: Start the Backend Server

```bash
python server/main.py
```

The server will run at:

```
http://127.0.0.1:8000
```

---

### ▶ Step 2: Start the Frontend UI

```bash
streamlit run app/main.py
```

---

## 🤖 Agent Capabilities (Tools)

The AI Agent is equipped with the following tools:

- **`find_books`** → Search books by title or author  
- **`create_order`** → Process new orders and automatically reduce stock levels  
- **`restock_book`** → Increase stock quantity for specific books  
- **`update_price`** → Modify book pricing  
- **`order_status`** → Retrieve detailed order and customer summaries  
- **`inventory_summary`** → List books with low stock (less than 5 units)  

---

## 📝 Sample Scenarios Supported

### 🛒 Sales
```
We sold 3 copies of Clean Code to customer 2 today. Create the order and adjust stock.
```

### 🔁 Multi-tasking
```
Restock The Pragmatic Programmer by 10 and list all books by Andrew Hunt.
```

### 📊 Status Check
```
What's the status of order 3?
```

---

## 🧠 System Architecture Flow

1. User submits request in Streamlit UI  
2. Request is sent to FastAPI backend  
3. LangChain Agent interprets intent  
4. Agent selects appropriate tool  
5. Tool executes SQL operation  
6. Response is returned to the UI  



