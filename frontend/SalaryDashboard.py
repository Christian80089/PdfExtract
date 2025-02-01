import plotly.express as px

from Utils import *


# Function for the main dashboard
def salary_dashboard(input_df):
    st.title("Salary Dashboard Analysis")
    st.header("General Statistics")

    start_date, end_date = date_range_filter(input_df, "date_periodo_di_retribuzione")
    selected_company = multiselect_from_dataframe(
        "Company",
        input_df,
        "ragione_sociale_azienda",
        sidebar=True,
        default=["Relatech Spa"],
    )

    # Filter data based on date range and company
    dynamic_dataframe = input_df[
        (input_df["date_periodo_di_retribuzione"].between(start_date, end_date))
        & (input_df["ragione_sociale_azienda"].isin(selected_company))
    ]
    dynamic_dataframe = dynamic_dataframe.copy()

    today = pd.Timestamp.today()
    start_of_period = (today - pd.DateOffset(months=7)).replace(day=1)

    static_dataframe = input_df[
        (input_df["date_periodo_di_retribuzione"].between(start_of_period, today))
        & (input_df["ragione_sociale_azienda"].isin(selected_company))
    ]
    static_dataframe = static_dataframe.copy()

    # Calculate and format key metrics
    metrics = {
        "total_gross": dynamic_dataframe["totale_competenze"].sum(),
        "total_deductions": dynamic_dataframe["totale_trattenute"].sum(),
        "total_net": dynamic_dataframe["netto_del_mese"].sum(),
        "average_net": dynamic_dataframe["netto_del_mese"].mean(),
        "accrued_tfr_gross": dynamic_dataframe["quota_tfr"].sum(),
        "total_irpef": dynamic_dataframe["irpef_pagata"].sum(),
        "worked_days": dynamic_dataframe["giorni_lavorati"].sum(),
        "remaining_holidays": (
            round(dynamic_dataframe["totale_ferie_rimanenti"].iloc[-1], 2)
            if not dynamic_dataframe.empty
            else 0
        ),
        "remaining_permissions": (
            round(dynamic_dataframe["totale_permessi_rimanenti"].iloc[-1], 2)
            if not dynamic_dataframe.empty
            else 0
        ),
    }

    formatted_metrics = format_number(
        pd.DataFrame([metrics]), list(metrics.keys())
    ).iloc[0]

    # Display key metrics
    cols = st.columns(3)
    metrics_labels = [
        ("Total Gross Salary (€)", "total_gross"),
        ("Total Deductions (€)", "total_deductions"),
        ("Total Net Salary (€)", "total_net"),
        ("Average Net Salary (€)", "average_net"),
        ("Accrued Gross TFR (€)", "accrued_tfr_gross"),
        ("Total IRPEF Paid (€)", "total_irpef"),
        ("Remaining Holidays (Days)", "remaining_holidays"),
        ("Remaining Permissions (Hours)", "remaining_permissions"),
        ("Total Worked Days", "worked_days"),
    ]

    for i, (label, key) in enumerate(metrics_labels):
        cols[i % 3].metric(
            label,
            f"{formatted_metrics[key]} €" if "€" in label else formatted_metrics[key],
        )

    # Net salary time series chart
    static_dataframe["month"] = (
        static_dataframe["date_periodo_di_retribuzione"].dt.to_period("M").astype(str)
    )
    df_aggregated = static_dataframe.groupby("month", as_index=False)[
        "netto_del_mese"
    ].sum()

    fig = px.bar(
        df_aggregated,
        x="month",
        y="netto_del_mese",
        title="Net Monthly Salary Trend",
        labels={"month": "Period", "netto_del_mese": "Net Salary"},
        color_discrete_sequence=["green"],
    )
    fig.update_traces(texttemplate="%{y:.0f} €", textposition="outside")
    fig.update_layout(xaxis=dict(tickangle=45))
    st.plotly_chart(fig)

    # Filtered data table
    dynamic_dataframe = dynamic_dataframe.sort_values(
        by="date_periodo_di_retribuzione", ascending=False
    ).drop(
        columns=[
            "record_key",
            "date_periodo_di_retribuzione",
            "percentuale_maggiorazione_ore_straordinario",
        ]
    )
    dynamic_dataframe.columns = [
        col.replace("_", " ").title() for col in dynamic_dataframe.columns
    ]

    st.dataframe(dynamic_dataframe)
