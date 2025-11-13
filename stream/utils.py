import os, time, pathlib
import pandas as pd

def ensure_dir(path: str):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def record_to_df(records):
    """Extract 'after' payloads from Debezium JSON records → DataFrame."""
    rows = []
    for r in records:
        after = r.get("payload", {}).get("after")
        if not after:
            continue
        rows.append(after)
    return pd.DataFrame(rows) if rows else pd.DataFrame()

def write_parquet(df: pd.DataFrame, base_dir: str, table: str, ts_col: str):
    if df.empty:
        return None
    df[ts_col] = pd.to_datetime(df[ts_col])
    df["ingest_date"] = df[ts_col].dt.date.astype(str)
    for date, g in df.groupby("ingest_date"):
        outdir = os.path.join(base_dir, "raw", table, f"ingest_date={date}")
        ensure_dir(outdir)
        outfile = os.path.join(outdir, f"part-{int(time.time()*1000)}.parquet")
        g.drop(columns=["ingest_date"]).to_parquet(outfile, index=False)
    return True
