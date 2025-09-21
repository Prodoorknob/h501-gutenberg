# h501-gutenberg

A tiny Python package + notebook for the H501 exercise:

> **List Project Gutenberg author aliases in order of translation count** using the TidyTuesday “Project Gutenberg” dataset (week of 2025-06-03).  
> The ordered list is displayed inside `gutenberg.ipynb`.

## Repo layout

```
h501-gutenberg/
├─ tt_gutenberg/
│  ├─ __init__.py
│  ├─ authors.py        # public API: list_authors(...)
│  └─ io_utils.py       # CSV loaders (local path or URL)
└─ gutenberg.ipynb      # notebook that prints the list of aliases
```

## What it does

1. **Loads 3 CSVs** from the TidyTuesday Gutenberg week:
   - `gutenberg_languages.csv` — per-work language list, keyed by `gutenberg_id`
   - `gutenberg_metadata.csv` — maps each `gutenberg_id` to one or more author IDs
   - `gutenberg_authors.csv` — author table with `alias`
2. **Joins** Languages → Metadata → Authors to attach an **alias** to each work.
3. **Parses languages** robustly (accepts `en`, `eng`, `english`, semicolons/commas/pipes).
4. **Counts translations per alias** (two modes):
   - `by_languages=True` (default): number of **distinct non-English languages** across that author’s works.
   - `by_languages=False`: number of **unique works** with any non-English language.
5. **Returns a Python list** of aliases sorted by count (desc), tie-broken alphabetically.

## Quick start

### Option A — Run the notebook (no install)
Open `gutenberg.ipynb` from the **repo root** and run:

```python
from tt_gutenberg.authors import *

AUTHORS_URL   = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_authors.csv"
LANGUAGES_URL = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_languages.csv"
METADATA_URL  = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-06-03/gutenberg_metadata.csv"

aliases = list_authors(
    by_languages=True,    # distinct non-English language codes per alias
    alias=True,
    authors_csv=AUTHORS_URL,
    languages_csv=LANGUAGES_URL,
    metadata_csv=METADATA_URL
)
aliases  # printed output visible in the notebook
```

> If your notebook isn’t launched from the repo root, add:
> ```python
> import sys, pathlib; sys.path.insert(0, str(pathlib.Path.cwd()))
> ```

### Option B — Editable install

Add a minimal `pyproject.toml` (optional):

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "h501-gutenberg"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = ["pandas>=1.5"]

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
    alias: bool = True,                    # kept for interface parity; always returns aliases
    authors_csv: str | None = None,        # local path or URL
    languages_csv: str | None = None,      # local path or URL
    metadata_csv: str | None = None        # local path or URL
) -> list[str]
```

If you don’t pass URLs/paths, the loaders default to the **2025-06-03** TidyTuesday files.

## Notes for graders

- Every module in `tt_gutenberg/` contains **only imports and functions** (no top-level executable code).
- `authors.py` calls helpers in **`io_utils.py`** to satisfy the “multi-module” requirement.
- The notebook cell prints a **list** of aliases in the required order.

## Troubleshooting

- **`ModuleNotFoundError: tt_gutenberg`**  
  Open the notebook from the repo root or add the repo path to `sys.path`.

- **“Merge keys are not unique … validate='m:1'”**  
  The implementation deduplicates metadata (multiple author IDs per work) and authors (multiple rows per author id) before merging. If you edited those helpers, re-enable the dedupe.

- **Empty result**  
  Usually language parsing/filters. The code recognizes `en|eng|english` as English and counts the rest; ensure you didn’t change the parsing/filters.

- **Duplicate `alias` columns**  
  Joins can create `alias`, `alias_au`, etc. The code coalesces them into a single `alias` and drops the rest.

## Data

TidyTuesday “Project Gutenberg” week (2025-06-03) — CSVs hosted in the rfordatascience/tidytuesday repo:
- `gutenberg_authors.csv`
- `gutenberg_languages.csv`
- `gutenberg_metadata.csv`

## License

Add a LICENSE file if you plan to share (MIT suggested). TidyTuesday data is released to the public domain (CC0).

---

**Commit this README**

```bash
git add README.md
git commit -m "Add project README"
git push
```
