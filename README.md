# Rentcars Data Platform — Case Técnico (Senior Data Engineer)

---

## Visão Geral

Este projeto implementa uma plataforma de dados ponta-a-ponta baseada em arquitetura Lakehouse em camada Medalion, com ingestão via Spark, orquestração com Airflow e serving via API FastAPI.

O objetivo foi construir uma solução **simples, funcional e escalável**, priorizando:

* Entrega end-to-end
* Controle de custos (FinOps)
* Observabilidade
* Governança de dados

---

1. Arquitetura

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

2. Como rodar localmente (1 comando)

```bash
cd infra
docker-compose up --build
```

---

## Acessos

* Airflow: http://localhost:8080
* API Docs: http://localhost:8000/docs
* Métricas: http://localhost:8000/metrics

---

3. Estrutura do Projeto

```text
repo-case-de-rentcars/
├── pipeline/        # DAGs, ETL e métricas
├── api/             # FastAPI
├── infra/           # Docker + Terraform
├── observability/   # Métricas e alertas
├── governance.md    # Governança e FinOps
├── README.md
```

---

4. Decisões Técnicas

a) Arquitetura Lakehouse

* Uso de Parquet para reduzir custo e melhorar performance
* Separação em camadas: raw → silver → gold

> Trade-off:

* Simplicidade vs uso de Delta Lake (não implementado)

---

b)  Spark local ao invés de cluster distribuído

* Escolha feita para simplificar execução local

> Trade-off:

* Menor escalabilidade em produção

---

c) API lendo diretamente parquet

* Reduz latência de desenvolvimento

> Trade-off:

* Sem camada de cache ou banco analítico

---

d) Small Files Handling

* Uso de `coalesce` no Spark
* Métrica de contagem de arquivos

> Benefício:

* Redução de custo no Athena
* Melhor performance de leitura

---

5. Observabilidade

## API

* Métricas Prometheus (`/metrics`)
* Logging estruturado

## Pipeline

* Métricas derivadas de execução
* Monitoramento de small files

---

# Alertas

* Taxa de falha > 15%
* Tempo de pipeline > 7200s
* Streaming lag > 300s
* Small files por partição

---

6. Estimativa de Custo AWS (mensal)

| Componente            | Estimativa |
| --------------------- | ---------- |
| S3 (100GB)            | ~$2.30     |
| Athena (1TB scan/mês) | ~$5.00     |
| EMR/Glue              | ~$20–50    |
| Transferência         | ~$5        |

## Maior risco de custo:

Athena, devido ao volume de dados escaneados.

---

7. Estratégias de Otimização (FinOps)

* Parquet + particionamento → menos scan
* Lifecycle S3 (Standard → IA → Glacier)
* Spot Instances para batch
* Compactação de small files

---

8. Limitações Conhecidas

* Não utiliza Delta Lake
* Não possui cache na API
* Pipeline roda em modo local (não distribuído)
* Terraform simplificado (sem deploy completo)

---

9.  Melhorias Futuras

* Implementar Delta Lake
* Adicionar cache (Redis)
* Deploy em Kubernetes
* CI/CD pipeline
* Data Quality automatizada

---

10. Governança

Detalhes completos em:

> [governance.md](./governance.md)

Inclui:

* Data lineage
* Data contracts
* Segurança
* Backup e recuperação
* FinOps detalhado

---

11. Conclusão

A solução prioriza entrega end-to-end com foco em eficiência de custo e simplicidade, atendendo aos requisitos do desafio sem overengineering.

---

## Autor

Hugo Souza
Senior Data Engineer
