import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import src.schema.positions as schema
import src.schema.details as details_schema

def scrape_listing_data(url: str) -> pd.DataFrame:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = soup.find_all('div', class_= 'jobs-list__job')
    data = []

    for job in jobs:
        row = {}
        job_info = job.find('a')
        row[schema.column_detail_page_uri] = job.find('a')['href']
        job_info = job_info.text.split("\n")
        row[schema.column_job_title] = job_info[0].strip()
        
        if len(job_info) > 1 and job_info[1] != "":
            locations = job_info[1][3:].split(",")
            if len(locations) > 1:
                row[schema.column_city] = locations[0].strip()
                row[schema.column_country] = locations[1].strip()
            else:
                row[schema.column_country] = locations[0].strip()
        
        relocation_package = job.find_all('div', class_= 'job__package job__package_advanced with-tooltip')
        if len(relocation_package) > 0:
            row[schema.column_relocation_package] = job.find_all('div', class_= 'job__package job__package_advanced with-tooltip')[0].text.strip()
        
        company_data = job.find_all('div', class_ = 'job__company')
        row[schema.column_company_name] = company_data[0].text.strip()
        if len(company_data) > 1:
            row[schema.column_remote_option] = company_data[1].text.strip()
        
        row[schema.column_tags] = list(map(lambda x: x.text.strip(), job.find_all('span', class_= 'job__tag')))
        
        data.append(row)
    
    df = pd.DataFrame(data)
    return df


def scrape_detail_data(url: str) -> dict:
    result = {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    desc_items = soup.find_all('div', {'class': 'job-info__description-item'})
    desc_items = list(map(lambda x: x.text.strip(), desc_items))
    desc = re.sub(' +', ' ', '\n'.join(desc_items).strip().replace('\n', ' '))
    result[details_schema.column_job_description] = desc

    relocation_package_items = soup.find_all('div', {'class': 'relocation-packages__item'})
    relocation_package_items = list(map(lambda x: x.text.strip(), relocation_package_items))
    result[details_schema.column_relocation_package_options] = relocation_package_items

    job_tags = soup.find_all('a', {'class': 'job__tag'})
    job_tags = list(map(lambda x: x.text.strip(), job_tags))
    result[details_schema.column_tags] = job_tags

    return result