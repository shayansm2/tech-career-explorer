import requests
from src.crawlers.GlassdoorCrawlerInputs import GlassdorrCrawlerInputs
import src.schema.positions as schema
from urllib.parse import urlparse
from datetime import datetime, timedelta
import pandas as pd

class GlassdorrCrawler(object):
    def __init__(self) -> None:
        self.url = 'https://www.glassdoor.com/graph'
        self.site_url = 'https://www.glassdoor.com'
        self.csrf_token = self._get_csrf_token()

    def scrape_listing_data(self, inputs: GlassdorrCrawlerInputs): 
        response = requests.post(
            self.url,
            headers=self.get_headers(),
            json=self.get_listing_body(inputs)
        )

        data = response.json()[0]['data']['jobListings']['jobListings']
        return pd.DataFrame(list(map(self.extract_fields, data)))

    # todo check with jobspy    
    def get_headers(self):
        return {
                'authority': 'www.glassdoor.com',
                'accept': '*/*',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'apollographql-client-name': 'job-search-next',
                'apollographql-client-version': '7.15.4',
                'content-type': 'application/json',
                'gd-csrf-token': self.csrf_token,
                'origin': self.site_url,
                'referer': self.site_url,
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'x-gd-job-page': 'serp',
        }
        
    # todo check with jobspy
    @staticmethod
    def _get_csrf_token():
        return 'jO-6yIPii6CFGzwsNOikVQ:WJ9XlupTFHEOHu7bC25GRDY_6CoZgPAtrXOn-sIcbIeAwWxsVWOfL-a0QbZ336OAvJ2qroRASrf451akuYaT3g:CiYwBOV-Bd-dNAMIA4d8anUb2iqmJIJ1R9jaRH_qP_A'
    
    ## todo check with jobspy
    def get_listing_body(self, inputs: GlassdorrCrawlerInputs):
        with open('./src/crawlers/glassdorrQuery.graphql', 'r') as file:
            query = file.read()

        return [{
            'operationName': 'JobSearchResultsQuery',
            'variables': {
                'keyword': inputs.keyword,
                'locationId': inputs.location_id,
                'locationType': inputs.location_type,
                'numJobsToShow': 30, # should be 30 always
                'parameterUrlInput': 'IL.0,11_IN178_KO12,29', ## todo check with jobspy
                'pageType': 'SERP',
                'seoFriendlyUrlInput': 'netherlands-software-engineer-jobs', ## todo check with jobspy
                'seoUrl': True,
                'pageNumber': inputs.page
            },
            'query': query,
        }]
    
    @staticmethod
    def extract_fields(data: dict) -> dict:
        data = data['jobview']['header']
        result = {
            schema.column_job_title: data['normalizedJobTitle'],
            'desc': data['jobTitleText'],
            schema.column_company_name: data['employerNameFromSearch'],
            schema.column_detail_page_uri: urlparse(data['seoJobLink']).path,
            schema.column_created_at: (datetime.now() - timedelta(days=data['ageInDays'])).strftime('%Y-%m-%d'),
            'rating': data['rating'],
            'pay_currency': data['payCurrency'],
        }

        if data['locationType'] == 'C':
            result[schema.column_city] = data['locationName']
        elif data['locationType'] == 'N':
            result[schema.column_country] = data['locationName']

        return result