import os, json
import duckdb
from dotenv import load_dotenv
from openai import OpenAI

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
    try:
        df = con.execute(query).fetchdf()
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

SYSTEM = f"""You are a data analyst. Answer questions by querying this DuckDB database.
Write SQL, run it with the run_sql tool, and if it errors, fix it and try again.
Only state numbers you got from query results.

Schema:
{get_schema()}"""

def ask(question, max_steps=8):
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

        if not msg.tool_calls:          # no tool requested = final answer
            return msg.content

        for call in msg.tool_calls:
            query = json.loads(call.function.arguments)["query"]
            print(f"\n[step {step+1}] SQL:\n{query}")
            result = run_sql(query)
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