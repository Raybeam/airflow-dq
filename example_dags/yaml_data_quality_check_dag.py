from datetime import datetime, timedelta

import airflow
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

from utilities.dq_check_tools import create_dq_checks_from_directory, create_dq_checks_from_list

default_args = {
    "owner" : "airflow",
    "start_date" : airflow.utils.dates.days_ago(1),
    "retries" : 0,
    "retry_delay" : timedelta(minutes=5),
    "email_on_failure" : True
}

YAML_DIR = "./tests/configs/yaml_configs"

YAML_LIST = [
    ('./example_dags/yaml_dq_check_dag/yaml_configs/dq_check1.yaml', {'start_date': default_args['start_date']}),
    ('./example_dags/yaml_dq_check_dag/yaml_configs/dq_check2.yaml', {})
]

dag = DAG(
    "yaml_data_quality_check_dag",
    default_args=default_args,
    schedule_interval=None
)

dq_check_tasks = create_dq_checks_from_directory(dag, YAML_DIR) + create_dq_checks_from_list(dag, YAML_LIST)

start = DummyOperator(
    task_id="start",
    dag=dag
)

load_data = PostgresOperator(
    task_id="load_test_data",
    sql="./yaml_dq_check_dag/load_test_data.sql",
    postgres_conn_id="test_conn",
    dag=dag
)

end = DummyOperator(
    task_id="end",
    dag=dag
)

start >> load_data >> dq_check_tasks >> end