import os
import pandas as pd
import plotly.express as px
import streamlit as st


# Function to load data
def load_data(input_path):
    try:
        csv_data = pd.read_csv(input_path)
        return csv_data
    except FileNotFoundError:
        st.error("The CSV file was not found. Please check the path and try again.")
        return None


# Function to format numbers with commas for thousands and dots for decimals
def format_number(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# Function for the main dashboard
def salary_dashboard(input_df):
    st.title("Salary Dashboard Analysis")
    st.header("General Statistics")

    # Convert date column
    input_df['date_periodo_di_retribuzione'] = pd.to_datetime(input_df['date_periodo_di_retribuzione'])

    # Date range selection
    st.sidebar.header("Filter by Period")
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        [input_df['date_periodo_di_retribuzione'].min(), input_df['date_periodo_di_retribuzione'].max()]
    )

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

    # Calculate key metrics
    total_gross = filtered_data['totale_competenze'].sum()
    total_deductions = filtered_data['totale_trattenute'].sum()
    total_net = filtered_data['netto_del_mese'].sum()
    average_net = filtered_data['netto_del_mese'].mean()
    accrued_tfr_gross = filtered_data['quota_tfr'].sum()
    total_irpef = filtered_data['irpef_pagata'].sum()
    worked_days = filtered_data['giorni_lavorati'].sum()
    remaining_holidays = round(filtered_data['totale_ferie_rimanenti'].iloc[-1], 2)
    remaining_permissions = round(filtered_data['totale_permessi_rimanenti'].iloc[-1], 2)

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
    st.header("Net Salary Chart")
    df_aggregated = filtered_data.groupby('date_periodo_di_retribuzione', as_index=False).agg({'netto_del_mese': 'sum'})

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
    .drop(columns=['record_key', 'date_periodo_di_retribuzione', 'percentuale_maggiorazione_ore_straordinario']))
    filtered_data.columns = [col.replace('_', ' ').title() for col in filtered_data.columns]

    st.header("Filtered Data Table")
    st.dataframe(filtered_data)


# Function for the "Other Charts" page
def other_charts(input_df):
    st.title("Other Charts - Salary Analysis")
    st.header("Breakdown of Earnings and Deductions")

    total_earnings = input_df['totale_competenze'].sum()
    total_deductions = input_df['totale_trattenute'].sum()

    pie_data = pd.DataFrame({
        "Category": ["Earnings", "Deductions"],
        "Total": [total_earnings, total_deductions]
    })

    fig = px.pie(pie_data, values='Total', names='Category', title="Earnings/Deductions Breakdown")
    st.plotly_chart(fig)


# CSV file path in the resources folder
base_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.join(base_path, "../backend/resources/output_data/salary/salary_history.csv")

# Load data
data = load_data(csv_path)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Salary Dashboard", "Other Charts"])

# Display selected page
if data is not None:
    if page == "Salary Dashboard":
        salary_dashboard(data)
    elif page == "Other Charts":
        other_charts(data)
else:
    st.warning(f"Upload a CSV file to start or check the path: Root: {base_path} - Folder: {csv_path}")
