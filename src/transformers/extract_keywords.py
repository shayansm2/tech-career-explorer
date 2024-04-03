if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import src.schema.details as schema
from src.configs.configs import get_config

@transformer
def transform(data, *args, **kwargs):
    for field, flags in get_config('keywords').items():
        data[field] = data[schema.column_job_description] \
            .apply(lambda x: get_flags(x, flags))

    return data


def get_flags(description: str, keywords: list):
    if description is None:
        return None
    result = [word for word in keywords if word.lower() in description.lower().split()]
    if len(result) == 0:
        return None
    return result

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert schema.column_job_description not in output.columns
