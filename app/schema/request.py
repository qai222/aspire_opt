from datetime import datetime
from typing import Literal, Any

import pandas as pd
from pydantic import BaseModel, validator, root_validator

_eps = 1e-6


class OptimizationRequest(BaseModel):
    """ an optimization request sent to the service """

    identifier: str
    """ string identifier for the request """

    datetime: datetime
    """ datetime when creating and sending this request  """

    continuous_parameter_space: dict[str, tuple[float, float]]
    """ 
    a dictionary of `dict[<parameter_name>, (<min>, <max>)]` 
    that defines the limits for the continuous parameter `<parameter_name>`
    """

    categorical_parameter_space: dict[str, set[str]]
    """ 
    a dictionary of `dict[<parameter_name>, {choice_1, choice_2, ...}]` 
    that defines the domain for the categorical parameter `<parameter_name>`
    """

    target_names: list[str]
    """ a list of <parameter_name> that will be optimized """

    observations: list[dict[str, Any]]
    """ 
    a list of observations, an observation is just a mapping of <parameter_name> -> <parameter_value>,
    note targets are also considered as parameters
    """

    optimize_goal: Literal['minimize', 'maximize']
    """ optimization direction """

    @validator('continuous_parameter_space')
    def validate_co_ps(cls, co_ps):
        for k, v in co_ps.items():
            if not v[0] < v[1] - _eps:
                raise ValueError(f"parameter space of {k} is too small: {v}")
        return co_ps

    @validator('categorical_parameter_space')
    def validate_ca_ps(cls, ca_ps):
        for k, v in ca_ps.items():
            if len(v) < 1:
                raise ValueError(f"parameter space of {k} is too small: {v}")
        return ca_ps

    @root_validator
    def validate_all(cls, values):
        records = values['observations']
        df = pd.DataFrame.from_records(records)
        observation_params = set(df.columns)

        known_params = set()
        for k in values['continuous_parameter_space']:
            known_params.add(k)
        for k in values['categorical_parameter_space']:
            known_params.add(k)

        target_params = set(values['target_names'])

        if not observation_params.issuperset(known_params):
            raise ValueError(f'params not in observations: {known_params.difference(observation_params)}')

        if not observation_params.issuperset(target_params):
            raise ValueError(f'targets not in observations: {target_params.difference(observation_params)}')
        return values
