from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crm_analytics_pipeline',
    default_args=default_args,
    description='CRM Analytics Pipeline',
    schedule_interval='0 0 * * *',  
    start_date=days_ago(1),
    catchup=False,
    tags=['crm', 'analytics'],
)

# Task to extract data from source
extract_data = BashOperator(
    task_id='extract_data',
    bash_command='python /opt/airflow/scripts/extract_data.py',
    dag=dag,
)

# Task to run DBT models
run_dbt = BashOperator(
    task_id='run_dbt',
    bash_command='cd /opt/airflow/dbt && dbt run',
    dag=dag,
)

# Task to run DBT tests
test_dbt = BashOperator(
    task_id='test_dbt',
    bash_command='cd /opt/airflow/dbt && dbt test',
    dag=dag,
)

# Task to generate DBT documentation
generate_docs = BashOperator(
    task_id='generate_dbt_docs',
    bash_command='cd /opt/airflow/dbt && dbt docs generate',
    dag=dag,
)

# Set task dependencies
extract_data >> run_dbt >> test_dbt >> generate_docs 