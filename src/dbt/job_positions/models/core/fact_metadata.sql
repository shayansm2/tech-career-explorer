with linkedin_metadata as (
    select stg_linkedtin_details.*, stg_linkedin.created_at
    from {{ ref('stg_linkedin') }} as stg_linkedin
    full join {{ ref('stg_linkedin_details') }} as stg_linkedtin_details
    on stg_linkedin.position_id = stg_linkedtin_details.position_id
), 


relocate_metadata as (
    select stg_relocate_details.*,
        stg_relocate.relocation_package,
        stg_relocate.remote_option,
        stg_relocate.tags as listing_tags
    from {{ ref('stg_relocate') }} as stg_relocate
    full join {{ ref('stg_relocate_details') }} as stg_relocate_details
    on stg_relocate.position_id = stg_relocate_details.position_id
),

glassdoor_metadata as (
    select position_id,
       created_at,
       job_type,
       rating,
       pay_currency,
       pay_period,
       city
    from {{ ref('stg_glassdoor') }}
)

select position_id,
       relocation_package_options,
       array_cat(tags, listing_tags) as tags,
       languages,
       tools,
       frameworks,
       libraries,
       databases,
       infra,
       test::text,
       job_roles::text,
       relocation_package,
       remote_option,
       null                          as seniority_level,
       null                          as employment_type,
       null                          as job_function,
       null                          as industry,
       null                          as created_at,
       0                             as rating,
       null                          as pay_currency,
       null                          as pay_period
from relocate_metadata
union all
select position_id,
       null as relocation_package_options,
       null as tags,
       languages,
       tools,
       frameworks,
       libraries,
       databases,
       infra,
       test::text,
       job_roles::text,
       null as relocation_package,
       null as remote_option,
       seniority_level,
       employment_type,
       job_function,
       industry,
       created_at,
       0    as rating,
       null as pay_currency,
       null as pay_period
from linkedin_metadata
union all
select position_id,
       null                   as relocation_package_options,
       null                   as tags,
       null                   as languages,
       null                   as tools,
       null                   as frameworks,
       null                   as libraries,
       null                   as databases,
       null                   as infra,
       null                   as test,
       text(ARRAY [job_type]) as job_roles,
       null                   as relocation_package,
       CASE
           WHEN city = 'remote' THEN 'Remote'
           END                as remote_option,
       null                   as seniority_level,
       null                   as employment_type,
       null                   as job_function,
       null                   as industry,
       created_at,
       rating,
       pay_currency,
       pay_period
from glassdoor_metadata