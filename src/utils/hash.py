import hashlib
import src.schema.positions as schema

def create_hash_id(row):
    return hashlib.md5((str(row[schema.column_job_title]) + str(row[schema.column_company_name])).encode()).hexdigest()