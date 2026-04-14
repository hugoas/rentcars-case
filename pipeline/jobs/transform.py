from pyspark.sql.functions import *
from pyspark.sql.window import Window


# GENERIC DEDUP
def deduplicate(df, key, order_col):
    window = Window.partitionBy(key).orderBy(col(order_col).desc())
    return df.withColumn("rn", row_number().over(window)) \
             .filter("rn = 1") \
             .drop("rn")

# EVENTS
def process_events(spark, df, watermark):
    df = df.withColumn("event_ts", to_timestamp("event_ts"))

    # Dedup
    df = deduplicate(df, "event_id", "event_ts")

    # Normalize
    df = df.withColumn("device", lower(col("device"))) \
           .withColumn("country", upper(col("country")))

    # Remove bots
    df = df.filter(col("is_bot_flag") == False)

    # Late arriving (watermark)
    df = df.filter(col("event_ts") >= watermark["events"])

    df.write.mode("overwrite").partitionBy("ingest_date") \
        .parquet("data/silver/events")

    return df

# -----------------------
# TRANSACTIONS
# -----------------------
def process_transactions(spark, df, watermark):
    df = df.withColumn("created_at", to_timestamp("created_at"))

    df = deduplicate(df, "transaction_id", "created_at")

    df = df.withColumn("status", lower(col("status")))

    # Filtrar inválidos
    df = df.filter(col("amount") > 0)

    df.write.mode("overwrite").partitionBy("ingest_ts") \
        .parquet("data/silver/transactions")

    return df

# -----------------------
# PARTNERS (SCHEMA EVOLUTION)
# -----------------------
def process_partners(spark, df):
    df = df.withColumn("webhook_enabled", col("webhook_enabled").cast("boolean"))

    df = df.withColumn("sla_hours", coalesce(col("sla_hours"), lit(0))) \
           .withColumn("avg_rating", coalesce(col("avg_rating"), lit(0.0)))

    df.write.mode("overwrite").parquet("data/silver/partners")

    return df