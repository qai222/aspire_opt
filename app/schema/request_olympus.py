from datetime import datetime
from enum import Enum
from typing import Any

import pandas as pd
from olympus.datasets import load_dataset
from olympus.planners import PlannerLoader

from .request import OptimizationRequest

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


def _suzuki(default=True):
    suzuki_data, suzuki_config, _ = load_dataset("suzuki")
    params = suzuki_config['parameters']
    continuous_parameter_space = {p['name']: (p['low'], p['high']) for p in params}
    df = pd.DataFrame(suzuki_data[:5], columns=[p['name'] for p in params] + ['yield', ])
    req = {
        "identifier": "example_olympus",
        "datetime": datetime.now(),
        "continuous_parameter_space": continuous_parameter_space,
        "categorical_parameter_space": dict(),
        "target_names": ['yield', ],
        "observations": df.to_dict(orient="records"),
        "optimize_goal": 'maximize',
        "planner_name": "ConjugateGradient",
        "return_docs": False,
    }
    if default:
        req['use_default'] = True
        req['planner_kwargs'] = dict()
    else:
        req['use_default'] = False
        req['planner_kwargs'] = dict(goal='minimize', gtol=1e-04)
    return req


class OptimizationRequestOlympus(OptimizationRequest):
    """
    request an olympus optimization
    """

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
            "example": _suzuki(False),
        }
        # TODO "examples" doesnt work...
