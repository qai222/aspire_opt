import erdantic as erd

from schema import RecommendationRequest
from hardware_pydantic.junior.junior_devices import *

erd.draw(Instruction, out="dev.png")

# erd.draw(RecommendationRequest, out="diagram.eps")
# erd.draw(RecommendationRequest, out="diagram.png")
