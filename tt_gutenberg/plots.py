# --- Plot: average translation count per author by birth century ---
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
from .utils import load_authors, load_metadata

def plot_translations(over='birth_century'):
    """
    Creates a Seaborn barplot showing the average translation count for authors
    grouped by a specified category (e.g., birth century).

    Args:
        over (str): The column name to group authors by. Expected 'birth_century'.
    """
    # Load the datasets
    authors_df = load_authors()
    metadata_df    = load_metadata()
    # --- Data Processing ---

    # 1. Calculate the number of unique languages (translations) for each author
    # We group by the author ID and count the number of distinct languages.
    translation_counts = metadata_df.groupby('gutenberg_author_id')['language'].nunique().reset_index()
    translation_counts.rename(columns={'language': 'translation_count'}, inplace=True)

    # 2. Merge the translation counts with the main authors dataframe
    df = pd.merge(authors_df, translation_counts, on='gutenberg_author_id')

    # 3. Calculate the birth century
    # We drop authors with no birthdate and then calculate the century.
    # (e.g., 1753.0 -> 1700)
    df.dropna(subset=['birthdate'], inplace=True)
    df['birth_century'] = (df['birthdate'] // 100 * 100).astype(int)

    # --- Plotting ---

    # Create the barplot using Seaborn
    # `sns.barplot` automatically calculates the mean and the 95% confidence interval.
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.figure(figsize=(14, 8))
    ax = sns.barplot(data=df, x=over, y='translation_count', palette='viridis')

    # Set plot titles and labels for clarity
    ax.set_title(
        'Average Number of Translations by Author\'s Birth Century',
        fontsize=16,
        fontweight='bold'
    )
    ax.set_xlabel('Birth Century', fontsize=12)
    ax.set_ylabel('Average Translation Count', fontsize=12)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Usage:
#plot_translations(over='birth_century')
