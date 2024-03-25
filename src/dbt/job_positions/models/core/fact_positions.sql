select position_id,
       job_id,
       job_title,
       company_name,
       source,
       page_url,
       city,
       country
from {{ ref('stg_glassdoor')}}
union all
select position_id,
       job_id,
       job_title,
       company_name,
       source,
       page_url,
       city,
       country
from {{ ref('stg_linkedin')}}
union all
select position_id,
       job_id,
       job_title,
       company_name,
       source,
       page_url,
       city,
       country
from {{ ref('stg_relocate') }}