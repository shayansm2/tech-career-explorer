import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from src.crawlers.LinkedinCrawler import scrape_detail_data

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    df = args[0][['hash_id', 'detail_page_uri']]
    
    df['detail_page_url'] = df['detail_page_uri'] \
        .apply(lambda x: 'https://www.linkedin.com/' + x)
    
    new_columns = df['detail_page_url'] \
        .apply(scrape_detail_data) \
        .apply(pd.Series)
    
    df = pd.concat([df, new_columns], axis=1)
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
