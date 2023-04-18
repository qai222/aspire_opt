from olympus.planners import PlannerLoader
from app.schema.utils import import_string
"""
use this to check additional dependencies for olympus
"""

for planner_name in PlannerLoader().list_planners():
    planner_file = PlannerLoader.class_to_file(planner_name)
    planner_path = f'olympus.planners.planner_{planner_file}.{planner_name}'
    o = import_string(planner_path)
    # failed to build Phoenics...
