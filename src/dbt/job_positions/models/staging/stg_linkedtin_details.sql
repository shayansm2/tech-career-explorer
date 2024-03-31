select hash_id as position_id,
       seniority_level,
       employment_type,
       job_function,
       industries as industry,
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'languages') }},
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'tools') }},
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'frameworks') }},
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'libraries') }},
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'databases') }},
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'infra') }},
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'test') }},
       {{ select_column_if_exists(source('staging', 'linkedin_job_position_details'),   'job_roles') }}
from {{ source('staging', 'linkedin_job_position_details') }}
