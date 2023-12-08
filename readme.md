# ASPIRE Empirical Optimization API

Interface to empirical optimizers for reaction condition optimization.

### Deployment

```bash
docker compose up
```

### Optimizer
- OLYMPUS: https://github.com/aspuru-guzik-group/olympus
- Summit: https://github.com/sustainable-processes/summit

# API examples
Input
```json
{
  "identifier": "example_olympus",
  "continuous_parameter_space": {
    "temperature": [75, 90],
    "pd_mol": [0.5, 5],
    "arbpin": [1, 1.8],
    "k3po4": [1.5, 3]
  },
  "categorical_parameter_space": {},
  "target_names": [
    "yield"
  ],
  "observations": [
    {"temperature": 75, "pd_mol": 0.5, "arbpin": 1, "k3po4": 1.5, "yield": 2.4},
    {"temperature": 75, "pd_mol": 0.5, "arbpin": 1.2, "k3po4": 1.5, "yield": 4.6}

  ],
  "optimize_goal": "maximize",
  "planner_name": "ConjugateGradient"
}
```
Output
```json
{
  "arbpin": 1.6015094769562883, "k3po4": 2.9960569094796194, 
  "pd_mol": 4.371576658109785, "temperature": 85.93353741155443
}
```

# Benchmark reaction datasets

Access to the following reaction datasets is provided.

| DOI                        | Description       | Parameters               | Target | # of reactions |
|----------------------------|-------------------|--------------------------|--------|----------------|
| 10.1126/science.aap9112    | Suzuki-Miyaura    | Categorical + Continuous | Yield  | 5280           |
| 10.1126/science.aar5169    | Buchwald-Hartwig  | Categorical              | Yield  | 4132           |
| 10.1021/jacs.8b01523       | Deoxyfluorination | Categorical              | Yield  | 80             |
| 10.1021/acscatal.0c02247   | Dehalogenation    | Categorical              | Yield  | 1152           |
| 10.1038/s41586-021-03213-y | Arylation         | Categorical + Continuous | Yield  | 1728           |

After downloading them to [the correct folder](app/reaction_datasets/download) using [download.py](app/reaction_datasets/download/download.py),
all datasets can be accessed as `BenchmarkDataframe` objects:
```python
from reaction_datasets import BenchmarkDataframe

dehalogenation_dataset = BenchmarkDataframe.ds_3()
```
An example using [Summit](https://github.com/sustainable-processes/summit) for benchmarking can be found in [this notebook](benchmark/benchmark_summit.ipynb)