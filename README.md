# 🚗 Rentcars Data Platform — Case Técnico (Senior Data Engineer)

---

## Visão Geral

Solução end-to-end para ingestão, processamento e disponibilização de dados, priorizando simplicidade, custo e entrega funcional em ambiente controlado.

A arquitetura privilegia completude e governança sobre complexidade desnecessária, garantindo uma pipeline confiável, observável e otimizada.

---

# Arquitetura

```text
Raw (CSV)
   ↓
Spark (ETL)
   ↓
Silver (Parquet limpo e deduplicado)
   ↓
Gold (Agregações)
   ↓
FastAPI (Serving Layer)
```

---

#  Como rodar localmente

```bash
cd infra && docker-compose up --build
```

Acessos:

* Airflow: http://localhost:8080
* API: http://localhost:8000/docs
* Metrics (Prometheus): http://localhost:8000/metrics

---

# Estrutura do Projeto

```text
repo-case-de-rentcars/
├── pipeline/
│   ├── dags/
│   ├── core/
│   ├── tests/
│   └── run_pipeline.py
├── api/
├── infra/
├── observability/
├── governance.md
├── README.md
```

---

#  Decisões Técnicas e Trade-offs

## Spark local

Escolha: execução local para simplicidade e portabilidade.

Trade-off:

*  menor escalabilidade
*  facilidade de setup

---

## Parquet ao invés de Delta Lake

Escolha: reduzir complexidade e focar na entrega end-to-end.

Trade-off:

* ausência de ACID
* menor overhead operacional

---

## API lendo diretamente do Data Lake

Escolha: evitar banco intermediário.

Trade-off:

* maior latência
* menor custo e menor complexidade

---

## Small Files Handling

Implementado com:

* `coalesce` no Spark (compaction)
* controle de tamanho de arquivos (`spark.sql.files.maxPartitionBytes`)
* métrica de arquivos por partição
* alerta de threshold

Benefícios:

* redução de custo no Athena
* melhor performance de leitura

---

# Pipeline de Dados

## Idempotência

Deduplicação por `event_id` garantindo consistência:

```python
df.dropDuplicates(["event_id"])
```

---

## Late Arriving Data

Tratamento via watermark lógico:

```text
Filtro baseado em data mínima de evento
```

---

## Schema Evolution

Suporte a evolução de schema com:

```python
.option("mergeSchema", "true")
```

---

## Data Quality

Valores inválidos (nulos ou negativos) são tratados na camada de transformação, garantindo consistência downstream.

---

# Observabilidade

* Métricas expostas no padrão Prometheus
* Logging estruturado do pipeline
* Monitoramento de small files
* Métricas de pipeline via `pipeline_runs.csv`

---

# Alertas Implementados

* Taxa de falha > 15%
* Pipeline > 7200s
* Streaming lag > 300s
* Small files por partição

---

# Testes

## API

* Health check
* Autenticação (API Key)
* Endpoints principais

## Pipeline

* Validação de duplicidade
* Validação de valores negativos
* Consistência dos dados processados (silver layer)

---

# Estimativa de Custo AWS

| Serviço           | Estimativa |
| ----------------- | ---------- |
| S3 (100GB)        | ~$2.30     |
| Athena (1TB scan) | ~$5.00     |
| Glue/EMR          | ~$30       |
| Transferência     | ~$5        |

## Maior risco de custo

Athena → custo baseado em dados escaneados

---

# Otimizações de Custo (FinOps)

* Parquet + particionamento
* Lifecycle S3 (Standard → IA → Glacier)
* Uso de Spot Instances
* Compaction para evitar small files
* Predicate pushdown

---

# Limitações

* Não utiliza Delta Lake
* Pipeline não distribuído (local Spark)
* API sem cache
* Terraform simplificado

---

# Melhorias Futuras

* Delta Lake / Apache Iceberg
* Redis cache na API
* Deploy em Kubernetes
* CI/CD pipeline
* Data Quality framework (Great Expectations)

---

# Governança

Detalhes completos em:

[governance.md](./governance.md)

---

# Autor

Hugo Souza
