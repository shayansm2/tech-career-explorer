select
    {{ 
        dbt_utils.generate_surrogate_key(['job_title', 'company_name']) 
    }} as job_id,
    hash_id as position_id,
    job_title,
    company_name,
    city,
    country,
    concat('https://relocate.me', detail_page_uri) as page_url,

    relocation_package,
    remote_option,
    tags
from {{ source('staging', 'relocate_job_positions') }}