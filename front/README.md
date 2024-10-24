# SQL Agent - GUI

## Set up
Save the following environment variables in a `.env` file:

```bash
SQL_AGENT_BASE_URL=<server-base-url>
```

## How to run

Page: http://localhost:8501/

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```