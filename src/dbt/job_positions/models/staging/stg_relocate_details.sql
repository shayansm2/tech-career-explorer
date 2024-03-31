select hash_id as position_id,
       relocation_package_options,
       tags,
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'languages') }},
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'tools') }},
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'frameworks') }},
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'libraries') }},
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'databases') }},
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'infra') }},
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'test') }},
       {{ select_column_if_exists(source('staging', 'relocate_job_position_details'),   'job_roles') }}
from {{ source('staging', 'relocate_job_position_details') }}