import json
from pyspark.sql.functions import max

def load_watermark():
    try:
        with open("watermark.json") as f:
            return json.load(f)
    except:
        return {"events": "1900-01-01"}

def save_watermark(df, col_name):
    max_ts = df.agg(max(col_name)).collect()[0][0]

    with open("watermark.json", "w") as f:
        json.dump({"events": str(max_ts)}, f)