from fastapi import FastAPI
from api.routes import metrics, partners, transactions, events
import logging
from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Rentcars API")


Instrumentator().instrument(app).expose(app)

# rotas
app.include_router(metrics.router, prefix="/v1")
app.include_router(partners.router, prefix="/v1")
app.include_router(transactions.router, prefix="/v1")
app.include_router(events.router, prefix="/v1")

@app.get("/v1/health")
def health():
    logger.info("Health check chamado")
    return {"status": "ok"}