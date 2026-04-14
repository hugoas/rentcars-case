def main():
    import os
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col

    print(" Pipeline iniciado...")

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("rentcars") \
        .getOrCreate()

    # ======================
    #  PREVENÇÃO SMALL FILES
    # ======================
    spark.conf.set("spark.sql.files.maxPartitionBytes", 134217728)

    path = "/opt/airflow/data/raw/raw_events.csv"

    if not os.path.exists(path):
        raise Exception(f"Arquivo não encontrado: {path}")

    # ======================
    #  LEITURA + SCHEMA EVOLUTION
    # ======================
    df = spark.read.option("mergeSchema", "true").csv(path, header=True)

    print(f" Linhas (raw): {df.count()}")

    # ======================
    #  CAST DE TIPOS (IMPORTANTE)
    # ======================
    if "price_usd" in df.columns:
        df = df.withColumn("price_usd", col("price_usd").cast("double"))
        df = df.filter(col("price_usd").isNotNull())
        df = df.filter(col("price_usd") >= 0)
    

    # ======================
    #  DEDUPLICAÇÃO (IDEMPOTÊNCIA)
    # ======================
    if "event_id" in df.columns:
        before = df.count()
        df = df.dropDuplicates(["event_id"])
        after = df.count()
        print(f"🧹 Duplicados removidos: {before - after}")

    # ======================
    #  LATE ARRIVING DATA (WATERMARK)
    # ======================
    #  dataset usa event_ts (não event_timestamp)
    if "event_ts" in df.columns:
        df = df.filter(col("event_ts") >= "2025-01-01")

    # ======================
    #  COMPACTION (CORREÇÃO SMALL FILES)
    # ======================
    df = df.coalesce(4)

    # ======================
    #  SILVER
    # ======================
    silver_path = "/opt/airflow/data/silver/events"

    print(f" Salvando SILVER em: {silver_path}")
    df.write.mode("overwrite").parquet(silver_path)

    # ======================
    #  GOLD
    # ======================
    gold_path = "/opt/airflow/data/gold/events_agg"

    print(f" Salvando GOLD em: {gold_path}")
    df.groupBy().count().coalesce(1).write.mode("overwrite").parquet(gold_path)

    # ======================
    #  DETECÇÃO SMALL FILES
    # ======================
    def count_files(path):
        return len([f for f in os.listdir(path) if f.endswith(".parquet")])

    def avg_file_size(path):
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".parquet")]
        if not files:
            return 0
        sizes = [os.path.getsize(f) for f in files]
        return sum(sizes) / len(sizes)

    silver_files = count_files(silver_path)
    avg_size = avg_file_size(silver_path)

    print(f" Arquivos silver: {silver_files}")
    print(f" Tamanho médio: {avg_size / (1024 * 1024):.2f} MB")

    # ======================
    #  ALERTA SMALL FILES
    # ======================
    if avg_size < 128 * 1024 * 1024:
        print(" ALERTA: small files detectado (abaixo de 128MB)!")

    print(" Pipeline finalizado com sucesso")


if __name__ == "__main__":
    main()