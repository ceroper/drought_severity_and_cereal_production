"""Repository-wide configuration: paths, analysis period, countries, and constants."""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# This file lives at <repo>/Code/util/config.py.
UTIL_DIR = Path(__file__).resolve().parent
CODE_DIR = UTIL_DIR.parent
REPO_ROOT = CODE_DIR.parent
DATA_DIR = CODE_DIR / "data"

# Data file names
CHIRPS_FILE = "chirps_sel.nc"
COUNTRY_MASK_FILE = "CountryMergedNC.nc"
FAOSTAT_FILE = "FAOSTAT_data_en_7-18-2026.csv"
ANNUAL_SPI_VIETNAM_FILE = "annual_spi_vietnam.csv"
ANNUAL_SPI_INDONESIA_FILE = "annual_spi_indonesia.csv"

# ---------------------------------------------------------------------------
# Analysis settings
# ---------------------------------------------------------------------------
ANALYSIS_PERIOD = ("1981", "2023")
COUNTRIES = ["Indonesia", "Viet Nam"]

# CHIRPS domain covers mainland (MCR/Vietnam) and maritime (ECR/Indonesia).
COUNTRY_CODES = {"Indonesia": "IDN", "Viet Nam": "VNM"}

# ---------------------------------------------------------------------------
# Drought severity (SPI-based)
# ---------------------------------------------------------------------------
DROUGHT_SEVERITY_bins = [-float("inf"), -2.0, -1.5, -1.0]
DROUGHT_SEVERITY_labels = ["Extreme Drought", "Severe Drought", "Moderate Drought"]