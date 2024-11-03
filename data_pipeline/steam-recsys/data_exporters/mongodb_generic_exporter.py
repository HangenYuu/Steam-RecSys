from os import path
from pandas import DataFrame
import pandas as pd
import json
import numpy as np

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.mongodb import MongoDB

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.int64, np.int32)):
            return int(obj)
        else:
            return super(CustomEncoder, self).default(obj)

@data_exporter
def export_data_to_mongodb(df: DataFrame, **kwargs) -> None:
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    data_dict = df.to_dict(orient="records")
    data_dict_1 = json.dumps(data_dict, cls=CustomEncoder)
    data_dict_final = json.loads(data_dict_1)

    MongoDB.with_config(ConfigFileLoader(config_path, config_profile)).export(
        data_dict_final,
        collection=kwargs['COLLECTION_NAME'],
    )