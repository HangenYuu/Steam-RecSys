from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from datetime import date

@data_loader
def load_data_from_postgres(*args, **kwargs):
    """
    Template for loading data from a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """
    schema_name = kwargs["POSTGRES_SCHEMA"]
    table_names = kwargs['GENERIC_TABLES'].split(",")
    today = date.today()
    result = []
    for table in table_names:
        query = f'SELECT * FROM {schema_name}.{table}'
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'

        with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
            df = loader.load(query)
            df["record_created_dt"] = today
            result.append(dict(name=table, data=df))
    return [result]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'