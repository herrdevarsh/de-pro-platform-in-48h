import json, os, sys, time
from confluent_kafka import Consumer
from utils import record_to_df, write_parquet, ensure_dir

BROKER = os.getenv("BROKER","localhost:9092")
LAKE_DIR = os.getenv("LAKE_DIR","./lake")

TOPICS = {
  "public.customers": {"topic":"ecom.public.customers","ts_col":"updated_at"},
  "public.orders":    {"topic":"ecom.public.orders","ts_col":"updated_at"},
  "public.events":    {"topic":"ecom.public.events","ts_col":"updated_at"},
}

def make_consumer(group_id="lake-writer"):
    return Consumer({
        "bootstrap.servers": BROKER,
        "group.id": group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True
    })

def run():
    ensure_dir(LAKE_DIR)
    c = make_consumer()
    c.subscribe([cfg["topic"] for cfg in TOPICS.values()])
    buffers = {k: [] for k in TOPICS}
    last_flush = time.time()
    FLUSH_SEC = 5
    try:
        while True:
          msg = c.poll(1.0)
          if msg is None:
              if time.time()-last_flush > FLUSH_SEC:
                  for table, cfg in TOPICS.items():
                      df = record_to_df(buffers[table])
                      if not df.empty:
                          write_parquet(df, LAKE_DIR, table.split(".")[1], cfg["ts_col"])
                      buffers[table] = []
                  last_flush = time.time()
              continue
          if msg.error():
              print(f"Kafka error: {msg.error()}", file=sys.stderr)
              continue
          payload = json.loads(msg.value().decode("utf-8"))
          tbl = payload.get("source",{}).get("table")
          key = f"public.{tbl}"
          if key in buffers:
              buffers[key].append(payload)
    except KeyboardInterrupt:
        pass
    finally:
        c.close()

if __name__ == "__main__":
    run()
