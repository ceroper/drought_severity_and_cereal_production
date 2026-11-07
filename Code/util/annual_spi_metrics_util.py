import pandas as pd
import numpy as np
import xarray as xr

def monthly_severity_per_year(x):
    """
    x: xarray.DataArray with 'spi' monthly and 'time' coordinate (datetime)
    Returns DataFrame with counts of months in each drought severity per year
    """
    # Resample to annual frequency, using last value per year
    annual = x.resample(time='1YE').last()
    annual = annual.to_pandas()

    # Assign year
    annual['year'] = annual.index.year

    # Define bins and severity names
    bins = [-np.inf, -2.0, -1.5, -1.0, 0, np.inf]
    labels = ['Extreme Drought', 'Severe Drought', 'Moderate Drought', 'Mild Drought', 'No Drought']

    # Categorize SPI values into integer codes (0 to 4)
    annual['bin_id'] = pd.cut(annual['spi'], bins=bins, labels=False)

    # Map codes to actual label strings
    code_to_label = {i: l for i, l in enumerate(labels)}
    annual['severity'] = annual['bin_id'].map(code_to_label)

    # Count months per year per severity
    result = annual.groupby('year')['severity'].count().reset_index()

    # Make sure all severity columns exist (even if zero)
    # The columns will be: year, Extreme Drought, Severe Drought, Moderate Drought, Mild Drought, No Drought
    return result

def categorize_spi(spi_data_array):
  """
  Categorizes SPI values into drought severity levels.

  Takes an xarray DataArray containing 12m SPI values with a 'time' coordinate.

  Returns a pandas DataFrame with the annual 'spi' and its 'category'
  """
  spi_12m_annual = spi_data_array.resample(time='1YE').last()
  spi_12m_annual_pd = spi_12m_annual.to_pandas()
  spi_12m_annual_pd.index = spi_12m_annual_pd.index.year
  spi_12m_annual_pd.index.name = 'year'
  spi_values = spi_12m_annual_pd.rename('SPI Value')

  # Define bins and labels for drought severity
  bins = [-np.inf, -2.0, -1.5, -1.0, 0, np.inf]
  labels = ['Extreme Drought', 'Severe Drought', 'Moderate Drought', 'Mild Drought', 'No Drought']

  # Categorize SPI values
  spi_category = pd.cut(spi_values, bins=bins, labels=labels, right=False)

  # Create a DataFrame from the results
  result_df = pd.DataFrame({
      'spi': spi_values,
      'category': spi_category
  })

  return result_df

def get_severity_label(spi_value):
    """
    Determines the drought severity label based on SPI value.
    """
    if spi_value <= -2.0:
        return DROUGHT_SEVERITY_labels[0]
    elif spi_value <= -1.5:
        return DROUGHT_SEVERITY_labels[1]
    elif spi_value <= -1.0:
        return DROUGHT_SEVERITY_labels[2]
    else:
        return None

def extract_years_in_drought_spell(spell_data):
    """
    Given a list of {'time':..., 'spi':...} entries for a drought spell,
    returns the set of years during the spell.
    """
    times = [pd.to_datetime(d['time']) for d in spell_data]
    years = np.unique(times.year)
    return years.tolist()

def process_drought_spell(spell_data, yearly_summary):
    """
    Processes a single drought spell and updates yearly_summary.
    """
    if not spell_data:
        return

    # Build xarray DataArray for the spell
    spi_values = xr.DataArray([d['spi'] for d in spell_data],
                              coords={'time': [d['time'] for d in spell_data]})
    years_in_spell = extract_years_in_drought_spell(spell_data)

    for year in years_in_spell:
        # Filter SPI values for this year
        spi_for_year = spi_values.sel(time=str(year))
        if spi_for_year.size > 0:
            min_spi = spi_for_year.min().item()
            label = get_severity_label(min_spi)
            if label:
                if year not in yearly_summary:
                    yearly_summary[year] = {'event_count': 0, 'severity_counts': {k:0 for k in DROUGHT_SEVERITY_labels}}
                yearly_summary[year]['event_count'] += 1
                yearly_summary[year]['severity_counts'][label] += 1

# Drought severity labels and bins
DROUGHT_SEVERITY_bins = [-np.inf, -2.0, -1.5, -1.0]
DROUGHT_SEVERITY_labels = ['Extreme Drought', 'Severe Drought', 'Moderate Drought']

def process_all_data(spi_data,
                    drought_severity_bins=DROUGHT_SEVERITY_bins,
                    drought_severity_labels=DROUGHT_SEVERITY_labels):
    """
    Processes the entire SPI time series to compute yearly drought summary.
    Assumes spi_data is an xarray DataArray of (time, spi) with time as datetime.
    """
    yearly_summary = {}
    current_drought_spell_data = []
    in_drought = False

    # Iterate through (time_val, spi_val) pairs
    for time_val, spi_val in zip(spi_data.time.values, spi_data.values):
        if spi_val <= drought_severity_bins[1]:  # SPI <= -1.0 is drought
            in_drought = True
            current_drought_spell_data.append({'time': time_val, 'spi': spi_val})
        else:
            if in_drought:
                # End of drought spell
                process_drought_spell(current_drought_spell_data, yearly_summary)
                current_drought_spell_data = []
                in_drought = False

    # Check for a trailing drought spell at the end
    if in_drought and current_drought_spell_data:
        process_drought_spell(current_drought_spell_data, yearly_summary)

    return yearly_summary

# Example usage (if you want to test):
# yearly_summary = process_all_data(spi_1m_viet)
