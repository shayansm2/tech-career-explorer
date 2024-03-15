import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


from orchestrator.crawlers.RelocateCrawler import scrape_data_from_url
from orchestrator.utils.hash import create_hash_id

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    dfs = []
    page_number = 0
    while True:
        page_number+=1
        url = f'https://relocate.me/search?page={page_number}'
        print(f'crawling page {page_number}')
        df = scrape_data_from_url(url)
        print(f'page {page_number} crawled')
        if len(df) == 0:
            break
        dfs.append(df)

    result = pd.concat(dfs)
    result['hash_id'] = result.apply(lambda x: create_hash_id(x), axis=1)
    result['data_source'] = 'relocate.me'
    return result


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert len(output[output['detail_page_url'].isnull()]) == 0
    assert len(output[output['job_title'].isnull()]) == 0
    assert len(output[output['company_name'].isnull()]) == 0
    assert len(output[output['hash_id'].isnull()]) == 0
