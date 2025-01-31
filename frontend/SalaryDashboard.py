import plotly.express as px

from Utils import *


# Function for the main dashboard
def salary_dashboard(input_df):
    st.title("Salary Dashboard Analysis")
    st.header("General Statistics")

    # Convert date column
    input_df['date_periodo_di_retribuzione'] = pd.to_datetime(input_df['date_periodo_di_retribuzione'])

    # Date range selection
    st.sidebar.header("Filter by Period")
    min_date = input_df['date_periodo_di_retribuzione'].min()
    max_date = input_df['date_periodo_di_retribuzione'].max()
    min_year, min_month = min_date.year, min_date.month
    max_year, max_month = max_date.year, max_date.month

    available_years = sorted(input_df['date_periodo_di_retribuzione'].dt.year.unique(), reverse=True)
    months = list(range(1, 13))

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_year = st.selectbox("Start Year", available_years, key="start_year",
                                  index=available_years.index(min_year))
    with col2:
        start_month = st.selectbox(
            "Start Month", months, format_func=lambda x: pd.to_datetime(f"{x}", format="%m").strftime("%B"),
            key="start_month", index=min_month - 1
        )
    col3, col4 = st.sidebar.columns(2)
    with col3:
        end_year = st.selectbox("End Year", available_years, key="end_year", index=available_years.index(max_year))
    with col4:
        end_month = st.selectbox(
            "End Month", months, format_func=lambda x: pd.to_datetime(f"{x}", format="%m").strftime("%B"),
            key="end_month", index=max_month - 1
        )
    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)

    if start_date > end_date:
        st.sidebar.error("⚠️ La data di inizio deve essere precedente alla data di fine!")

    # Filter by company
    st.sidebar.header("Filter by Company")
    company_options = input_df['ragione_sociale_azienda'].unique()
    selected_company = st.sidebar.selectbox(
        "Select Company",
        company_options,
        index=list(company_options).index("Relatech Spa") if "Relatech Spa" in company_options else 0
    )

    # Filter data based on date range and company
    filtered_data = input_df[
        (input_df['date_periodo_di_retribuzione'] >= pd.to_datetime(start_date)) &
        (input_df['date_periodo_di_retribuzione'] <= pd.to_datetime(end_date)) &
        (input_df['ragione_sociale_azienda'] == selected_company)
        ]

    today = pd.Timestamp.today()
    six_months_ago = today - pd.DateOffset(months=6)
    start_of_six_months_ago = six_months_ago.replace(day=1)

    chart_filtered_data = input_df[
        (input_df['date_periodo_di_retribuzione'] >= start_of_six_months_ago) &
        (input_df['date_periodo_di_retribuzione'] <= today) &
        (input_df['ragione_sociale_azienda'] == selected_company)
        ]

    # Calculate key metrics
    total_gross = filtered_data['totale_competenze'].sum()
    total_deductions = filtered_data['totale_trattenute'].sum()
    total_net = filtered_data['netto_del_mese'].sum()
    average_net = filtered_data['netto_del_mese'].mean()
    accrued_tfr_gross = filtered_data['quota_tfr'].sum()
    total_irpef = filtered_data['irpef_pagata'].sum()
    worked_days = filtered_data['giorni_lavorati'].sum()
    if not filtered_data.empty:
        remaining_holidays = round(filtered_data['totale_ferie_rimanenti'].iloc[-1], 2)
        remaining_permissions = round(filtered_data['totale_permessi_rimanenti'].iloc[-1], 2)
    else:
        remaining_holidays = 0  # Valore di default se non ci sono dati
        remaining_permissions = 0

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Gross Salary", f"{format_number(total_gross)} €")
    col2.metric("Total Deductions", f"{format_number(total_deductions)} €")
    col3.metric("Total Net Salary", f"{format_number(total_net)} €")

    col4, col5, col6 = st.columns(3)
    col4.metric("Average Net Salary", f"{format_number(average_net)} €")
    col5.metric("Accrued Gross TFR", f"{format_number(accrued_tfr_gross)} €")
    col6.metric("Total IRPEF Paid", f"{format_number(total_irpef)} €")

    col7, col8, col9 = st.columns(3)
    col7.metric("Remaining Holidays (Days)", format_number(remaining_holidays))
    col8.metric("Remaining Permissions (Hours)", format_number(remaining_permissions))
    col9.metric("Total Worked Days", format_number(worked_days))

    # Net salary time series chart
    df_aggregated = chart_filtered_data.groupby('date_periodo_di_retribuzione', as_index=False).agg(
        {'netto_del_mese': 'sum'})

    fig = px.bar(
        df_aggregated,
        x='date_periodo_di_retribuzione',
        y='netto_del_mese',
        title='Net Monthly Salary Trend',
        labels={"date_periodo_di_retribuzione": "Period", "netto_del_mese": "Net Salary"},
        color_discrete_sequence=["green"]
    )
    fig.update_traces(text=df_aggregated['netto_del_mese'], textposition='outside')
    fig.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig)

    # Filtered data table
    filtered_data = (filtered_data
    .sort_values(by='date_periodo_di_retribuzione', ascending=False)
    .drop(
        columns=['record_key', 'date_periodo_di_retribuzione', 'percentuale_maggiorazione_ore_straordinario']))
    filtered_data.columns = [col.replace('_', ' ').title() for col in filtered_data.columns]

    st.dataframe(filtered_data)
