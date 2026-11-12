"""Local data loading (replaces google.colab.drive / gdown / pooch in notebooks)."""

from pathlib import Path

import pandas as pd
import xarray as xr

from .config import DATA_DIR, CHIRPS_FILE, COUNTRY_MASK_FILE, FAOSTAT_FILE


def get_data_dir() -> Path:
    """Return the directory containing local project data."""
    return DATA_DIR


def load_chirps(filename: str = CHIRPS_FILE) -> xr.Dataset:
    """Load the CHIRPS precipitation dataset."""
    path = DATA_DIR / filename
    return xr.open_dataset(path)


def load_country_mask(filename: str = COUNTRY_MASK_FILE) -> xr.Dataset:
    """Load the country mask dataset."""
    path = DATA_DIR / filename
    return xr.open_dataset(path)


def load_fao_crops(filename: str = FAOSTAT_FILE) -> pd.DataFrame:
    """Load the FAO cereal production CSV."""
    path = DATA_DIR / filename
    return pd.read_csv(path)
