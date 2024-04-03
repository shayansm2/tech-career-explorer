import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from src.crawlers.GlassdoorCrawler import GlassdoorCrawler
from src.crawlers.GlassdoorCrawlerInputs import GlassdoorCrawlerInputs
from src.configs.configs import get_config


@data_loader
def load_data_from_api(*args, **kwargs):
    inputs = GlassdoorCrawlerInputs(keyword=kwargs['keyword'], location=kwargs['location'])
    dfs = []
    max_retries = get_config('crawlers', 'glassdoor.max_retries')
    for page in range(get_config('crawlers', 'glassdoor.max_page')):
        inputs.set_page(page+1)
        retries = 0
        need_retry = True
        while retries < max_retries and need_retry:
            try:
                need_retry = False
                print(f"getting page {page+1} data")
                df = GlassdoorCrawler().scrape_listing_data(inputs)
                print(f"found {len(df)} results in page {page+1}")
            except requests.Timeout:
                print(f"time out page {page+1}")
                need_retry = True
                retries += 1
        
        if len(df) == 0:
            break
        dfs.append(df)
    return pd.concat(dfs)


@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'
    assert len(output[output['job_title'].isnull()]) == 0
    assert len(output[output['company_name'].isnull()]) == 0
    assert len(output[output['detail_page_uri'].isnull()]) == 0
