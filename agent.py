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
TOOLS = [{
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
}]

SYSTEM = f"""You are a data analyst. ...

Business rules:
- customer_id is unique per ORDER. To count real customers, use customer_unique_id.
- "Late" means order_delivered_customer_date > order_estimated_delivery_date.
- Only orders with order_status = 'delivered' have a delivery date.

Schema:
{get_schema()}"""

def ask(question, max_steps=8):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": question},
    ]
    last_sql = None
    for step in range(max_steps):
        resp = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            return msg.content, last_sql

        for call in msg.tool_calls:
            query = json.loads(call.function.arguments)["query"]
            print(f"\n[step {step+1}] SQL:\n{query}")
            result = run_sql(query)
            print(f"[result]\n{result[:500]}")
            if not result.startswith(("SQL error", "Error")):
                last_sql = query
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result,
            })
    return "Stopped: too many steps.", last_sql

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        answer, _ = ask(q)
        print("\nANSWER:", answer)