from .csv_integration import *


def read_acled():
    """Read in and combine ACLED data"""
    regions = {
        "Africa": "data/Africa_aggregated_data_up_to-2025-10-18.csv",
        "Asia-Pacific": "data/Asia-Pacific_aggregated_data_up_to-2025-10-18.csv",
        "Europe-Central-Asia": "data/Europe-Central-Asia_aggregated_data_up_to-2025-10-18.csv",
        "Latin-America-the-Caribbean": "data/Latin-America-the-Caribbean_aggregated_data_up_to-2025-10-18.csv",
        "Middle-East": "data/Middle-East_aggregated_data_up_to-2025-10-18.csv",
        "US-and-Canada": "data/US-and-Canada_aggregated_data_up_to-2025-10-18.csv"
    }

    # Combine datasets
    dfs = {}
    for region_name, file_path in regions.items():
        dfs[region_name] = pd.read_csv(file_path)
        print(f"Loaded {region_name}: {len(dfs[region_name])} rows")

    # Combine into single DataFrame
    acled = pd.concat(dfs.values(), ignore_index=True)
    print(f"Combined dataset: {len(acled)} total rows")

    return acled


def tier1_integration(tier1, acled):
    """
    Pipeline for tier 1 csv integration, convering the following countries
    """
    for country, paths in tier1.items():
        trends_data, merged = data_prep(filter_country, country, paths, acled)
        corr_df = corr_analysis(trends_data, merged)
        top_terms = time_lag_analysis(corr_df, merged)
        key_periods(top_terms, trends_data, merged)
        visualizations(country, top_terms, merged)

def tier2_integration(tier2, acled):
    """
    Pipeline for tier 2 csv integration
    """
    tier1_integration(tier2, acled)

def tier3_integration(tier3, acled):
    """
    Pipeline for tier 3 csv integration
    """
    for cat, cat_dict in tier3.items():
        if cat == 'country':
            filter = filter_country
        elif cat == 'theme':
            filter = filter_theme
        else:
            filter = filter_region

        for name, paths in cat_dict.items():
            trends_data, merged = data_prep(filter, name, paths, acled)
            corr_df = corr_analysis(trends_data, merged)
            top_terms = time_lag_analysis(corr_df, merged)
            key_periods(top_terms, trends_data, merged)
            visualizations(name, top_terms, merged)


# Helper functions for filtering acled data (by country, region, and theme)
def filter_country(name, acled):
    return acled[
        (acled['COUNTRY'] == name.title()) &
        (acled['WEEK'] >= '2020-01-01')
    ]

def filter_region(name, acled):
    return acled[
        (acled['REGION'] == name.title()) &
        (acled['WEEK'] >= '2020-01-01')
    ]

def filter_theme(name, acled):
    return acled
