import pandas as pd

def load_authors() -> pd.DataFrame:
    """
    Load authors table (needs at least: gutenberg_author_id, alias)

    """
    source = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_authors.csv"
    return pd.read_csv(source)


def load_languages() -> pd.DataFrame:
    """
    Load languages table (needs at least: gutenberg_author_id, languages)

    """
    source = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_languages.csv"
    return pd.read_csv(source)


def load_metadata() -> pd.DataFrame:
    """
    Load metadata table (needs at least: gutenberg_author_id, gutenberg_id)

    """
    source = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_metadata.csv"
    return pd.read_csv(source)