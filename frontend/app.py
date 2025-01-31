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
    df_aggregated = chart_filtered_data.groupby('date_periodo_di_retribuzione', as_index=False).agg({'netto_del_mese': 'sum'})

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

    st.dataframe(filtered_data)


def bank_transactions_charts(input_df):
    st.title("Bank Transactions Dashboard")
    st.header("General Statistics")

    # Convert date column
    input_df['data_operazione'] = pd.to_datetime(input_df['data_operazione'])

    # Date range selection
    st.sidebar.header("Filter by Period")
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        [input_df['data_operazione'].min(), input_df['data_operazione'].max()]
    )

    # Filter by company
    st.sidebar.header("Filter by Category")
    company_options = input_df['causale'].unique()
    select_all_option = "All"
    company_options_with_select_all = [select_all_option] + list(company_options)
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        options=company_options_with_select_all,
        default=select_all_option
    )
    if select_all_option in selected_categories:
        selected_categories = list(company_options)

    # Filter data based on date range and company
    filtered_data = input_df[
        (input_df['data_operazione'] >= pd.to_datetime(start_date)) &
        (input_df['data_operazione'] <= pd.to_datetime(end_date)) &
        (input_df['causale'].isin(selected_categories))
        ]

    today = pd.Timestamp.today()
    six_months_ago = today - pd.DateOffset(months=6)
    start_of_six_months_ago = six_months_ago.replace(day=1)

    chart_filtered_data = input_df[
        (input_df['data_operazione'] >= start_of_six_months_ago) &
        (input_df['data_operazione'] <= today) &
        (input_df['causale'].isin(selected_categories))
        ]

    # Calculate key metrics
    filtered_data['entrate'] = filtered_data['entrate'].str.replace(',', '.', regex=False)
    filtered_data['uscite'] = filtered_data['uscite'].str.replace(',', '.', regex=False)
    filtered_data['entrate'] = pd.to_numeric(filtered_data['entrate'], errors='coerce')
    filtered_data['uscite'] = pd.to_numeric(filtered_data['uscite'], errors='coerce')
    filtered_data['entrate'] = filtered_data['entrate'].fillna(0)
    filtered_data['uscite'] = filtered_data['uscite'].fillna(0)

    chart_filtered_data['entrate'] = chart_filtered_data['entrate'].str.replace(',', '.', regex=False)
    chart_filtered_data['uscite'] = chart_filtered_data['uscite'].str.replace(',', '.', regex=False)
    chart_filtered_data['entrate'] = pd.to_numeric(chart_filtered_data['entrate'], errors='coerce')
    chart_filtered_data['uscite'] = pd.to_numeric(chart_filtered_data['uscite'], errors='coerce')
    chart_filtered_data['entrate'] = chart_filtered_data['entrate'].fillna(0)
    chart_filtered_data['uscite'] = chart_filtered_data['uscite'].fillna(0)

    total_income = filtered_data['entrate'].sum()
    total_expenses = filtered_data['uscite'].sum()
    balance = total_income + total_expenses
    filtered_data['month'] = filtered_data['data_operazione'].dt.to_period('M').astype(str)
    chart_filtered_data['month'] = chart_filtered_data['data_operazione'].dt.to_period('M').astype(str)
    monthly_stats = filtered_data.groupby('month').agg({'entrate': 'sum', 'uscite': 'sum'})
    average_monthly_income = monthly_stats['entrate'].mean()
    average_monthly_expenses = monthly_stats['uscite'].mean()
    average_balance = average_monthly_income + average_monthly_expenses

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"{format_number(total_income)} €")
    col2.metric("Total Expenses", f"{format_number(total_expenses)} €")
    col3.metric("Balance", f"{format_number(balance):} €")

    col4, col5, col6 = st.columns(3)
    col4.metric("Average Monthly Income", f"{format_number(average_monthly_income)} €")
    col5.metric("Average Monthly Expenses", f"{format_number(average_monthly_expenses)} €")
    col6.metric("Avarege Balance", f"{format_number(average_balance):} €")

    # Monthly Expenses Trend
    df_aggregated = chart_filtered_data.groupby('month', as_index=False).agg({'uscite': 'sum'})
    fig = px.bar(
        df_aggregated,
        x='month',
        y='uscite',
        title='Monthly Expenses Trend',
        labels={"month": "Month", "uscite": "Expenses (€)"},
        color_discrete_sequence=["red"]
    )

    fig.update_traces(texttemplate='%{y:.2f} €', textposition='outside')
    fig.update_layout(
        xaxis=dict(tickangle=45),
        yaxis=dict(title="Amount (€)"),
        bargap=0.2
    )
    st.plotly_chart(fig)

    # Monthly Income Trend
    df_aggregated = chart_filtered_data.groupby('month', as_index=False).agg({'entrate': 'sum'})
    fig = px.bar(
        df_aggregated,
        x='month',
        y='entrate',
        title='Monthly Income Trend',
        labels={"month": "Month", "entrate": "Income (€)"},
        color_discrete_sequence=["green"]
    )

    fig.update_traces(texttemplate='%{y:.2f} €', textposition='outside')
    fig.update_layout(
        xaxis=dict(tickangle=45),
        yaxis=dict(title="Amount (€)"),
        bargap=0.2
    )
    st.plotly_chart(fig)

    # Expenses Pie Chart
    df_category_expenses = filtered_data.groupby('causale', as_index=False).agg({'uscite': 'sum'})
    df_category_expenses['uscite'] = df_category_expenses['uscite'].abs()
    df_category_expenses = df_category_expenses[df_category_expenses['uscite'] != 0]
    fig_pie = px.pie(
        df_category_expenses,
        names='causale',
        values='uscite',
        title='Expense Distribution by Category',
        labels={'causale': 'Category', 'uscite': 'Amount (€)'},
        color='causale',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textinfo='percent+label', pull=[0.1] * len(df_category_expenses))
    st.plotly_chart(fig_pie)

def berebel_dashboard(input_df):
    st.title("Berebel Dashboard Analysis")
    st.header("General Statistics")

    # Convert date column
    input_df['date_estratto_conto'] = pd.to_datetime(input_df['date_estratto_conto'])

    # Date range selection
    st.sidebar.header("Filter by Period")
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range",
        [input_df['date_estratto_conto'].min(), input_df['date_estratto_conto'].max()]
    )

    # Filter data based on date range and company
    filtered_data = input_df[
        (input_df['date_estratto_conto'] >= pd.to_datetime(start_date)) &
        (input_df['date_estratto_conto'] <= pd.to_datetime(end_date))
    ]

    today = pd.Timestamp.today()
    twelve_months_ago = today - pd.DateOffset(months=12)
    start_of_twelve_months_ago = twelve_months_ago.replace(day=1)

    chart_filtered_data = input_df[
        (input_df['date_estratto_conto'] >= start_of_twelve_months_ago) &
        (input_df['date_estratto_conto'] <= today)
        ]

    # Calculate key metrics
    travelled_km = filtered_data['km_percorsi'].sum()
    additional_km = filtered_data['km_da_pagare'].sum()
    avg_travelled_km = filtered_data['km_percorsi'].mean()
    total_minimum_monthly = filtered_data['minimo_mensile'].sum()
    total_additional_km_cost = filtered_data['premio_di_conguaglio'].sum()
    total_paid = filtered_data['totale_pagato'].sum()

    # Display key metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Travelled Km", f"{travelled_km}")
    col2.metric("Additional Km", f"{additional_km}")
    col3.metric("Avg Travelled Km", f"{format_number(avg_travelled_km)}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Total Monthly Minimum", f"{format_number(total_minimum_monthly)} €")
    col5.metric("Total Cost Additional Km", f"{format_number(total_additional_km_cost)} €")
    col6.metric("Total Paid", f"{format_number(total_paid)} €")

    df_aggregated = chart_filtered_data.groupby('date_estratto_conto', as_index=False).agg({'km_percorsi': 'sum'})

    fig = px.bar(
        df_aggregated,
        x='date_estratto_conto',
        y='km_percorsi',
        title='Monthly Travelled Km',
        labels={"date_estratto_conto": "Period", "km_percorsi": "Km Travelled"},
        color_discrete_sequence=["lightskyblue"]
    )
    fig.update_traces(text=df_aggregated['km_percorsi'].apply(lambda x: f"{x:,.0f} km"), textposition='outside')
    fig.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig)

    df_aggregated = chart_filtered_data.groupby('date_estratto_conto', as_index=False).agg({'totale_pagato': 'sum'})
    df_aggregated['Budget'] = df_aggregated['totale_pagato'].apply(lambda x: 'OnBudget' if x <= 50 else 'OverBudget')

    fig = px.bar(
        df_aggregated,
        x='date_estratto_conto',
        y='totale_pagato',
        title='Monthly Costs',
        labels={"date_estratto_conto": "Period", "totale_pagato": "Total Paid"},
        color='Budget',
        color_discrete_map={"OnBudget": "green", "OverBudget": "red"}
    )
    fig.update_traces(text=df_aggregated['totale_pagato'].apply(lambda x: f"€ {x:,.2f}"), textposition='outside')
    fig.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig)

    filtered_data['year'] = filtered_data['date_estratto_conto'].dt.to_period('Y').astype(str)
    df_category_expenses = filtered_data.groupby('year', as_index=False).agg({'km_percorsi': 'sum'})

    fig_pie = px.pie(
        df_category_expenses,
        names='year',
        values='km_percorsi',
        title='Yearly Travelled Km',
        labels={'year': 'Year', 'km_percorsi': 'Km Travelled'},
        color='year',
        color_discrete_sequence=px.colors.qualitative.Set2_r
    )
    fig_pie.update_traces(textinfo='percent+label', pull=[0.1] * len(df_category_expenses))
    st.plotly_chart(fig_pie)

    filtered_data['year'] = filtered_data['date_estratto_conto'].dt.to_period('Y').astype(str)
    df_category_expenses = filtered_data.groupby('year', as_index=False).agg({'totale_pagato': 'sum'})

    fig_pie = px.pie(
        df_category_expenses,
        names='year',
        values='totale_pagato',
        title='Yearly Costs Percentage',
        labels={'year': 'Year', 'totale_pagato': 'Total Paid'},
        color='year',
        color_discrete_sequence=px.colors.qualitative.Set2_r
    )
    fig_pie.update_traces(textinfo='percent+label', pull=[0.1] * len(df_category_expenses))
    st.plotly_chart(fig_pie)


# CSV file path in the resources folder
base_path = os.path.abspath(os.path.dirname(__file__))
salary_csv_path = os.path.join(base_path, "../backend/resources/output_data/salary/salary_history.csv")
bank_transactions_ing_csv_path = os.path.join(base_path, "../backend/resources/output_data/bank_transactions/ing/bank_transactions_history.csv")
berebel_csv_path = os.path.join(base_path, "../backend/resources/output_data/berebel/berebel_history.csv")


# Load data
salary_data = load_data(salary_csv_path)
bank_transactions_data = load_data(bank_transactions_ing_csv_path)
berebel_data = load_data(berebel_csv_path)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select Page", ["Salary Dashboard", "Bank Transactions Dashboard", "BeRebel Dashboard"])

# Display selected page
if salary_data is not None:
    if page == "Salary Dashboard":
        salary_dashboard(salary_data)
    elif page == "Bank Transactions Dashboard":
        bank_transactions_charts(bank_transactions_data)
    elif page == "BeRebel Dashboard":
        berebel_dashboard(berebel_data)
else:
    st.warning(f"Upload a CSV file to start or check the path: Root: {base_path} - Folder: {salary_csv_path}")
