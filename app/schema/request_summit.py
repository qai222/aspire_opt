from datetime import datetime
from typing import Literal

import pandas as pd
from olympus.datasets import load_dataset

from .request import OptimizationRequest


def _suzuki():
    suzuki_data, suzuki_config, _ = load_dataset("suzuki")
    params = suzuki_config['parameters']
    continuous_parameter_space = {p['name']: (p['low'], p['high']) for p in params}
    df = pd.DataFrame(suzuki_data[:5], columns=[p['name'] for p in params] + ['yield', ])
    df.rename(columns={"yield": "YIE"}, inplace=True)  # summit doesn't like python keywords
    req = {
        "identifier": "example_olympus",
        "datetime": datetime.now(),
        "continuous_parameter_space": continuous_parameter_space,
        "categorical_parameter_space": dict(),
        "target_names": ['YIE', ],
        "observations": df.to_dict(orient="records"),
        "optimize_goal": 'maximize',
        "strategy": "STBO",
        "target_bounds": {"YIE": [0.1, 100]}
    }
    return req


class OptimizationRequestSummit(OptimizationRequest):
    """ request a Summit optimization """

    strategy: Literal[
        "STBO", "MTBO", "TSEMO", "GRYFFIN", "SOBO", "SNOBFIT", "NelderMead", "FullFactorial",
        "Random", "LHS", "DRO", "ENTMOOT",
    ]
    """ optimization strategy """

    target_bounds: dict[str, tuple[float, float]]
    """ target bounds for each target """

    class Config:
        schema_extra = {
            "example": _suzuki()
        }
