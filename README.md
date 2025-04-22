# Text-to-SQL

A lightweight Python toolkit for generating Entity-Relationship Diagrams (ERDs) and translating natural language queries into SQL statements using OpenAI’s language models.

## 🚀 Features

- **ERD Generation**: Connect to a PostgreSQL database, inspect the schema, and generate a Mermaid-formatted ERD.
- **SQL Tool**: List tables, describe their columns, and execute arbitrary SQL queries programmatically.
- **LLM-Powered Agent**: Interact via a conversational interface to translate user questions into valid SQL.
- **Modular Architecture**: Easily extend or replace components (connectors, tools, LLM backends).

## 📋 Prerequisites

- Python 3.8+ installed
- PostgreSQL database (e.g., `dvdrental` sample database)
  here is the link for data https://neon.tech/postgresqltutorial/dvdrental.zip
- An OpenAI API key with access to the desired model (e.g., `gpt-4o`)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/text-to-sql.git
   cd text-to-sql
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate       # Unix/macOS
   venv\Scripts\activate.bat    # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with the following entries:

```dotenv
# OpenAI settings
OPENAI_API_KEY=your_openai_api_key_here

# PostgreSQL settings
DB_NAME=dvdrental
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost      # optional, defaults to localhost
DB_PORT=5432           # optional, defaults to 5432
```

## 📂 Project Structure

```
text-to-sql/
├── src/
│   ├── agent.py            # Agent class for LLM-driven SQL generation
│   ├── tools.py            # SQLTool & DBConfig for database interactions
│   ├── utils.py            # ERD generation helper (Mermaid format)
│   ├── openai_utils.py     # Wrapper around OpenAI API
│   └── postgres_connector.py # SQLAlchemy-based connector
├── main.py                 # CLI entrypoint for interactive agent
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
└── README.md               # This documentation
```

## 📖 Usage

1.  **Run the interactive agent**
   ```bash
   python main.py
   ```
   - Enter natural language prompts (e.g., `List customers with overdue rentals.`)
   - The agent will return SQL and query results inline.
   - Type `exit` to quit.

## 🛠️ Example

```bash
$ python main.py
ERD Loaded
Database Analyst Agent is ready. Type 'exit' to quit.

Enter your query:

Response:
SELECT COUNT(*) FROM film WHERE release_year = 2006;
```

## 🤝 Contributing

Contributions are welcome! Please fork the repo and open a pull request:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am "Add awesome feature"`
4. Push and submit a PR

## 📜 License

This project is licensed under the MIT License © Vaibhav Lohar
