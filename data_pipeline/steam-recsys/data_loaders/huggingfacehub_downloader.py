from huggingface_hub import hf_hub_download
from mage_ai.data_preparation.shared.secrets import get_secret_value
from pathlib import Path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here
    print("Downloading data from Hugging Face...")
    repo_id = "HangenYuu/Steam_Games_Review"
    local_dir = Path("data")
    filenames = ["games_description.csv", "games_ranking.csv", "steam_game_reviews.csv"]

    for filename in filenames:
        hf_hub_download(
            repo_id=repo_id, filename=filename, repo_type="dataset", local_dir=local_dir, token=get_secret_value("HF_TOKEN")
        )
    print("Data downloaded successfully")
    return


@test
def test_output(*args) -> None:
    """
    Template code for testing the output of the block.
    """
