if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import polars as pl
from pathlib import Path

@transformer
def transform(*args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    def parse_reviews(value):
        if "%" in value:
            # Extract percentage and total number
            match = re.search(r"(\d+)% of ([\d,]+)", value)
            if match:
                percentage = int(match.group(1))
                total = int(match.group(2).replace(",", ""))
                return int((percentage / 100) * total)
        else:
            # Extract the number directly
            match = re.search(r"\(([\d,]+)\)", value)
            if match:
                return int(match.group(1).replace(",", ""))


    def parse_system_requirements(requirements_list):
        result = {}
        for item in requirements_list:
            if ":" in item:
                key, value = item.split(":")[:2]
                result[key.strip()] = value.strip()
        return result
    
    local_dir = Path("data")

    df = pl.read_csv(local_dir / "games_description.csv")
    df = df.with_columns(
        pl.col("genres").str.replace_many(["]", "'", "["], "").str.split(", "),
        pl.col("number_of_english_reviews").str.replace_all(",", "").cast(pl.Int32),
        pl.col(["minimum_system_requirement", "recommend_system_requirement"])
        .str.replace_many(["]", "'", "["], "")
        .str.split(", ")
        .map_elements(parse_system_requirements, return_dtype=pl.Object),
        pl.col(["developer", "publisher"])
        .str.replace_many(["]", "'", "["], "")
        .str.split(", "),
        pl.col("overall_player_rating").cast(pl.Categorical("lexical")),
        pl.when(pl.col("release_date").str.contains(r"\d{1,2} \w{3}, \d{4}"))
        .then(pl.col("release_date").str.to_date("%d %b, %Y", strict=False))
        .otherwise(pl.col("release_date").str.to_date("%b %Y", strict=False))
        .alias("release_date"),
        pl.col("number_of_reviews_from_purchased_people").map_elements(
            parse_reviews, return_dtype=pl.Int32
        ),
    )

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
