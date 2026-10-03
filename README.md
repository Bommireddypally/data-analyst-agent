# data-analyst-agent
LLM agent that answers business questions by writing SQL and analyzing data
# Olist Data Analyst Agent

An LLM agent that answers business questions about the Olist Brazilian
e-commerce dataset by writing SQL, running it on DuckDB, and charting results.

![screenshot](screenshot.png)

## What it does
- Turns questions into SQL and checks its own results
- Recovers from SQL errors by reading the error message and retrying
- Draws bar and line charts through a restricted `make_chart` tool
- Shows the SQL behind every answer

## How it works
Question -> LLM (Groq, OpenAI-compatible API) -> tool call (run_sql / make_chart)
-> result -> LLM -> answer. Loop capped at 8 steps.

## Guardrails
- Read-only DuckDB connection
- SELECT/WITH only; destructive keywords blocked
- Chart tool takes a query and column names, so the model never executes code

## Evaluation
- N questions with hand-written gold SQL, compared on result rows
- Latest score: X/Y auto-graded, plus manual trap questions (no 2020 data, no returns data)
- Business rules in the system prompt fixed two early failures: an invented
  currency (USD instead of BRL) and "canceled" reported as "returned"
- Known limitation: [one honest line, e.g. unrequested filters on some questions]

## Run it
pip install -r requirements.txt
# put GROQ_API_KEY in .env, download the Olist CSVs into data/
python load_data.py
streamlit run app.py