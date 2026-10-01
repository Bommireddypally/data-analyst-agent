import time
import duckdb
from agent import ask
from eval_set import EVAL_SET

con = duckdb.connect("olist.duckdb", read_only=True)

def result_of(sql):
    return con.execute(sql).fetchall()

passed = 0
for item in EVAL_SET:
    gold = result_of(item["gold_sql"])
    answer, agent_sql = ask(item["question"])

    try:
        agent_result = result_of(agent_sql) if agent_sql else None
    except Exception:
        agent_result = None

    ok = agent_result == gold
    passed += ok
    print(f"Q{item['id']}: {'PASS' if ok else 'FAIL'} | {item['question']}")
    if not ok:
        print("  gold :", gold[:3])
        print("  agent:", (agent_result or "no SQL")[:3] if agent_result else "no SQL")
    time.sleep(2)   # be gentle with the free-tier rate limit

print(f"\nAccuracy: {passed}/{len(EVAL_SET)}")