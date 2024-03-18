import requests
from bs4 import BeautifulSoup
import pandas as pd
import src.schema.positions as schema
from urllib.parse import urlparse
import re


def scrape_listing_data(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all('div', {'class': 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'})

    data = []
    for job in jobs:
        row = {}
        job_url = job.find('a', {'class': 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})['href']
        row[schema.column_detail_page_uri] = urlparse(job_url).path
        row[schema.column_job_title] = job.find('h3', {'class': 'base-search-card__title'}).text.strip()
        row[schema.column_company_name] = job.find('h4', {'class': 'base-search-card__subtitle'}).text.strip()
        location = job.find('span', {'class': 'job-search-card__location'}).text.strip().split(",")
        row[schema.column_city] = location[0]
        row[schema.column_country] = location[-1]
        
        date = job.find('time', {'class': 'job-search-card__listdate'})
        if date is None:
            created_at = None
        else:
            created_at = date['datetime']
        row[schema.column_created_at] = created_at

        # todo fix this
        # salary = job.find('span', {'class': 'job-search-card__salary-info'})
        # if salary is not None:
        #     salary = salary.text
        # row[schema.column_salary_range] = salary

        data.append(row)
    df = pd.DataFrame(data)
    return df


def scrape_detail_data(url: str) -> dict:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # for debugging
    # with open(url, 'r') as html_file:
        # content = html_file.read()
    # soup = BeautifulSoup(content, 'html.parser')

    result = dict()

    job_description = soup .find('div', {'class': 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden'}) \
        
    if job_description is None:
        return result
    
    result['job_description'] = re.sub(' +', ' ', job_description.text.strip().replace('\n', ' '))

    for item in soup.find_all('li', {'class': 'description__job-criteria-item'}):
        field = item.find('h3').text.strip().lower().replace(' ', '_')
        value = item.find('span').text.strip()
        result[field] = value
    
    return result