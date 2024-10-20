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
    print("Downloading data from Hugging Face...")
    repo_id = "HangenYuu/Steam_Games_Review"
    local_dir = Path("data")
    filenames = ["games_description", "games_ranking", "steam_game_reviews"]

    result = []

    for filename in filenames:
        print(f"Downloading {filename}...")
        hf_hub_download(
            repo_id=repo_id,
            filename=f"{filename}.csv",
            repo_type="dataset",
            local_dir=local_dir,
            token=get_secret_value("HF_TOKEN"),
        )
        result.append(dict(name=filename, data=pl.read_csv(local_dir / f"{filename}.csv", infer_schema_length=10000)))

    print("Data downloaded successfully")
    return [result]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert isinstance(output, list)
    assert len(output[0]) == 2