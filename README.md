# SQL Agent

SQL Agent for answering questions about the [Chinook database](https://www.sqlitetutorial.net/sqlite-sample-database/).

**Notes:**
- This is a modify version of SQL Agent from a LangGraph tutorial - [An agent for interacting with a SQL database](https://langchain-ai.github.io/langgraph/tutorials/sql-agent/)
- [Custom notebook and other examples](https://colab.research.google.com/drive/15iPieH2OrT8FS0FsClOJlV-bvuV4Eaa8?usp=sharing)

## How to run (Dev)

**GUI page:** http://localhost:8501/

### Set Up

Save the following environment variables in a `back/.env` file:

```bash
OPENAI_API_KEY=<your-openai-api-key>

# Optional
LANGCHAIN_API_KEY=<your-langchain-api-key>
LANGCHAIN_TRACING_V2=<true|false>
LANGCHAIN_PROJECT=<your-langchain-project>
```

### Manually

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python back/src/run_api.py
# In other teminal
source .venv/bin/activate
streamlit run front/src/app.py
```

### With Docker

Save the following environment variables in a `front/.env` file:

```bash
SQL_AGENT_BASE_URL="http://sql_agent_server:8000"
```

```bash
docker-compose up --build
```
