import plotly.express as px

from Utils import *


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

    chart_filtered_data = chart_filtered_data.copy()

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
