import pandas as pd
import altair as alt

def country_analysis(country_name, trends_files):
    """
    docstringgg
    """
    print("=" * 80)
    print(f"{country_name} analysis")
    print("=" * 80)

    # FLILTER ACLED DATA
    # ------------------
    country_acled = acled[
        (acled['COUNTRY'] == country_name) &
        (acled['WEEK'] >= '2020-01-01')
    ].copy()

    country_acled['month'] = country_acled['WEEK'].dt.to_period('M').dt.to_timestamp()
    country_monthly = country_acled.groupby('month').agg({
        'EVENTS': 'sum',
        'FATALITIES': 'sum'
    })

    print(f"ACLED data: {len(country_monthly)} months")
    print(f"Date range: {country_monthly['month'].min()} to {country_monthly['month'].max()}")
    print(f"Total events: {country_monthly['EVENTS'].sum():,}")
    print(f"Total fatalities: {country_monthly['FATALITIES'].sum():,}")

    # LOAD GOOGLE TRENDS FILES
    # ------------------------
    trends_data = {}
    for name, path in trends_files.items():
        try:
            df = pd.read_csv(filepath, skiprows = 1)
            df.columns = ['month', 'value']
            df['month'] = pd.to_datetime(df['month'])
            df['value'] = df['value'].replace('<1', '0.5')
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            trends_data[name] = df
            print(f"Loaded: {name:25s} - {len(df)} months, max={df['value'].max()}")
        except Exception as e:
            print(f"    ERROR LOADING {name}: {e}")

    # MERGE DATASETS
    # --------------
    merged = country_monthly.copy()
    for name, df in trends_data.items():
        merged = merged.merge(
            df.rename(columns={'value': name}),
            on='month',
            how='left'
        )
    print(f"\nMerged dataset: {len(merged)} months with {len(trends_data)} search terms")


def corr_analysis(country_name, trends_data, merged):
    """
    docstringgg
    """
    print("=" * 80)
    print("CORRELATION ANALYSIS")
    print("=" * 80)

    correlations = []
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
    print("\n" + f"{country_name}".to_string(index=False))


def time_lag_analysis(corr_df):
    """
    docstringgg
    """
    print("=" * 80)
    print("TIME LAG ANALYSIS")
    print("=" * 80)

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


def visualizations(country_name, merged, top_terms):
    """
    docstringgg
    """
    print("\n" + "="*80)
    print("CREATING VISUALIZATIONS")
    print("="*80)

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
            'text': '{country_name}: ACLED Events vs Google Search Interest (2020-2025)',
            'fontSize': 18,
            'subtitleFontSize': 13
        }
    ).interactive()

    chart.save(f"{country_name}_acled_vs_trends.html")
    print(f"✓ Saved: {country_name}_acled_vs_trends.html")

    # Display
    show(chart)


def comparison_charts(top_terms):
    """
    docstringgg
    """
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
            title=f'{country_name}: ACLED Events vs "{term}" Search Interest'
        ).interactive()
    
        filename = f"{country_name}_{term.lower().replace(' ', '_')}_comparison.html"
        term_chart.save(filename)
        print(f"✓ Saved: {filename}")

    print(f"\n{country_name} analysis complete!")
