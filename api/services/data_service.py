import pandas as pd
import os

def get_base_path():
    # Se estiver rodando no Docker (Airflow)
    if os.path.exists("/opt/airflow/data"):
        return "/opt/airflow/data/gold/events_agg"
    
    # Caso contrário (local)
    return "data/gold/events_agg"


def read_events():
    path = get_base_path()
    print(f"Lendo dados de: {path}")
    
    return pd.read_parquet(path)