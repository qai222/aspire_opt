from typing import Annotated

from fastapi import FastAPI, Body

from schema import RecommendationRequest, RecommendationResponse
from schema.rec import _suzuki_request_olympus, _suzuki_request_summit
from service import recommend_olympus, recommend_summit

app = FastAPI(
    title="ASPIRE Empirical Optimization",
    contact={"Qianxiang Ai": "qai@mit.edu"},
)

endpoint_recommend_annotation_body = Body(
    examples={
        "summit": {
            "summary": "a summit recommendation request",
            "description": "a summit recommendation request",
            "value": _suzuki_request_summit(),
        },
        "olympus": {
            "summary": "an olympus recommendation request",
            "description": "an olympus recommendation request",
            "value": _suzuki_request_olympus(),
        }
    }

)


@app.get('/')
async def index():
    return {"connect": "1"}


@app.post('/recommend/', summary="endpoint for recommendation")
async def endpoint_recommend(req: Annotated[RecommendationRequest, endpoint_recommend_annotation_body]):
    # async def endpoint_recommend(req: RecommendationRequest):
    """
    Request an OLYMPUS optimization:
    """
    if req.optimizer.package == 'summit':
        rec = recommend_summit(req)
    elif req.optimizer.package == 'olympus':
        rec = recommend_olympus(req)
    else:
        rec = RecommendationResponse(recommendation=[{"error": f"unknown package requested: {req.optimizer.package}"}])
    return rec.dict()
