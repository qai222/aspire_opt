from fastapi import FastAPI

from schema import OptimizationRequestOlympus, OptimizationRequestSummit
from service import optimize_summit, optimize_olympus

app = FastAPI(
    title="ASPIRE Empirical Optimization",
    contact={"Qianxiang Ai": "qai@mit.edu"},
)


@app.get('/')
async def index():
    return {"connect": "1"}


@app.post('/olympus/', summary="endpoint for OLYMPUS")
async def olympus(req: OptimizationRequestOlympus, ):
    """
    Request an OLYMPUS optimization:
    """
    recommendation = optimize_olympus(req)
    return recommendation


@app.post('/summit/', summary="endpoint for SUMMIT")
def summit(req: OptimizationRequestSummit):
    """
    Request an SUMMIT optimization:
    """
    recommendation = optimize_summit(req)
    return recommendation
