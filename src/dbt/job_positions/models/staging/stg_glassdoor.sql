select
    {{ 
        dbt_utils.generate_surrogate_key(['job_title', 'company_name']) 
    }} as job_id,
    hash_id as position_id,
    job_title,
    company_name,
    city,
    country,
    concat('https://www.glassdoor.com', detail_page_uri) as page_url,
    'glassdoor' as source,

    created_at,
    job_type,
    rating,
    pay_currency,
    pay_period

from {{ source('staging', 'glassdoor_job_positions') }}