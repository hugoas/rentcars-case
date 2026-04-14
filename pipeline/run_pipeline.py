def main():
    import os

    print("Pipeline iniciado")
    print("Current dir:", os.getcwd())
    print("Files:", os.listdir("/opt/airflow/data"))

    from pyspark.sql import SparkSession

    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("rentcars") \
        .getOrCreate()

    print("Spark iniciado")

    path = "/opt/airflow/data/raw/raw_events.csv"

    print("Tentando ler:", path)

    if not os.path.exists(path):
        raise Exception(f"Arquivo não encontrado: {path}")

    df = spark.read.csv(path, header=True)

    print("Linhas:", df.count())

    df = df.coalesce(4)

    # SILVER
    silver_path = "/opt/airflow/data/silver/events"

    print("Salvando silver em:", silver_path)

    df.write.mode("overwrite").parquet(silver_path)

    # GOLD
    gold_path = "/opt/airflow/data/gold/events_agg"

    print("Salvando gold em:", gold_path)

    df.groupBy().count().coalesce(1).write.mode("overwrite").parquet(gold_path)


    # SMALL FILES METRIC

    def count_files(path):
        return len([f for f in os.listdir(path) if f.endswith(".parquet")])

    silver_files = count_files(silver_path)
    gold_files = count_files(gold_path)

    print(f"Small files (silver): {silver_files}")
    print(f"Small files (gold): {gold_files}")

    if silver_files > 50:
        print("ALERTA: muitos arquivos pequenos no SILVER!!!")

    if gold_files > 10:
        print("ALERTA: muitos arquivos pequenos no GOLD!!!")

    print("Pipeline finalizado")


if __name__ == "__main__":
    main()