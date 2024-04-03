from mage_ai.orchestration.run_status_checker import check_status
from src.configs.configs import get_config
from src.utils.decorators import check_till_true

@check_till_true
def check_condition(*args, **kwargs) -> bool:
    return check_status(
        get_config('pipelines', 'relocate.uuid'),
        kwargs['execution_date'],
    )