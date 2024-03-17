if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from src.utils.hash import create_hash_id

@transformer
def transform(data, *args, **kwargs):
    data.drop_duplicates(inplace=True)
    data['hash_id'] = data.apply(lambda x: create_hash_id(x), axis=1)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
