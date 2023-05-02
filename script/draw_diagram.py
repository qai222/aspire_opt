import erdantic as erd

from schema import RecommendationRequest

erd.draw(RecommendationRequest, out="diagram.eps")
erd.draw(RecommendationRequest, out="diagram.png")
