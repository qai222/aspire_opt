import pandas as pd
from loguru import logger
from olympus import ParameterSpace, Parameter, Observations
from olympus.objects.object_parameter_vector import ObjectParameterVector
from olympus.planners import PlannerLoader
from olympus.planners.planner import Planner

from schema.request_olympus import OptimizationRequestOlympus
from schema.utils import import_string


def _load_planner_from_name(planner_name: str):
    planner_file = PlannerLoader.class_to_file(planner_name)
    planner_path = f'olympus.planners.planner_{planner_file}.{planner_name}'
    return import_string(planner_path)


def optimize_olympus(request: OptimizationRequestOlympus):
    planner_name = request.planner_name.value
    planner_class = _load_planner_from_name(planner_name)
    if request.return_docs:
        return planner_class.__init__.__doc__

    df = pd.DataFrame.from_records(request.observations)
    features = []
    param_space = ParameterSpace()

    for feature, lims in request.continuous_parameter_space.items():
        p = Parameter(kind='continuous', name=feature, low=lims[0], high=lims[1])
        param_space.add(p)
        features.append(feature)

    for feature in request.categorical_parameter_space:
        logger.critical(f"categorical parameter is not supported by olympus now, the feature is ignored: {feature}")

    observations = Observations()
    observations.params = df[features].values
    observations.values = df[request.target_names].values
    observations.param_space = param_space
    observations.value_space = None

    if request.use_default:
        planner = Planner(kind=planner_name, goal=request.optimize_goal, param_space=param_space)
    else:
        planner = planner_class(**request.planner_kwargs)
        planner.set_param_space(param_space)
    parameter_vector = planner.recommend(observations=observations)
    parameter_vector: ObjectParameterVector
    return parameter_vector.to_dict()  # , planner.to_dict()
