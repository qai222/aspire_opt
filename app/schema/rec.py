from datetime import datetime
from typing import Literal, Union

import pandas as pd
from pydantic import BaseModel

from schema.base import Domain, suzuki_data, _domain_suzuki, suzuki_config
from schema.optimizer import OptimizerOlympus, OptimizerSummit, _suzuki_optimizer_olympus, _suzuki_optimizer_summit


def _suzuki_request_olympus():
    domain = _domain_suzuki()
    params = suzuki_config['parameters']
    df = pd.DataFrame(suzuki_data[:5], columns=[p['name'] for p in params] + ['yield', ])
    df.rename(columns={"yield": "yld"}, inplace=True)
    req = {
        "identifier": "example_suzuki_olympus",
        "number_of_recommendations": 1,
        "datetime": datetime.now(),
        "domain": domain,
        "observations": df.to_dict(orient="records"),
        "optimize_goal": 'maximize',
        "optimizer": _suzuki_optimizer_olympus,
    }
    return req


def _suzuki_request_summit():
    domain = _domain_suzuki()
    params = suzuki_config['parameters']
    df = pd.DataFrame(suzuki_data[:5], columns=[p['name'] for p in params] + ['yield', ])
    df.rename(columns={"yield": "yld"}, inplace=True)
    req = {
        "identifier": "example_suzuki_summit",
        "number_of_recommendations": 1,
        "datetime": datetime.now(),
        "domain": domain,
        "observations": df.to_dict(orient="records"),
        "optimize_goal": 'maximize',
        "optimizer": _suzuki_optimizer_summit,
    }
    return req


class RecommendationRequest(BaseModel):
    """ an optimization request sent to the service """

    identifier: str
    """ string identifier for the request """

    number_of_recommendations: int
    """ how many recommendations? """

    datetime: datetime
    """ datetime when creating and sending this request  """

    domain: Domain

    observations: list[dict[str, Union[float, str]]]  # https://github.com/pydantic/pydantic/issues/1599
    """ 
    a list of observations, an observation is just a mapping of <parameter_name> -> <parameter_value>,
    """

    optimize_goal: Literal['minimize', 'maximize']
    """ optimization direction """

    optimizer: Union[OptimizerSummit, OptimizerOlympus]


class RecommendationResponse(BaseModel):
    recommendation: list[dict[str, Union[str, float]]]
