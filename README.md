# 🚗 Rentcars Data Platform — Case Técnico (Senior Data Engineer)

---

## Visão Geral

Este projeto implementa uma plataforma de dados ponta-a-ponta baseada em arquitetura Lakehouse, com ingestão, processamento e serving de dados.

A solução prioriza:

* Simplicidade com entrega completa end-to-end
* Eficiência de custos (FinOps)
* Observabilidade e governança

---

# Arquitetura

```text
Raw (CSV)
   ↓
Spark (ETL)
   ↓
Silver (Parquet)
   ↓
Gold (Agregações)
   ↓
FastAPI (Serving Layer)
```

---

# Como rodar localmente

```bash
cd infra
docker-compose up --build
```

Acessos:

* Airflow: http://localhost:8080
* API: http://localhost:8000/docs
* Metrics: http://localhost:8000/metrics

---

# Estrutura do Projeto

```text
repo-case-de-rentcars/
├── pipeline/
├── api/
├── infra/
├── observability/
├── governance.md
├── README.md
```

---

#  Decisões Técnicas e Trade-offs

## 🔹 Spark local

Escolha: execução local para simplicidade

Trade-off:

*  menor escalabilidade
* facilidade de setup

---

##  Parquet ao invés de Delta Lake

Escolha: simplicidade

Trade-off:

*  sem ACID
*  menor complexidade

---

##  API lendo direto do Data Lake

Escolha: evitar banco adicional

Trade-off:

*  latência maior
*  menos custo e infraestrutura

---

##  Small Files Handling

Implementado com:

* coalesce no Spark
* monitoramento de arquivos

Benefício:

* redução de custo no Athena
* melhor performance

---

#  Observabilidade

* Métricas Prometheus (`/metrics`)
* Logging estruturado
* Monitoramento de small files

---

#  Alertas

* Fail rate > 15%
* Pipeline > 7200s
* Streaming lag > 300s
* Small files por partição

---

#  Estimativa de Custo AWS

| Serviço           | Estimativa |
| ----------------- | ---------- |
| S3 (100GB)        | ~$2.30     |
| Athena (1TB scan) | ~$5.00     |
| Glue/EMR          | ~$30       |
| Transferência     | ~$5        |

##  Maior risco

Athena → custo baseado em dados escaneados

---

#  Otimizações de Custo

* Parquet + particionamento
* Lifecycle S3
* Spot Instances
* Compaction de arquivos

---

#  Limitações

* Não utiliza Delta Lake
* Não possui cache na API
* Pipeline não distribuído
* Terraform simplificado

---

#  Melhorias Futuras

* Delta Lake
* Redis cache
* Deploy em Kubernetes
* CI/CD
* Data Quality checks

---

#  Governança

Veja detalhes em:

 [governance.md](./governance.md)

---

#  Autor

Hugo Souza
