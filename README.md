# tech-job-crawler

tools to use:
- postgres as data warehouse (production)
- duckdb as data warehouse (development)
- mage-ai as pipeline orchestrator
- DLT, DBT for ELT
- metabase for dashboard
<!-- - spark
- hamravesh or Arvan as cloud provider
- teraform  -->


todos:
- [x] build postgressql docker
- [x] build mage-ai docker
- [x] build metabase docker
- [x] make build
- [x] simple pipeline
- [ ] multi crawler
    - [ ] ICrawler - Exporter
    - [x] https://relocate.me/ crawler
    - [ ] https://www.glassdoor.com/ crawler
    - [ ] https://siaexplains.github.io/visa-sponsorship-companies/ crawler
    - [ ] https://www.linkedin.com/jobs/ crawler
- [ ] Detailed Page
    - [ ] Detailes of relocate and extract data from it
- [ ] crawler settings
    - [ ] preference, configs and filters panel ?
    - [ ] relocate filters
- [ ] hash_id and update, replace
- [ ] UI
    - [ ] store dashboards
    - [ ] panel for sertting values for positions (not_interested, interested, applied)
- [ ] dbt
    - [ ] join and one meta table
    - [ ] tables doc
    - [ ] tests
- [ ] kafka
    - [ ] event based for linkdin
- [ ] spark
    - [ ] batch processing of PDPs

how to build:
1. docker clone
2. chmod +x build.sh
3. ./build.sh