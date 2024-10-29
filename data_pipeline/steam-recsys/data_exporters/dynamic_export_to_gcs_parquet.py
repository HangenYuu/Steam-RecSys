from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path
import os
import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = get_secret_value('GOOGLE_APPLICATION_CREDENTIALS')

@data_exporter
def export_data_to_google_cloud_storage(data: dict, **kwargs) -> None:
    """
    Template for exporting data to a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """
    project_id = "solid-acrobat-440004-g5"
    bucket_name = kwargs['CONFORMED_BUCKET']    
    table_name = data["name"]
    root_path = f"{bucket_name}/{table_name}"

    table = pa.Table.from_pandas(pd.DataFrame(data["data"]))
    

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["record_created_dt"],
        filesystem=gcs
    )    