import pandas as pd
from src.crawlers.GlassdoorCrawler import GlassdoorCrawler

def load_data_from_api(*args, **kwargs):
    crawler = GlassdoorCrawler().scrape_detail_data

    df = args[0][['hash_id', 'detail_page_uri']]

    df.loc[:, 'detail_page_url'] = df['detail_page_uri'] \
        .apply(lambda x: 'https://www.glassdoor.com' + x)

    columns = df['detail_page_url'] \
        .apply(crawler) \
        .apply(pd.Series)
    df = pd.concat([df, columns], axis=1)
    return df

def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'