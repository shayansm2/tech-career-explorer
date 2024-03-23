CREATE DATABASE tech_jobs;

USE tech_jobs;

CREATE TABLE public.glassdoor_job_positions
(
    hash_id         text    not null unique,
    job_title       text    not null,
    company_name    text    not null,
    job_type        text,
    city            text,
    country         text,
    created_at      date,
    detail_page_uri varchar not null unique,
    rating          float,
    pay_currency    text,
    pay_period      text
);


CREATE TABLE public.linkedin_job_positions
(
    hash_id         text    not null unique,
    job_title       text    not null,
    company_name    text    not null,
    city            text,
    country         text,
    created_at      date,
    detail_page_uri varchar not null unique
);


CREATE TABLE public.relocate_job_positions
(
    hash_id            text    not null unique,
    job_title          text    not null,
    company_name       text    not null,
    city               text,
    country            text,
    detail_page_uri    varchar not null unique,
    relocation_package text,
    remote_option      text,
    tags               text[]
);