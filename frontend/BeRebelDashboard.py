import plotly.express as px

from Utils import *


def berebel_dashboard(input_df):
    st.title("Berebel Dashboard")
    st.header("General Statistics")

    start_date, end_date = date_range_filter(input_df, "date_estratto_conto")

    # Filter data based on date range and company
    dynamic_dataframe = input_df[
        (input_df["date_estratto_conto"].between(start_date, end_date))
    ]

    today = pd.Timestamp.today()
    start_of_period = (today - pd.DateOffset(months=7)).replace(day=1)

    static_dataframe = input_df[
        (input_df["date_estratto_conto"].between(start_of_period, today))
    ]

    # Calculate key metrics
    metrics = {
        "Travelled Km": dynamic_dataframe["km_percorsi"].sum(),
        "Additional Km": dynamic_dataframe["km_da_pagare"].sum(),
        "Avg Travelled Km": dynamic_dataframe["km_percorsi"].mean(),
        "Total Monthly Minimum": dynamic_dataframe["minimo_mensile"].sum(),
        "Total Cost Additional Km": dynamic_dataframe["premio_di_conguaglio"].sum(),
        "Total Paid": dynamic_dataframe["totale_pagato"].sum(),
    }

    formatted_metrics = format_number(
        pd.DataFrame([metrics]), list(metrics.keys())
    ).iloc[0]

    # Display key metrics
    cols = st.columns(3)
    metrics_labels = [
        ("Travelled Km", "Travelled Km"),
        ("Additional Km", "Additional Km"),
        ("Avg Travelled Km", "Avg Travelled Km"),
        ("Total Monthly Minimum (€)", "Total Monthly Minimum"),
        ("Total Cost Additional Km (€)", "Total Cost Additional Km"),
        ("Total Paid (€)", "Total Paid"),
    ]

    for i, (label, key) in enumerate(metrics_labels):
        cols[i % 3].metric(
            label,
            f"{formatted_metrics[key]} €" if "€" in label else formatted_metrics[key],
        )

    df_aggregated = static_dataframe.groupby("date_estratto_conto", as_index=False).agg(
        {"km_percorsi": "sum"}
    )

    fig = px.bar(
        df_aggregated,
        x="date_estratto_conto",
        y="km_percorsi",
        title="Monthly Travelled Km",
        labels={"date_estratto_conto": "Period", "km_percorsi": "Km Travelled"},
        color_discrete_sequence=["lightskyblue"],
    )
    fig.update_traces(
        text=df_aggregated["km_percorsi"].apply(lambda x: f"{x:,.0f} km"),
        textposition="outside",
    )
    fig.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig)

    df_aggregated = static_dataframe.groupby("date_estratto_conto", as_index=False).agg(
        {"totale_pagato": "sum"}
    )
    df_aggregated["Budget"] = df_aggregated["totale_pagato"].apply(
        lambda x: "OnBudget" if x <= 50 else "OverBudget"
    )

    fig = px.bar(
        df_aggregated,
        x="date_estratto_conto",
        y="totale_pagato",
        title="Monthly Costs",
        labels={"date_estratto_conto": "Period", "totale_pagato": "Total Paid"},
        color="Budget",
        color_discrete_map={"OnBudget": "green", "OverBudget": "red"},
    )
    fig.update_traces(
        text=df_aggregated["totale_pagato"].apply(lambda x: f"€ {x:,.2f}"),
        textposition="outside",
    )
    fig.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig)

    dynamic_dataframe["year"] = (
        dynamic_dataframe["date_estratto_conto"].dt.to_period("Y").astype(str)
    )
    df_category_expenses = dynamic_dataframe.groupby("year", as_index=False).agg(
        {"km_percorsi": "sum"}
    )

    fig_pie = px.pie(
        df_category_expenses,
        names="year",
        values="km_percorsi",
        title="Yearly Travelled Km",
        labels={"year": "Year", "km_percorsi": "Km Travelled"},
        color="year",
        color_discrete_sequence=px.colors.qualitative.Set2_r,
    )
    fig_pie.update_traces(
        textinfo="percent+label", pull=[0.1] * len(df_category_expenses)
    )
    st.plotly_chart(fig_pie)

    dynamic_dataframe["year"] = (
        dynamic_dataframe["date_estratto_conto"].dt.to_period("Y").astype(str)
    )
    df_category_expenses = dynamic_dataframe.groupby("year", as_index=False).agg(
        {"totale_pagato": "sum"}
    )

    fig_pie = px.pie(
        df_category_expenses,
        names="year",
        values="totale_pagato",
        title="Yearly Costs Percentage",
        labels={"year": "Year", "totale_pagato": "Total Paid"},
        color="year",
        color_discrete_sequence=px.colors.qualitative.Set2_r,
    )
    fig_pie.update_traces(
        textinfo="percent+label", pull=[0.1] * len(df_category_expenses)
    )
    st.plotly_chart(fig_pie)
