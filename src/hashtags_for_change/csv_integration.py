import pandas as pd
import altair as alt


def data_prep(filter, name, trends_files, acled):
    """
    Extracts relevant portion of ACLED data for search term or hashtag of
    interest. Cleans and merges the Google trends and ACLED dataset by time to
    prepare for analysis.

    Args:
        - filter (callable): function that filters the ACLED data based on the
            category of the subject of the analysis
        - name (str): the name of the subject of analysis
        - trends_files (dict): the file paths of the csv files associated with 'name',
            in a dictionary (key = search term, value = full file path)
        - acled (pd.DataFrame): complete acled dataset

    Returns:
        - trends_data (dict): cleaned Google trends data for each search term
        - merged (pd.DataFrame): cleaned and combined dataset with ACLED and
            search interest aligned by month
    """
    print("\n" + "=" * 80)
    print(f"{name.upper()} ANALYSIS")
    print("=" * 80)

    filtered_acled = filter(name, acled)

    filtered_acled['WEEK'] = pd.to_datetime(filtered_acled['WEEK'])
    filtered_acled['month'] = filtered_acled['WEEK'].dt.to_period('M').dt.to_timestamp()

    country_monthly = filtered_acled.groupby('month').agg({
        'EVENTS': 'sum',
        'FATALITIES': 'sum'
    })

    print(f"ACLED data: {len(country_monthly)} months")
    print(f"Date range: {country_monthly.min()} to {country_monthly.max()}")
    print(f"Total events: {country_monthly['EVENTS'].sum():,}")
    print(f"Total fatalities: {country_monthly['FATALITIES'].sum():,}")

    # LOAD GOOGLE TRENDS FILES
    # ------------------------
    trends_data = {}
    for n, path in trends_files.items():
        try:
            df = pd.read_csv(path, skiprows = 1)
            df.columns = ['month', 'value']
            df['month'] = pd.to_datetime(df['month'])
            df['value'] = df['value'].replace('<1', '0.5')
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            trends_data[n] = df
            print(f"Loaded: {n:25s} - {len(df)} months, max={df['value'].max()}")
        except Exception as e:
            print(f"    ERROR LOADING {n}: {e}")

    # MERGE DATASETS
    # --------------
    merged = country_monthly.copy()
    for n, df in trends_data.items():
        merged = merged.merge(
            df.rename(columns={'value': n}),
            on='month',
            how='left'
        )
    print(f"\nMerged dataset: {len(merged)} months with {len(trends_data)} search terms")
    return trends_data, merged


def corr_analysis(trends_data, merged):
    """
    Conducts pearson correlation analysis between ACLED events data and Google
    trends data. Checks correlation with events and correlation with fatalities.

    Args:
        - trends_data (dict): cleaned Google trends data for each search term
        - merged (pd.DataFrame): cleaned and combined dataset with ACLED and
            search interest aligned by month

    Returns:
        - corr_df (pd.DataFrame): data frame containg correlation values between
            each search term and ACLED metric, as well as how many data points
            were used in each calculation
    """
    print("\n" + "=" * 80)
    print("CORRELATION ANALYSIS")
    print("=" * 80)

    try:
        correlations = []
        corr_df = None
        for term in trends_data.keys():
            if term in merged.columns:
                valid_data = merged[['EVENTS', 'FATALITIES', term]].dropna()
            if len(valid_data) > 10:
                corr_events = valid_data['EVENTS'].corr(valid_data[term])
                corr_fatalities = valid_data['FATALITIES'].corr(valid_data[term])
                correlations.append({
                    'Search Term': term,
                    'Corr w/ Events': corr_events,
                    'Corr w/ Fatalities': corr_fatalities,
                    'Data Points': len(valid_data)
                })
                corr_df = pd.DataFrame(correlations).sort_values('Corr w/ Events', ascending=False)

        print(corr_df.to_string(index=False))

        return corr_df
    except Exception as e:
        print(f"Error in correlation analysis.")
        print(e)


def time_lag_analysis(corr_df, merged):
    """
    Conducts time lag analysis between ACLED events data and Google trends
    data for most strongly correlated search terms (up to 3).

    For each top correlated search term, looks at a window of -3 to +3 months
    to determine whether search interest leads, lags, or coincides with events.
    Identifies and interprets the lag with the greatest absolute correlation as:
        - reactive if best_lag > 0
        - predictive if best_lag < 0
        - concurrent if best_lag == 0

    Args:
        - corr_df (pd.DataFrame): data frame containg correlation values between
            each search term and ACLED metric, as well as how many data points
            were used in each calculation
        - merged (pd.DataFrame): cleaned and combined dataset with ACLED and
            search interest aligned by month

    Returns:
        - top_terms: the top search terms that were used in time lag analysis
    """
    print("\n" + "=" * 80)
    print("TIME LAG ANALYSIS")
    print("=" * 80)

    try:
        top_terms = corr_df.head(3)['Search Term'].tolist()

        for term in top_terms:
            print(f"\n{term}:")
            valid_data = merged[['EVENTS', term]].dropna()
            best_corr = -999
            best_lag = 0

            for lag in range(-3, 4):
                if lag == 0:
                    corr = valid_data['EVENTS'].corr(valid_data[term])
                elif lag > 0:
                    if len(valid_data) > lag:
                        corr = valid_data['EVENTS'].iloc[lag:].corr(valid_data[term].iloc[:-lag])
                    else:
                        corr = 0
                else:
                    if len(valid_data) > abs(lag):
                        corr = valid_data['EVENTS'].iloc[:lag].corr(valid_data[term].iloc[-lag:])
                    else:
                        corr = 0

                if abs(corr) > abs(best_corr):
                    best_corr = corr
                    best_lag = lag

                direction = "searches LAG" if lag > 0 else ("searches LEAD" if lag < 0 else "CONCURRENT")
                print(f"\tLag {lag:+2d} months ({direction:15s}): correlation = {corr:+.3f}")

            interpretation = "REACTIVE (searches follow events)" if best_lag > 0 else \
                            "PREDICTIVE (searches precede events)" if best_lag < 0 else \
                            "CONCURRENT (searches match events)"
            print(f"\n  → Best correlation at lag {best_lag:+d}: {best_corr:+.3f} ({interpretation})")

        return top_terms
    except Exception as e:
        print(f"Error in time lag analysis.")
        print(e)


def key_periods(top_terms, trends_data, merged):
    """
    Identifies and prints key periods of high conflict activity (top 5 months
    with highest number of ACLED events) and associated search interest.

    Args:
        - top_terms (list): top search terms from correlation analysis
        - trends_data (dict): Dictionary of cleaned Google Trends datasets.
        - merged (pd.DataFrame): cleaned and combined dataset with ACLED and
            search interest aligned by month

    Returns:
        - None
    """
    print("\n" + "="*80)
    print("KEY PERIODS")
    print("="*80)

    print("\nTop 5 Event Spikes:")
    top_spikes = merged.nlargest(5, 'EVENTS')[['month', 'EVENTS', 'FATALITIES'] + list(trends_data.keys())]
    for idx, row in top_spikes.iterrows():
        print(f"\n{row['month'].strftime('%B %Y')}:")
        print(f"  ACLED Events: {row['EVENTS']:,}")
        print(f"  ACLED Fatalities: {row['FATALITIES']:,}")
        print(f"  Search Interest:")
        for term in trends_data.keys():
            if pd.notna(row[term]):
                print(f"    - {term:25s}: {row[term]:.0f}/100")


def visualizations(name, top_terms, merged):
    """
    Uses Altair to create interactive visualizations comparing ACLED event data
    with Google trends over time. Creates a combined multi-series charts
    comparing all metrics and individual comparison charts for each top search
    term.

    Args:
        - name (str): the name of the subject of analysis
        - trends_data (dict): cleaned Google trends data for each search term
        - merged (pd.DataFrame): cleaned and combined dataset with ACLED and
            search interest aligned by month

    Returns:
        - None
    """
    print("\n" + "=" * 80)
    print("CREATING VISUALIZATIONS")
    print("="*80)

    if top_terms is None:
        return None

    # Normalize data
    merged_normalized = merged.copy()
    merged_normalized['EVENTS_norm'] = (merged['EVENTS'] / merged['EVENTS'].max()) * 100
    merged_normalized['FATALITIES_norm'] = (merged['FATALITIES'] / merged['FATALITIES'].max()) * 100

    # Reshape for Altair
    plot_data = []
    for _, row in merged_normalized.iterrows():
        plot_data.append({
            'month': row['month'],
            'metric': 'ACLED Events',
            'value': row['EVENTS_norm'],
            'type': 'Conflict Data',
            'raw_value': row['EVENTS']
        })
        plot_data.append({
            'month': row['month'],
            'metric': 'ACLED Fatalities',
            'value': row['FATALITIES_norm'],
            'type': 'Conflict Data',
            'raw_value': row['FATALITIES']
        })
        for term in top_terms:
            if term in row and pd.notna(row[term]):
                plot_data.append({
                    'month': row['month'],
                    'metric': f'Search: {term}',
                    'value': row[term],
                    'type': 'Google Trends',
                    'raw_value': row[term]
                })

    plot_df = pd.DataFrame(plot_data)

    # Main chart
    chart = alt.Chart(plot_df).mark_line(strokeWidth=2.5, point=True).encode(
        x=alt.X('month:T', title='Month', axis=alt.Axis(format='%b %Y', labelAngle=-45)),
        y=alt.Y('value:Q', title='Normalized Value (0-100)', scale=alt.Scale(domain=[0, 105])),
        color=alt.Color('metric:N', title='Metric', scale=alt.Scale(scheme='tableau10')),
        strokeDash=alt.StrokeDash('type:N', title='Data Type',
                                scale=alt.Scale(domain=['Conflict Data', 'Google Trends'],
                                                range=[[1,0], [5,3]])),
        tooltip=[
            alt.Tooltip('month:T', title='Month', format='%B %Y'),
            alt.Tooltip('metric:N', title='Metric'),
            alt.Tooltip('value:Q', title='Normalized', format='.1f'),
            alt.Tooltip('raw_value:Q', title='Raw Value', format=',.0f')
        ]
    ).properties(
        width=1400,
        height=450,
        title={
            'text': f'{name.title()}: ACLED Events vs Google Search Interest (2020-2025)',
            'fontSize': 18,
            'subtitleFontSize': 13
        }
    ).interactive()

    chart.save(f"{name.replace(' ', '_')}_acled_vs_trends.html")
    print(f"✓ Saved: {name.replace(' ', '_')}_acled_vs_trends.html")


    for term in top_terms:
        term_data = merged[['month', 'EVENTS', 'FATALITIES', term]].dropna().copy()

        base = alt.Chart(term_data).encode(
            x=alt.X('month:T', title='Month', axis=alt.Axis(format='%b %Y', labelAngle=-45))
        )

        events_line = base.mark_line(color='steelblue', strokeWidth=3).encode(
            y=alt.Y('EVENTS:Q', title='ACLED Events', axis=alt.Axis(titleColor='steelblue')),
            tooltip=[
                alt.Tooltip('month:T', title='Month', format='%B %Y'),
                alt.Tooltip('EVENTS:Q', title='Events', format=','),
                alt.Tooltip(f'{term}:Q', title='Search Interest', format='.0f')
            ]
        )

        trends_line = base.mark_line(color='red', strokeWidth=3).encode(
            y=alt.Y(f'{term}:Q', title=f'Google Trends: {term}',
                    axis=alt.Axis(titleColor='red'), scale=alt.Scale(domain=[0, 100])),
            tooltip=[
                alt.Tooltip('month:T', title='Month', format='%B %Y'),
                alt.Tooltip('EVENTS:Q', title='Events', format=','),
                alt.Tooltip(f'{term}:Q', title='Search Interest', format='.0f')
            ]
        )

        term_chart = alt.layer(events_line, trends_line).resolve_scale(
            y='independent'
        ).properties(
            width=1200,
            height=400,
            title=f'{name.title()}: ACLED Events vs "{term}" Search Interest'
        ).interactive()

        filename = f"{name.replace(' ', '_')}_{term.lower().replace(' ', '_')}_comparison.html"
        term_chart.save(filename)
        print(f"✓ Saved: {filename}")

    print(f"\n{name.title()} analysis complete!")
