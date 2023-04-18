import importlib

import pandas as pd
from summit import Domain, ContinuousVariable, CategoricalVariable, DataSet

from schema import OptimizationRequestSummit


def optimize_summit(request: OptimizationRequestSummit):
    domain = Domain()
    features = []

    for feature, lims in request.continuous_parameter_space.items():
        features.append(feature)
        domain += ContinuousVariable(name=feature, bounds=list(lims), description=feature)

    for feature, levels in request.categorical_parameter_space.items():
        features.append(feature)
        domain += CategoricalVariable(name=feature, levels=levels, description=feature)

    for tn in request.target_names:
        domain += ContinuousVariable(
            name=tn,
            is_objective=True,
            maximize=request.optimize_goal == 'maximize',
            description='tn',
            bounds=list(request.target_bounds[tn]),
        )

    df = pd.DataFrame.from_records(request.observations)
    dataset = DataSet.from_df(df[features + request.target_names])
    strategy = getattr(importlib.import_module('summit.strategies'), request.strategy)
    suggestions = strategy(domain=domain).suggest_experiments(1, prev_res=dataset)
    suggestions: DataSet
    df = pd.DataFrame(data=suggestions.data_to_numpy(), columns=suggestions.data_columns)
    return df.to_dict(orient="records")[0]
