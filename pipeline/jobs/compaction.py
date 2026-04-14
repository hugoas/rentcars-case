import os

def run_compaction(spark, path):
    df = spark.read.parquet(path)

    df.repartition(10) \
      .write.mode("overwrite") \
      .parquet(path)

    print(f"Compaction aplicado em {path}")