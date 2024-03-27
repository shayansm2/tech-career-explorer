import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

from src.data_loaders.crawl_glassdoor_details import load_data_from_api

def execute():
    db = init()
    df = e_from_extract(db)
    df = t_from_transform(df)
    # l_from_load(df, db)


def init():
    load_dotenv()

    db_username = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DBNAME')

    db = create_engine(f'postgresql://{db_username}:{db_password}@localhost:5432/{db_name}')
    return db

def e_from_extract(db):
    tbl_name = 'public.glassdoor_job_positions_stage'
    df = pd.read_sql(f'SELECT * FROM {tbl_name}', db)
    db.execute(f"DROP TABLE IF EXISTS {tbl_name}")
    return df

def t_from_transform(df):
    df = crawl_details(df)
    print(df)
    # perform_cleanup()

def crawl_details(df):
    return load_data_from_api([df])

def l_from_load(df, db):
    df.to_sql('glassdoor_job_position_details', db, if_exists='replace')

if __name__ == "__main__":
    execute()