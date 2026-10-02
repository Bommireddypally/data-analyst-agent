import os, json
import duckdb
from dotenv import load_dotenv
from openai import OpenAI
import re


load_dotenv()
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ["GROQ_API_KEY"],
)
MODEL = "openai/gpt-oss-120b"  # use any current Groq model that supports tool calling

con = duckdb.connect("olist.duckdb", read_only=True)  # read-only = basic safety

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

LAST_CHART = None

def make_chart(query, kind, x, y, title):
    global LAST_CHART
    check = run_sql(query)                      # reuse the SELECT-only guardrails
    if check.startswith(("Error", "SQL error")):
        return check
    if kind not in ("bar", "line"):
        return "Error: kind must be 'bar' or 'line'."
    df = con.execute(query.strip().rstrip(";")).fetchdf().head(50)
    if x not in df.columns or y not in df.columns:
        return f"Error: columns must be among {list(df.columns)}"
    Path("charts").mkdir(exist_ok=True)
    path = f"charts/chart_{len(list(Path('charts').glob('*.png'))) + 1}.png"
    fig, ax = plt.subplots(figsize=(8, 4))
    if kind == "bar":
        ax.bar(df[x].astype(str), df[y])
    else:
        ax.plot(df[x].astype(str), df[y], marker="o")
    ax.set_title(title)
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    LAST_CHART = path
    return f"Chart saved to {path}"

def get_schema():
    rows = con.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        ORDER BY table_name, ordinal_position
    """).fetchall()
    schema = {}
    for table, col, dtype in rows:
        schema.setdefault(table, []).append(f"{col} ({dtype})")
    return "\n".join(f"{t}: {', '.join(cols)}" for t, cols in schema.items())


def run_sql(query):
    q = query.strip().rstrip(";")
    if not re.match(r"^(select|with)\b", q, re.IGNORECASE):
        return "Error: only SELECT queries are allowed."
    if re.search(r"\b(insert|update|delete|drop|alter|create|attach|copy)\b", q, re.IGNORECASE):
        return "Error: query contains a forbidden keyword."
    try:
        df = con.execute(q).fetchdf()
        return df.head(50).to_string()
    except Exception as e:
        return f"SQL error: {e}"
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "run_sql",
            "description": "Run a read-only DuckDB SQL query and return the first 50 rows.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The SQL query"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "make_chart",
            "description": "Run a SELECT query and save a bar or line chart of two of its columns. Returns the image path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "kind": {"type": "string", "enum": ["bar", "line"]},
                    "x": {"type": "string", "description": "column for the x axis"},
                    "y": {"type": "string", "description": "numeric column for the y axis"},
                    "title": {"type": "string"},
                },
                "required": ["query", "kind", "x", "y", "title"],
            },
        },
    },
]

SYSTEM = f"""You are a data analyst. Answer questions by querying this DuckDB database.
Write SQL, run it with the run_sql tool, and if it errors, fix it and try again.
Only state numbers you got from query results.

Business rules:
- customer_id is unique per ORDER. To count real customers, use customer_unique_id.
- "Late" means order_delivered_customer_date > order_estimated_delivery_date.
- Only orders with order_status = 'delivered' have a delivery date.
- Currency is Brazilian reais (BRL). Never say USD.
- "Revenue" = SUM(price + freight_value) from order_items, for delivered orders,
  unless the user says otherwise. State which definition you used.
- Only describe filters and assumptions that appear in your SQL.
- If the question assumes something the data doesn't contain (e.g. returns,
  a year with no data), say so first, then offer the closest available measure.

Schema:
{get_schema()}"""


LAST_SQL = None

def ask(question, max_steps=8):
    global LAST_SQL, LAST_CHART
    LAST_SQL = None
    LAST_CHART = None
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    for step in range(max_steps):
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content

        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            if call.function.name == "make_chart":
                print(f"\n[step {step+1}] CHART: {args}")
                result = make_chart(**args)
            else:
                print(f"\n[step {step+1}] SQL:\n{args['query']}")
                result = run_sql(args["query"])
                if not result.startswith(("SQL error", "Error")):
                    LAST_SQL = args["query"]
            print(f"[result]\n{result[:500]}")
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })
    return "Stopped: too many steps."

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        print("\nANSWER:", ask(q))