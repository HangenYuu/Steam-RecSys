from os import path

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mongodb import MongoDB

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_mongodb(data, **kwargs) -> None:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    data = df.to_dict(orient="records")

    MongoDB.with_config(ConfigFileLoader(config_path, config_profile)).export(
        data,
        collection=kwargs['COLLECTION_NAME'],
    )