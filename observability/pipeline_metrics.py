import pandas as pd

def get_pipeline_metrics():
    df = pd.read_csv("data/pipeline_runs.csv")

    return {
        "avg_duration": df["duration"].mean(),
        "fail_rate": (df["status"] == "failed").mean(),
        "max_duration": df["duration"].max()
    }