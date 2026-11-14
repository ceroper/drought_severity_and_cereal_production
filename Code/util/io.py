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


def load_wdi_cereal(filename: str = "data_cereal_land.csv") -> pd.DataFrame:
    """
    Load World Development Indicators cereal production data.
    
    This function loads the WDI cereal production data (from data_cereal_land.csv),
    filters for Indonesia and Viet Nam, and transforms it into long format.
    
    The input file has:
    - Metadata rows at the top
    - Columns: Country Name, Country Code, Indicator Name, Indicator Code, and year columns
    - Values: Cereal production in metric tons
    
    Parameters:
    -----------
    filename : str, optional
        Path to WDI CSV file. Default is 'data_cereal_land.csv'.
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: ['Country Name', 'Country Code', 'Year', 'Production']
    """
    path = DATA_DIR / filename
    
    # Load the data (skip first 4 metadata rows, use row 4 as header)
    df = pd.read_csv(path, skiprows=4, header=0)
    
    # Filter for countries of interest
    countries = ['Indonesia', 'Viet Nam']
    df = df[df['Country Name'].isin(countries)]
    
    # Get year columns (1981-2023)
    year_columns = [str(year) for year in range(1981, 2024)]
    
    # Select only the columns we need
    columns_to_keep = ['Country Name', 'Country Code'] + year_columns
    existing_columns = [col for col in columns_to_keep if col in df.columns]
    df = df[existing_columns]
    
    # Transform to long format
    df_long = df.melt(
        id_vars=['Country Name', 'Country Code'],
        var_name='Year',
        value_name='Production'
    )
    
    # Convert Year to integer
    df_long['Year'] = df_long['Year'].astype(int)
    
    return df_long
