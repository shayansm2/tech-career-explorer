import tls_client
import re
import os
import requests
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime, timedelta
from dotenv import load_dotenv, set_key
from bs4 import BeautifulSoup
import subprocess
# from selenium import webdriver

from src.crawlers.GlassdoorCrawlerInputs import GlassdoorCrawlerInputs
import src.schema.positions as schema
import src.schema.details as details_schema
from src.configs.configs import get_config

class GlassdoorCrawler(object):
    def __init__(self) -> None:
        self.url = 'https://www.glassdoor.com/graph'
        self.base_url = 'https://www.glassdoor.com'

    def scrape_listing_data(self, inputs: GlassdoorCrawlerInputs): 
        response = requests.post(
            self.url,
            headers=self.get_headers(),
            json=self.get_listing_body(inputs),
            timeout=get_config('crawlers', 'glassdoor.timeout_time')
        )

        data = response.json()[0]['data']['jobListings']['jobListings']
        return pd.DataFrame(list(map(self.extract_fields, data)))
    
    # def _get_detail_soup_selenium(self, url):
    #     print('Initialize the WebDriver')
    #     options = webdriver.ChromeOptions()
    #     options.add_argument('headless')  # Run in headless mode

    #     print('Add headers')
    #     for key, value in self.get_detail_headers().items():
    #         options.add_argument(f'{key}={value}')

    #     driver = webdriver.Chrome(options=options)

    #     print('set time out')
    #     timeout=get_config('crawlers', 'glassdoor.timeout_time')
    #     driver.set_script_timeout(timeout)

    #     print('Load the page')
    #     driver.get(url)

    #     print('Get the page source and parse it with BeautifulSoup')
    #     soup = BeautifulSoup(driver.page_source, 'html.parser')

    #     print('Close the driver')
    #     driver.quit()

    #     return soup

    def _get_detail_soup_pip(self, url):
        print(url)
        timeout=get_config('crawlers', 'glassdoor.timeout_time')
        curl_command = f"curl -m {timeout} '{url}'"
        for key, value in self.get_detail_headers().items():
            curl_command += f" -H '{key}:{value}'"

        print(curl_command)
        process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, shell=True)
        response, _ = process.communicate()
        
        return BeautifulSoup(response, 'html.parser')

    def scrape_detail_data(self, url):
        soup = self._get_detail_soup_pip(url)

        desc = soup.find('div', {'class': 'JobDetails_jobDescriptionWrapper___tqxc JobDetails_jobDetailsSectionContainer__o_x6Z JobDetails_paddingTopReset__IIrci'}).text
        desc = re.sub(' +', ' ', desc.strip().replace('\n', ' '))

        salary_range = soup.find('div', {'class': 'SalaryEstimate_salaryRange__brHFy'})
        if salary_range:
            salary_range = salary_range.text.strip()

        company_info = {}
        for info in soup.find_all('div', {'class': 'JobDetails_overviewItem__cAsry'}):
            company_info[info.find('span').text.strip()] = info.find('div').text.strip()

        ratings = {}
        for info in soup.find_all('li', {'class': 'JobDetails_ratingItemContainer__BJoID'}):
            ratings[info.find('span').text.strip()] = info.find('div').text.strip()
        

        company_ratings = soup.find('ul', {'class': 'JobDetails_employerStatsDonuts__uWTLY'})
        if company_ratings:
            for info in company_ratings.find_all('li'):
                ratings[info.find('span').text.strip()] = info.find('div').text.strip()

        benefits = soup.find('div', {'class':'RatingHeadline_headline__scr7f'})
        if benefits:
            benefits = benefits.find('span')['aria-label']
            ratings['benefits'] = benefits

        return {
            details_schema.column_job_description: desc,
            details_schema.column_company_info: company_info,
            details_schema.column_company_ratings: ratings,
            'url': url,
        }

    
    # todo check liting headers with this
    def get_detail_headers(self):
        return {
            # todo check accpet all
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language' : 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control' : 'max-age=0',
            'sec-ch-ua' : '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile' : '?0', 
            'sec-ch-ua-platform' : '"macOS"',
            'sec-fetch-dest' : 'document',
            'sec-fetch-mode' : 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user' : '?1',
            'upgrade-insecure-requests' : '1',
            'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

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

    def get_listing_body(self, inputs: GlassdoorCrawlerInputs):
        with open('./src/crawlers/glassdoorQuery.graphql', 'r') as file:
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
        parsed_url = urlparse(data['seoJobLink'])
        result = {
            schema.column_job_type: data['normalizedJobTitle'],
            schema.column_job_title: data['jobTitleText'],
            schema.column_company_name: data['employerNameFromSearch'],
            schema.column_detail_page_uri: parsed_url.path + "?" + parsed_url.query,
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