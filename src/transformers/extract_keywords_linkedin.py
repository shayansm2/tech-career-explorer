import yaml
if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import src.schema.details as schema

@transformer
def transform(data, *args, **kwargs):
    with open('src/configs/keywords.yml', 'r') as file:
        keywords = yaml.safe_load(file)

    for field, flags in keywords.items():
        data[field] = data[schema.column_job_description] \
            .apply(lambda x: get_flags(x, flags))

    data.drop([schema.column_job_description, 'url'], axis=1, inplace=True)

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
