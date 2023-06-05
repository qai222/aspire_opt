import importlib

import olympus
import pandas as pd
import summit
from loguru import logger
from olympus.objects.object_parameter_vector import ObjectParameterVector as OlympusObjectParameterVector
from olympus.planners.planner import Planner as OlympusPlanner

from schema.base import Domain
from schema.rec import RecommendationRequest, OptimizerOlympus, RecommendationResponse, OptimizerSummit
from schema.utils import import_string


def _load_planner_from_name(planner_name: str):
    planner_file = olympus.planners.PlannerLoader.class_to_file(planner_name)
    planner_path = f'olympus.planners.planner_{planner_file}.{planner_name}'
    return import_string(planner_path)


def recommend_olympus(request: RecommendationRequest) -> RecommendationResponse:
    optimizer = request.optimizer
    domain = request.domain
    optimizer: OptimizerOlympus
    domain: Domain

    planner_name = optimizer.planner_name.value

    planner_class = _load_planner_from_name(planner_name)
    if optimizer.return_docs:
        return planner_class.__init__.__doc__
    df = pd.DataFrame.from_records(request.observations)
    features = []
    param_space = olympus.ParameterSpace()

    for p in domain.continuous_parameters:
        olympus_parameter = olympus.Parameter(kind='continuous', name=p.name, low=p.bounds[0], high=p.bounds[1])
        param_space.add(olympus_parameter)
        features.append(p.name)

    for p in domain.categorical_parameters:
        logger.critical(f"categorical parameter is not supported by olympus now, the feature is ignored: {p.name}")

    if len(domain.target_parameters) > 1:
        logger.critical(
            f"olympus does not allow multiple objectives, only this target will be optimized: {domain.target_parameters[0].name}")

    observations = olympus.Observations()
    observations.params = df[features].values
    observations.values = df[domain.target_parameters[0].name].values
    observations.param_space = param_space
    observations.value_space = None

    if optimizer.use_default:
        planner = OlympusPlanner(kind=planner_name, goal=request.optimize_goal, param_space=param_space)
    else:
        planner = planner_class(**optimizer.planner_kwargs)
        planner.set_param_space(param_space)
    parameter_vector = planner.recommend(observations=observations)
    parameter_vector: OlympusObjectParameterVector
    res = RecommendationResponse(
        recommendation=[parameter_vector.to_dict()]
    )
    return res


def recommend_summit(request: RecommendationRequest) -> RecommendationResponse:
    optimizer = request.optimizer
    domain = request.domain
    optimizer: OptimizerSummit
    domain: Domain

    summit_domain = summit.Domain()
    features = []

    for p in domain.continuous_parameters:
        summit_parameter = summit.ContinuousVariable(name=p.name, bounds=list(p.bounds), description=p.description)
        summit_domain += summit_parameter
        features.append(p.name)

    for p in domain.categorical_parameters:
        summit_parameter = summit.CategoricalVariable(name=p.name, levels=p.levels, description=p.description)
        summit_domain += summit_parameter
        features.append(p.name)

    target_names = []
    for p in domain.target_parameters:
        summit_parameter = summit.ContinuousVariable(
            name=p.name, bounds=list(p.bounds), description=p.description,
            is_objective=p.is_target, maximize=request.optimize_goal == 'maximize',
        )
        summit_domain += summit_parameter
        target_names.append(p.name)

    df = pd.DataFrame.from_records(request.observations)
    dataset = summit.DataSet.from_df(df[features + target_names])
    strategy = getattr(importlib.import_module('summit.strategies'), optimizer.strategy.value)
    suggestions = strategy(domain=summit_domain).suggest_experiments(request.number_of_recommendations, dataset)
    suggestions: summit.DataSet
    df = pd.DataFrame(data=suggestions.data_to_numpy(), columns=suggestions.data_columns)
    df = df[features]
    return RecommendationResponse(recommendation=df.to_dict(orient="records"))
