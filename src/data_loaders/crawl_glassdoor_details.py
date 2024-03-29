import pandas as pd
from src.crawlers.GlassdoorCrawler import GlassdoorCrawler
from src.configs.configs import get_config
import src.schema.details as schema
import time

def load_data_from_api(*args, **kwargs):
    crawler = GlassdoorCrawler().scrape_detail_data

    df = args[0][['hash_id', 'detail_page_uri']]

    df.loc[:, 'detail_page_url'] = df['detail_page_uri'] \
        .apply(lambda x: 'https://www.glassdoor.com' + x)

    columns = df['detail_page_url'] \
        .apply(crawler) \
        .apply(pd.Series)
    
    retries = 0
    max_retries = get_config('crawlers', 'glassdoor.max_retries')
    sleep_time = get_config('crawlers', 'glassdoor.sleep_time')

    while len(columns[columns[schema.column_job_description].isnull()]) > 0 and retries <= max_retries:
        time.sleep(sleep_time)
        retries += 1
        print('number of missing rows:', len(columns[columns[schema.column_job_description].isnull()]))
        print(f'retry number {retries}')

        missing_data = columns[schema.column_job_description].isnull()
        new_columns = columns.loc[missing_data, 'url'] \
            .apply(crawler) \
            .apply(pd.Series)
        
        print(new_columns)
        
        for col in new_columns.columns:
            columns.loc[missing_data, col] = new_columns[col]

    df = pd.concat([df, columns], axis=1)
    return df

def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'