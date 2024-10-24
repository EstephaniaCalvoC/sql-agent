# SQL Agent - Service

Server for the SQL Agent. It's built with FastAPI and LangGraph.

## Set up

Save the following environment variables in a `.env` file:

```bash
OPENAI_API_KEY=<your-openai-api-key>

# Optional
LANGCHAIN_API_KEY=<your-langchain-api-key>
LANGCHAIN_TRACING_V2=<true|false>
LANGCHAIN_PROJECT=<your-langchain-project>
```

## How to run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_api.py
```

## Test

```bash
cd src
python -m pytest ../tests
```
