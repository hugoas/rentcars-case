import pandas as pd

def test_no_duplicates():
    df = pd.read_parquet("data/silver/events")
    assert df["event_id"].nunique() == len(df)

def test_no_negative_values():
    df = pd.read_parquet("data/silver/events")

    if "price_usd" in df.columns:
        assert (df["price_usd"] >= 0).all()