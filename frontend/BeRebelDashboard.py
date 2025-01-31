import plotly.express as px

from Utils import *


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
