# CRM Analytics Pipeline

A comprehensive data pipeline for CRM analytics, leveraging modern data stack tools including Airflow, dbt, and PostgreSQL.

## Project Overview

This project implements an end-to-end analytics pipeline for CRM data:

1. **Data Extraction**: Extract data from CRM sources (HubSpot mock data)
2. **Data Transformation**: Transform data using dbt models
3. **Orchestration**: Schedule and run the pipeline using Airflow
4. **Visualization**: Analyze data using Jupyter notebooks

## Project Structure

```
CRM-Analytics-Pipeline/
├── dags/                # Airflow DAGs
├── data/                # Raw data files
├── dbt/                 # dbt project
│   ├── models/          # dbt models
│   │   ├── marts/       # Dimensional models
│   │   └── staging/     # Staging models
│   └── tests/           # Custom dbt tests
├── logs/                # Log files
├── notebooks/           # Jupyter notebooks
├── scripts/             # Python scripts
├── sql/                 # SQL scripts
│   └── init/            # Database initialization scripts
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # dbt Dockerfile
└── run_airflow.sh       # script for Airflow
```





