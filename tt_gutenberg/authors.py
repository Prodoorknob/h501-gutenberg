from typing import List
import pandas as pd
from .utils import load_authors, load_languages, load_metadata



def list_authors(by_languages: bool = True,alias: bool = True) -> List[str]:
    """
    Lists Project Gutenberg author aliases in order of translation count.

    Args:
        by_languages (bool, optional): If True, orders authors by the number of languages they have been translated into. Defaults to True.
        alias (bool, optional): If True, returns author aliases. Defaults to True.

    Returns:
        list: A list of author aliases ordered by translation count.
    """
    authors = load_authors()
    languages   = load_languages()
    metadata    = load_metadata()

    if by_languages and alias:
        # Merge the dataframes
        merge=metadata.merge(languages, on='gutenberg_id', how="left")
        merge= merge.drop_duplicates().sort_values(by='gutenberg_id').reset_index(drop=True).dropna()
        merge['gutenberg_id']=merge['gutenberg_id'].astype(int)
        merge_2=merge.merge(authors, on='gutenberg_author_id', how="left")
        #calculate the total translations
        aliases=merge_2.groupby('alias')['total_languages'].sum().sort_values(ascending=False).reset_index()
        # clean and list author names
        author_aliases = [str(author_alias) for author_alias in aliases['alias'] if pd.notna(author_alias) and str(author_alias).strip()]

        return author_aliases
    else:
        return []
