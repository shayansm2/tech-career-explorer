import requests
from bs4 import BeautifulSoup
import pandas as pd
import orchestrator.schema.positions as schema
# Make a GET request to the LinkedIn jobs page



def scrape_data_from_url(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')


    jobs = soup.find_all('div', {'class': 'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'})

    data = []
    for job in jobs:
        row = {}
        row[schema.column_detail_page_url] = job.find('a', {'class': 'base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]'})['href']
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
    
# scrape_data_from_url('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?geoId=102890719&keywords=software%20engineer&&start=0')
# scrape_data_from_url('https://www.linkedin.com/jobs/search?geoId=102890719&keywords=software%20engineer&position=1&pageNum=0')
# scrape_data_from_url('https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?geoId=102890719&keywords=software%20engineer&&start=70')