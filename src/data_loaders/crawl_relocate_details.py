import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from src.crawlers.RelocateCrawler import scrape_detail_data

@data_loader
def load_data_from_api(*args, **kwargs):
    df = args[0][['detail_page_uri', 'hash_id']]

    df.loc[:, 'detail_page_url'] = df['detail_page_uri'] \
        .apply(lambda x: 'https://relocate.me' + x)

    columns = df['detail_page_url'] \
        .apply(scrape_detail_data) \
        .apply(pd.Series)
    df = pd.concat([df, columns], axis=1)
    return df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'