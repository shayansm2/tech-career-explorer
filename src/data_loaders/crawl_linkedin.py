import io
import pandas as pd
import requests
import time
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from src.crawlers.LinkedinUrlGenerator import LinkedinUrlGenerator
from src.crawlers.LinkedinCrawler import scrape_listing_data
from src.configs.configs import get_config

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url_generator = LinkedinUrlGenerator() \
        .set_geo_id(102890719) \
        .set_keywords('Software Engineer')

    offset = 0
    call_counter = 0
    retries = 0
    max_retries = get_config('crawlers', 'linkedin.max_retries')
    sleep_time = get_config('crawlers', 'linkedin.sleep_time')
    max_offset = get_config('crawlers', 'linkedin.max_offset')
    
    dfs = []
    while offset < max_offset:
        if call_counter % 10 == 0:
            time.sleep(sleep_time)
        print(f'get offset {offset}.')
        df = scrape_listing_data(url_generator.set_offset(offset).get())
        length = len(df)
        print(f'got {length} results.')
        if len(df) == 0:
            if retries == max_retries:
                break
            retries += 1
            time.sleep(sleep_time)
        dfs.append(df)
        offset += len(df)
        call_counter += 1
    
    return pd.concat(dfs)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert len(output[output['detail_page_uri'].isnull()]) == 0
    assert len(output[output['job_title'].isnull()]) == 0
    assert len(output[output['company_name'].isnull()]) == 0
