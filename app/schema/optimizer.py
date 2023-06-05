from enum import Enum
from typing import Any
from typing import Literal

from olympus.planners import PlannerLoader
from pydantic import BaseModel

"""
TODO: test planner kwargs
TODO: multiple objectives
TODO: use pydantic models to set planner kwargs

Planners defined by `olympus.planners.planner.Planner` *function* to define planners can only have default settings.

OLYMPUS does not have in-code type hints for planner classes, they are in docstrings of `__init__`.
This makes `typing.get_type_hints` useless, but `inspect.signature` can still get `kwargs`.

```python
from olympus.planners import PlannerLoader
from schema.utils import import_string
for planner_name in PlannerLoader().list_planners():
    planner_file = PlannerLoader.class_to_file(planner_name)
    planner_path = f'olympus.planners.planner_{planner_file}.{planner_name}'
    o = import_string(planner_path)
    for p, pv in inspect.signature(o.__init__).parameters.items():
        print(p, pv, pv.name, pv.annotation)
    print(o.__init__.__doc__)
    break
```
"""

OlympusPlannerName = Enum(
    "OlympusPlannerKind",
    ((value, value) for value in PlannerLoader().list_planners()),
    type=str,
)

SummitStrategyName = Enum(
    "SummitStrategyChouce",
    ((value, value) for value in [
        "STBO", "MTBO", "TSEMO", "GRYFFIN", "SOBO", "SNOBFIT", "NelderMead",
        "FullFactorial", "Random", "LHS", "DRO", "ENTMOOT",
    ]),
    type=str,
)

_suzuki_optimizer_olympus = {
    "planner_name": "ConjugateGradient",
    "return_docs": False,
    "use_default": True,
    "planner_kwargs": dict(),
}

_suzuki_optimizer_summit = {
    "strategy": "STBO",
}


class OptimizerOlympus(BaseModel):
    """
    request an olympus optimization
    """

    package: str = 'olympus'

    planner_name: OlympusPlannerName
    """ planner basename """

    return_docs: bool = False
    """ if True, return docs about the planner only """

    use_default: bool = True
    """ if use the default settings """

    planner_kwargs: dict[str, Any]
    """ 
    kwargs passed to the planner, ignored if `use_default`,
    note this overwrites all planner related settings ex. `optimize_goal`
    """

    class Config:
        schema_extra = {
            "example": _suzuki_optimizer_olympus,
        }


class OptimizerSummit(BaseModel):
    """ request a Summit optimization """

    package: str = 'summit'

    strategy: SummitStrategyName
    """ optimization strategy """

    class Config:
        schema_extra = {
            "example": _suzuki_optimizer_summit,
        }
