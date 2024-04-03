if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import src.schema.details as schema


@transformer
def transform(data, *args, **kwargs):
    data.drop(
        [schema.column_job_description, 'detail_page_url', 'detail_page_uri'],
        axis=1,
        inplace=True
    )

    print(data.columns)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'