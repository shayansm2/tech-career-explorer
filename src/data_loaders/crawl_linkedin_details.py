import time
import pandas as pd
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from src.crawlers.LinkedinCrawler import scrape_detail_data
import src.schema.details as schema
from src.configs.configs import get_config

@data_loader
def load_data_from_api(*args, **kwargs):
    df = args[0][['hash_id', 'detail_page_uri']]
    
    df.loc[:, 'detail_page_url'] = df['detail_page_uri'] \
        .apply(lambda x: 'https://www.linkedin.com/' + x)
    
    columns = df['detail_page_url'] \
        .apply(scrape_detail_data) \
        .apply(pd.Series)
    
    max_retries = get_config('linkedin', 'max_retries')
    sleep_time = get_config('linkedin', 'sleep_time')
    retries = 0
    while len(columns[columns[schema.column_job_description].isnull()]) > 0 and retries <= max_retries:
        time.sleep(sleep_time)
        retries += 1
        print('number of missing rows:', len(columns[columns[schema.column_job_description].isnull()]))
        print(f'retry number {retries}')

        missing_data = columns[schema.column_job_description].isnull()
        new_columns = columns.loc[missing_data, 'url'] \
            .apply(scrape_detail_data) \
            .apply(pd.Series)
        
        for col in new_columns.columns:
            columns.loc[missing_data, col] = new_columns[col]
    
    df = pd.concat([df, columns], axis=1)
    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert len(output[output['detail_page_uri'].isnull()]) == 0
