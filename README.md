# tech-job-crawler

tools to use:
- postgres as data warehouse (production)
- duckdb as data warehouse (development)
- mage-ai as pipeline src
- DBT for ELT
- metabase for dashboard



![alt text](statics/de_zoomcamp_project_schema.png)

## todos:
- [x] build
    - [x] build postgressql docker
    - [x] build mage-ai docker
    - [x] build metabase docker
    - [x] build.sh
- [x] simple pipeline
- [ ] multi crawler
    - [ ] ICrawler - Exporter
    - [x] https://relocate.me/ crawler
    - [ ] https://www.glassdoor.com/ crawler
    - [ ] https://siaexplains.github.io/visa-sponsorship-companies/ crawler
    - [x] https://www.linkedin.com/jobs/ crawler
    - [x] linkedin retries
- [ ] Detailed Page
    - [ ] Detailes of relocate and extract data from it
    - [x] Detailes of linkedin
- [ ] crawler settings
    - [ ] preference, configs and filters panel ?
    - [ ] relocate filters
- [x] hash_id and update, replace
- [ ] db id for update not insert
- [ ] UI
    - [ ] **store dashboards**
    - [ ] panel for sertting values for positions (not_interested, interested, applied)
- [ ] dbt
    - [ ] join and one meta table
    - [ ] tables doc
    - [ ] tests
- [ ] kafka
    - [ ] event based for linkedin job alerts
- [ ] spark
    - [ ] batch processing of PDPs
- [ ] cloud deployment
    - Hamravesh
    - Arvan
    - liara
- [x] github page
- [ ] explain the project in readme
- [ ] change the name from tech job crawler to tech career explorer
- [x] config handler

how to build:
1. docker clone
2. chmod +x build.sh
3. ./build.sh