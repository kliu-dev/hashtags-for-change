# Hashtags for Change

*This project was managed under the University of Chicago's Data Science Society
in Winter Quarter, 2026. This repository contains a polished, easily
reproducible version of my responsibilities as a member of the project team.
The full project repository can be found [here](https://github.com/Tahvia127/Hashtags-For-Change).*

## Project Overview
**Objective:** Analyze how global awareness of social and human rights events
spreads through hashtags and social media activity, and how digital awareness
can drive real-world action.

The objective of this portion of the project is to compare the google trends
data for search terms and hashtags of interest to the ACLED database. This
project is concerned with a specific list of search terms and hashtags, but
the same code can be applied to any Google trends search term.

## Project Structure
```
src /
    hashtags_for_change /
        __init__.py
        csv_integration.py
        filepaths.py
        main.py
        pipeline.py
pyproject.toml
uv.lock
README.md
.gitignore
.python-version
```

## Data

### ACLED Data
The ACLED data includes comprehensive information on global events. The dataset
places events into categories like battles, protests, riots, and more, and
includes counts on how many events have occcured in a certain country at a
given time.

In this project, the ALCED data serves as a reference to compare the Google
trends data with. By aligning the two by date and running correlation and
time-lag analysis, we can explore how public interest relates to event occurences
in countries, regions, and across the globe in regards to specific themes.

### Google Trends Data
The Google trends data consist of separate CSV files for each search term or
hashtag of interest. The terms are separated into Tier 1, Tier 2, and Tier 3
based on priority, which was determined by the frequency of relevant events in
the ACLED dataset.The Google trends data spans from January 1, 2020 to October
18, 2025 and goes by month. Showing search volume over time on a 0-100 scale
relative to peak interest, with 100 being peak interest in the time period,
Google trends indicates how interest in specific topics evolve over time.

Tier 1 consists of search terms for the following countries:
- Ukraine
- India
- United States
- Mexico
- Syria
- Brazil
- Palestine
- Yemen
- Pakistan

Tier 2 consists of search terms of the following countries:
- Iraq
- France
- Russia
- South Korea
- Turkey
- Colombia
- Lebanon
- Nigeria
- Italy
- Afghanistan

Tier 3 consists of hashtag-based searches that are either country-specific,
theme-specific, or region-specific.

The data can be found in the zip file here. The files are divided by tier, and
the file names are saved as 'google_trends_{TERM}.csv'

### Data Folder Structure
All data can be downloaded [here](https://drive.google.com/drive/folders/1xO4mQmm38dj6yfCEWAROvCLJf5x3fFwV?usp=drive_link).


The files have the following structure:
```
├── data
│   ├── Africa_aggregated_data_up_to-2025-10-18.csv
│   ├── Asia-Pacific_aggregated_data_up_to-2025-10-18.csv
│   ├── Europe-Central-Asia_aggregated_data_up_to-2025-10-18.csv
│   ├── google_trends_raw
│   │   ├── collection_log.csv
│   │   ├── hashtags_brainstorm.csv
│   │   ├── TIER1_COUNTRIES
│   │   ├── TIER2_COUNTRIES
│   │   └── TIER3_HASHTAGS
│   ├── Latin-America-the-Caribbean_aggregated_data_up_to-2025-10-18.csv
│   ├── Middle-East_aggregated_data_up_to-2025-10-18.csv
│   ├── number_of_political_violence_events_by_country-month-year_as-of-03Oct2025.xlsx
│   ├── US-and-Canada_aggregated_data_up_to-2025-10-18.csv
│   └── world.geojson
```


## Environment Setup
This project uses Python 3.13 and manages dependencies with **uv**.

Install dependencies:
```
uv sync
```

Run the full project:
```
uv run hashtags-for-change
```

## Code

### main.py
Serves as a central location to execute functions. Run main.py to execute
entire project.


### filepaths.py
Creates dictionaries containing the paths to Google trends files, returning
tier 1, tier 2, and tier 3 dictionaries.

To create and verify all filepaths, in main.py, run:
```
def main():
    tier1, tier2, tier3 = create_paths_dict()
    validate_paths(tier1)
    validate_paths(tier2)
    validate_paths_tier3(tier3)
```

If correct, `Success loading {filename}` should be printed after every file and
the file sums should be:
- tier1 -> 44
- tier2 -> 25
- tier3 -> 89

**NOTE:** This file uses a path header constant that may need to be updated depending
on your local file system structure.


### csv_integration.py
Performs correlation and time lag analysis on Google trends and ACLED data.

Produces interactive graphs comparing ACLED event data with Google trends:
- a combined multi-series charts comparing all metrics
- individual comparison charts for each top search term


### pipeline.py
Pipeline that processes all Google trends files through `csv_integration`.

To complete all analysis, in main.py, run:
```
def main():
    tier1, tier2, tier3 = create_paths_dict()

    tier1_integration(tier1, acled)
    tier2_integration(tier2, acled)
    tier3_integration(tier3, acled)
```

## Key Insights
- according to the time lag analysis, lag 0 wins in every case
- public attention, not anticipatory, so it can not be cosidered a crisis early
warning tool or a predictive signal
- search interest tends to spike when an event occurs, but quickly falls
downwards
- higher attention events with lower fatalities, like the Yemen Red Sea Attacks,
may be because they involve people from outside of Yemen, thus receiving more
Western attention
