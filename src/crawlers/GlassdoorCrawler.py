import tls_client
import re
import os
import requests
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key

from src.crawlers.GlassdoorCrawlerInputs import GlassdorrCrawlerInputs
import src.schema.positions as schema
from src.configs.configs import get_config

class GlassdorrCrawler(object):
    def __init__(self) -> None:
        self.url = 'https://www.glassdoor.com/graph'
        self.base_url = 'https://www.glassdoor.com'

    def scrape_listing_data(self, inputs: GlassdorrCrawlerInputs): 
        response = requests.post(
            self.url,
            headers=self.get_headers(),
            json=self.get_listing_body(inputs),
            timeout=get_config('crawlers', 'glassdoor.timeout_time')
        )

        data = response.json()[0]['data']['jobListings']['jobListings']
        return pd.DataFrame(list(map(self.extract_fields, data)))

    def get_headers(self):
        headers = {
            'authority': 'www.glassdoor.com',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'apollographql-client-name': 'job-search-next',
            'apollographql-client-version': '7.15.4',
            'content-type': 'application/json',
            'origin': self.base_url,
            'referer': self.base_url,
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'x-gd-job-page': 'serp',
        }

        headers['gd-csrf-token'] = self.get_csrf_token(headers)
        return headers

    def get_csrf_token(self, headers):
        load_dotenv()
        date = os.getenv("GLASSDOOR_CSRF_TOKEN_DATE")
        token = os.getenv("GLASSDOOR_CSRF_TOKEN_VALUE")
        current_date = datetime.now().date().isoformat()

        if date == current_date and token is not None:
            return token
        else:
            token = self._get_csrf_token(headers)
            set_key(".env", "GLASSDOOR_CSRF_TOKEN_DATE", current_date)
            set_key(".env", "GLASSDOOR_CSRF_TOKEN_VALUE", token)
            return token

    def _get_csrf_token(self, headers):
        session = tls_client.Session(random_tls_extension_order=True)
        res = session.get(
            f"{self.base_url}/Job/computer-science-jobs.htm", headers=headers
        )
        pattern = r'"token":\s*"([^"]+)"'
        matches = re.findall(pattern, res.text)
        token = None
        if matches:
            token = matches[0]
        return token

    def get_listing_body(self, inputs: GlassdorrCrawlerInputs):
        with open('./src/crawlers/glassdorrQuery.graphql', 'r') as file:
            query = file.read()

        result = [{
            'operationName': 'JobSearchResultsQuery',
            'variables': {
                'keyword': inputs.keyword,
                'locationId': inputs.location_id,
                'locationType': inputs.location_type,
                'numJobsToShow': 30, # should be 30 always
                'parameterUrlInput': f"IL.0,12_I{inputs.location_type}{inputs.location_id}",
                'pageType': 'SERP',
                'seoUrl': True,
                'pageNumber': inputs.page,
                "fromage": inputs.age,
                "sort": "date",
            },
            'query': query,
        }]

        if inputs.age:
            result['variables']['filterParams'] = [{"filterKey": "fromAge", "values": str(inputs.age)}]

        return result
    
    @staticmethod
    def extract_fields(data: dict) -> dict:
        data = data['jobview']['header']
        result = {
            schema.column_job_type: data['normalizedJobTitle'],
            schema.column_job_title: data['jobTitleText'],
            schema.column_company_name: data['employerNameFromSearch'],
            schema.column_detail_page_uri: urlparse(data['seoJobLink']).path,
            schema.column_created_at: (datetime.now() - timedelta(days=data['ageInDays'])).strftime('%Y-%m-%d'),
            schema.column_rating: data['rating'],
            schema.column_pay_currency: data['payCurrency'],
            schema.column_pay_period: data['payPeriod'],
        }

        if data['locationType'] == 'C':
            result[schema.column_city] = data['locationName']
        elif data['locationType'] == 'N':
            result[schema.column_country] = data['locationName']
        elif data['locationType'] == 'S':
            result[schema.column_country] = 'remote'
            result[schema.column_city] = 'remote'

        return result