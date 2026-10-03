import time
import agent
from eval_set import EVAL_SET

con = agent.con

def norm(rows):
    return sorted(
        (tuple(round(v, 2) if isinstance(v, float) else v for v in row) for row in rows),
        key=str,
    )

passed = graded = 0
for item in EVAL_SET:
    answer = agent.ask(item["question"])
    agent_sql = agent.LAST_SQL

    if item["gold_sql"] is None:
        print(f"\nQ{item['id']}: MANUAL CHECK | {item['question']}\n  {answer}\n")
        continue

    graded += 1
    gold = norm(con.execute(item["gold_sql"]).fetchall())
    try:
        got = norm(con.execute(agent_sql).fetchall()) if agent_sql else None
    except Exception:
        got = None

    ok = got == gold
    passed += ok
    print(f"\nQ{item['id']}: {'PASS' if ok else 'FAIL'} | {item['question']}")
    if not ok:
        print("  gold :", gold)
        print("  agent:", got)
    time.sleep(2)

print(f"\nAccuracy: {passed}/{graded} (plus manual checks)")