from typing import Union

from olympus.datasets import load_dataset
from pydantic import BaseModel, validator

suzuki_data, suzuki_config, _ = load_dataset("suzuki")
_eps = 1e-6


def _domain_suzuki():
    params = suzuki_config['parameters']
    domain = dict(continuous_parameters=[], categorical_parameters=[], target_parameters=[], )
    for p in params:
        param_obj = ContinuousParameter(name=p['name'], description=p['name'], is_target=False,
                                        bounds=(p['low'], p['high']))
        domain['continuous_parameters'].append(param_obj.dict())
    domain['target_parameters'].append(
        ContinuousParameter(
            name='yld', description='yld', is_target=True, bounds=(0, 1),
        ).dict()
    )
    return domain


# TODO ordinal parameter

class Parameter(BaseModel):
    name: str
    description: str
    unit: Union[str, None] = None
    is_target: bool = False

    class Config:
        frozen = True


class ContinuousParameter(Parameter):
    bounds: tuple[float, float]

    @validator('bounds')
    def validate_bounds(cls, bounds):
        mi, ma = bounds
        if not mi < ma - _eps:
            raise ValueError(f"parameter space is too small!")
        return bounds


class CategoricalParameter(Parameter):
    levels: list[str]

    @validator('levels')
    def validate_levels(cls, levels):
        if len(levels) != len(set(levels)):
            raise ValueError("duplicate levels!")
        if len(levels) < 2:
            raise validator("need at least two levels!")
        return levels


class Domain(BaseModel):
    continuous_parameters: list[ContinuousParameter]
    categorical_parameters: list[CategoricalParameter]
    target_parameters: list[ContinuousParameter]

    # TODO validate disjoint

    class Config:
        schema_extra = {
            "example": _domain_suzuki(),
        }
