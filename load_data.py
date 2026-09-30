import duckdb
from pathlib import Path

con = duckdb.connect("olist.duckdb")

for csv in Path("data").glob("*.csv"):
    table = csv.stem.replace("olist_", "").replace("_dataset", "")
    con.execute(
        f"CREATE OR REPLACE TABLE {table} AS "
        f"SELECT * FROM read_csv_auto('{csv.as_posix()}')"
    )
    n = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {n} rows")

con.close()