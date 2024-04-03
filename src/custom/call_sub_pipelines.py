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

    json_data = {
        'pipeline_run': {
            'variables': {
                'keyword': 'backend',
                'geo_id': 102890719,
            },
        },
    }

    url = get_config('apis', 'linkedin_pipeline.url')
    uri = get_config('apis', 'linkedin_pipeline.uri')
    requests.post(
        f'{url}{uri}',
        headers=headers,
        json=json_data,
    )

    return {}