from huggingface_hub import hf_hub_download
from mage_ai.data_preparation.shared.secrets import get_secret_value
from pathlib import Path
import polars as pl

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs) -> list[dict]:
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    print("Getting data from the folder...")
    repo_id = "HangenYuu/Steam_Games_Review"
    local_dir = Path("data/processed")
    filenames = kwargs['POSTGRES_TABLES'].split(",")

    result = []

    for filename in filenames:
        result.append(dict(name=filename, data=pl.read_parquet(local_dir / f"{filename}.parquet")))

    return [result]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert isinstance(output, list)
    assert len(output[0]) == 2