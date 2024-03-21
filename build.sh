#!/bin/bash

if [ ! -f ".env" ]; then
    touch .env
    echo POSTGRES_DBNAME=tech_jobs >> .env
    echo POSTGRES_SCHEMA=public >> .env
    echo POSTGRES_USER=user >> .env
    echo POSTGRES_PASSWORD=password >> .env
    echo POSTGRES_HOST=postgres >> .env
    echo POSTGRES_PORT=5432 >> .env
fi

docker-compose up --build