from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
#import uvicorn
import logging

app = FastAPI()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metric
REQUEST_COUNTER = Counter('http_requests_total', 'Total HTTP Requests')


@app.get("/")
def read_root():
    logger.info("Root endpoint hit")
    REQUEST_COUNTER.inc()
    return {"status": "ok"}


@app.get("/healthz")
def health_check():
    return {"health": "ok"}


@app.get("/ready")
def readiness_check():
    return {"ready": "ok"}
