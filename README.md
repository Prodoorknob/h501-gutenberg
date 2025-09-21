# h501-gutenberg

A tiny Python package + notebook for the H501 exercise:

> List Project Gutenberg author **aliases** in order of translation count using the TidyTuesday “Project Gutenberg” dataset (week of 2025‑06‑03).  
> Display that ordered list in `gutenberg.ipynb`, **and** visualize how translation counts vary across *author birth centuries*.

## Repo layout

```
h501-gutenberg/
├─ tt_gutenberg/
│  ├─ __init__.py
│  ├─ authors.py        # public API: list_authors(...)
│  └─ io_utils.py       # CSV loaders (local path or URL)
└─ gutenberg.ipynb      # notebook that prints the ordered list and shows a bar plot
```

## What it does

1. Loads 3 CSVs from the TidyTuesday Gutenberg week:
   - `gutenberg_languages.csv` — per‑work language list, keyed by `gutenberg_id`
   - `gutenberg_metadata.csv` — maps each `gutenberg_id` to one or more author IDs
   - `gutenberg_authors.csv` — author table with `alias` and canonical `name`
2. Joins **Languages → Metadata → Authors** to attach an **alias** to each work.
3. Parses languages robustly (accepts `en`, `eng`, `english`; handles semicolons/commas/pipes).
4. Counts translations per alias (two modes):
   - `by_languages=True` *(default)*: number of **distinct non‑English languages** across that author’s works.
   - `by_languages=False`: number of **unique works** with any non‑English language.
5. Returns a Python **list of aliases** sorted by count (desc), tie‑broken alphabetically.
6. **New**: Adds a notebook helper `plot_translations(over='birth_century')` that builds a Seaborn **bar plot** of
   the **average number of distinct languages per author**, grouped by each author’s **birth century**.  
   - The plot **uses canonical author names (not aliases)** for the per‑author aggregation.  
   - X‑axis: integer centuries (e.g., `1700` means `1700–1799`).  
   - Y‑axis: mean number of distinct languages per author with **95% CI** error bars.

## Quick start

### Option A — Run the notebook (no install)

Open `gutenberg.ipynb` from the repo root and run:

```python
from tt_gutenberg.authors import *

AUTHORS_URL   = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_authors.csv"
LANGUAGES_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_languages.csv"
METADATA_URL  = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_metadata.csv"

# Ordered list of author aliases by translation count
aliases = list_authors(
    by_languages=True,    # distinct non‑English language codes per alias
    alias=True,
    authors_csv=AUTHORS_URL,
    languages_csv=LANGUAGES_URL,
    metadata_csv=METADATA_URL
)
aliases
```

To generate the **birth‑century bar plot**, make sure the notebook has `authors`, `metadata`, and the helper loaded (the provided notebook cell does this), then:

```python
plot_translations(over='birth_century')
```

This produces a Seaborn bar plot where each bar is the **average number of distinct languages per author** in that **birth century** (95% CI shown). Birth year → century mapping uses floor to the lower hundred (e.g., `1753.0 → 1700`).

> If your notebook isn’t launched from the repo root, add:
>
> ```python
> import sys, pathlib
> sys.path.insert(0, str(pathlib.Path.cwd()))
> ```

### Option B — Editable install (optional)

Add a minimal `pyproject.toml` (optional):

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "h501-gutenberg"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["pandas>=1.5", "matplotlib>=3.6", "seaborn>=0.12"]

[tool.setuptools]
packages = ["tt_gutenberg"]
```

Then:

```bash
pip install -e .
```

Use from any script/notebook:

```python
from tt_gutenberg.authors import list_authors
```

## API

```python
from tt_gutenberg.authors import list_authors

list_authors(
    by_languages: bool = True,
    alias: bool = True,                    # kept for interface parity; returns aliases
    authors_csv: str | None = None,        # local path or URL
    languages_csv: str | None = None,      # local path or URL
    metadata_csv: str | None = None        # local path or URL
) -> list[str]
```

If you don’t pass URLs/paths, the loaders default to the 2025‑06‑03 TidyTuesday files.

## Visualization details

- **Aggregation unit**: one row per **author (canonical name)** with `n_languages = number of distinct language codes` across that author’s works.
- **Birth century**: `birth_century = floor(birth_year/100)*100` (integers like `1600`, `1700`, …).
- **Error bars**: 95% confidence intervals via Seaborn’s `barplot`. If your Seaborn version uses `errorbar=("ci", 95)` and that raises a `TypeError`, it will fall back to the legacy `ci=95` parameter automatically in the helper cell.
- **Missing values**: authors with unknown birth year are omitted from the plot; authors with no language data are treated as `0` in their group’s average.

## Troubleshooting

- **`ModuleNotFoundError: tt_gutenberg`**  
  Open the notebook from the repo root or add the repo path to `sys.path` as shown above.

- **“Merge keys are not unique … `validate='m:1'`”**  
  The implementation deduplicates metadata (multiple author IDs per work) and authors (multiple rows per author id) before merging. If you edited those helpers, re‑enable dedupe.

- **Empty result / unexpected zeros**  
  Language parsing/filters: the code recognizes `en|eng|english` as English and counts the rest; ensure you didn’t change the parsing/filters.

- **Seaborn errorbar parameter**  
  Older Seaborn uses `ci=95`; newer uses `errorbar=("ci", 95)`. The helper handles both.

## Data

TidyTuesday “Project Gutenberg” week (2025‑06‑03) — CSVs hosted in the `rfordatascience/tidytuesday` repo:

- `gutenberg_authors.csv`
- `gutenberg_languages.csv`
- `gutenberg_metadata.csv`

## License

Add a LICENSE file if you plan to share (MIT suggested). TidyTuesday data is released to the public domain (CC0).