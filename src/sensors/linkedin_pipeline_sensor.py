from mage_ai.orchestration.run_status_checker import check_status

if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor
from src.configs.configs import get_config

@sensor
def check_condition(*args, **kwargs) -> bool:
    return check_status(
        get_config('pipelines', 'linkedin.uuid'),
        kwargs['execution_date'],
    )