def ingest_all(spark):
    return {
        "events": spark.read.option("header", True).csv("data/raw_events.csv"),
        "transactions": spark.read.option("header", True).csv("data/raw_transactions.csv"),
        "partners": spark.read.option("header", True).csv("data/raw_partner_catalog.csv")
    }