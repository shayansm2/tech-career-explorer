import requests
from bs4 import BeautifulSoup
import pandas as pd
import orchestrator.schema.positions as schema

def scrape_data_from_listing_url(url) -> pd.DataFrame:
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
