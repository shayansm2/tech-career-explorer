select
    {{ 
        dbt_utils.generate_surrogate_key(['job_title', 'company_name']) 
    }} as job_id,
    hash_id as position_id,
    job_title,
    company_name,
    city,
    country,
    created_at,
    concat('https://linkedin.com', detail_page_uri) as page_url
from {{ source('staging', 'linkedin_job_positions') }}