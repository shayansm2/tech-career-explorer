if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import requests
from src.configs.configs import get_config


@custom
def transform_custom(*args, **kwargs):
    headers = {
        'Content-Type': 'application/json',
    }

    url = get_config('pipelines', 'relocate.url')
    uri = get_config('pipelines', 'relocate.uri')
    response = requests.post(
        f'{url}{uri}',
        headers=headers,
    )

    return {
        'execution_date': response.json()['pipeline_run']['created_at']
    }