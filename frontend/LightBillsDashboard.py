import plotly.express as px

from Utils import *


# Function for the main dashboard
def light_bills_dashboard(input_df):
    st.title("Ligh Bills Dashboard")
    st.header("General Statistics")

    start_date, end_date = date_range_filter(input_df, "data_fattura")
    selected_supplier = multiselect_from_dataframe(
        "Supplier",
        input_df,
        "fornitore",
        sidebar=True,
        default=["Select All"],
    )

    # Filter data based on date range and company
    dynamic_dataframe = input_df[
        (input_df["data_fattura"].between(start_date, end_date))
        & (input_df["fornitore"].isin(selected_supplier))
    ]
    dynamic_dataframe = dynamic_dataframe.copy()

    today = pd.Timestamp.today()
    start_of_period = (today - pd.DateOffset(months=12)).replace(day=1)

    static_dataframe = input_df[
        (input_df["data_fattura"].between(start_of_period, today))
        & (input_df["fornitore"].isin(selected_supplier))
    ]
    static_dataframe = static_dataframe.copy()

    # Clean and convert columns
    dynamic_dataframe = clean_and_convert(
        dynamic_dataframe,
        [
            "prezzo_unitario_kWh",
            "totale_da_pagare",
            "canone_tv",
            "spese_per_energia",
            "spese_trasporto_gestione_contatore",
            "spese_oneri",
            "altre_partite",
            "imposte_iva",
        ],
    )
    static_dataframe = clean_and_convert(
        static_dataframe,
        [
            "prezzo_unitario_kWh",
            "totale_da_pagare",
            "canone_tv",
            "spese_per_energia",
            "spese_trasporto_gestione_contatore",
            "spese_oneri",
            "altre_partite",
            "imposte_iva",
        ],
    )

    # Calculate and format key metrics
    metrics = {
        "total_paid": dynamic_dataframe["totale_da_pagare"].sum(),
        "total_kw_consumed": dynamic_dataframe["kWh_consumati_totali"].sum(),
        "total_tv_paid": dynamic_dataframe["canone_tv"].sum(),
        "only_energy_paid": dynamic_dataframe["spese_per_energia"].sum(),
        "only_transport_meter_paid": dynamic_dataframe[
            "spese_trasporto_gestione_contatore"
        ].sum(),
        "total_taxes": dynamic_dataframe["imposte_iva"].sum(),
        "total_charges": dynamic_dataframe["spese_oneri"].sum(),
        "other_costs": dynamic_dataframe["altre_partite"].sum(),
        "unitary_cost_kw": (
            round(
                float(
                    dynamic_dataframe["prezzo_unitario_kWh"].iloc[-1]
                ),
                5,
            )
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
        ("Total Paid (€)", "total_paid"),
        ("Total kilowatt Consumed (kWh)", "total_kw_consumed"),
        ("Total TV Paid (€)", "total_tv_paid"),
        ("Only Energy Paid (€)", "only_energy_paid"),
        ("Only Transport and Meter Paid (€)", "only_transport_meter_paid"),
        ("Total Taxes (€)", "total_taxes"),
        ("Total Charges (€)", "total_charges"),
        ("Other Costs (€)", "other_costs"),
        ("Unitary Cost kW/h (€)", "unitary_cost_kw"),
    ]

    for i, (label, key) in enumerate(metrics_labels):
        cols[i % 3].metric(
            label,
            f"{formatted_metrics[key]} €" if "€" in label else formatted_metrics[key],
        )

    # Net salary time series chart
    static_dataframe["month"] = (
        static_dataframe["data_fattura"].dt.to_period("M").astype(str)
    )
    
    df_aggregated = static_dataframe[
        (static_dataframe["kWh_F1_consumati"] != 0) |
        (static_dataframe["kWh_F2_consumati"] != 0) |
        (static_dataframe["kWh_F3_consumati"] != 0)
    ]

    fig = px.bar(
        df_aggregated,
        x="periodo_fornitura",
        y=["kWh_F1_consumati", "kWh_F2_consumati", "kWh_F3_consumati"],
        title="Consumption Trend",
        labels={"periodo_fornitura": "Supply Period", "value": "Consumption"},
        color_discrete_sequence=["orange", "yellow", "lightyellow"],
    )
    
    fig.for_each_trace(lambda t: t.update(name={
        "kWh_F1_consumati": "F1 Consumed",
        "kWh_F2_consumati": "F2 Consumed",
        "kWh_F3_consumati": "F3 Consumed"
    }[t.name]))
    
    fig.update_traces(texttemplate="%{y:.0f}", textposition="outside")
    fig.update_layout(xaxis=dict(tickangle=45), barmode='group')
    st.plotly_chart(fig)
    
    fig = px.bar(
        df_aggregated,
        x="periodo_fornitura",
        y=["kWh_consumati_totali", "spese_per_energia"],
        title="Comparison Consumption Trend",
        labels={"periodo_fornitura": "Supply Period", "value": "Consumption"},
        color_discrete_sequence=["orange", "yellow"],
    )
    
    fig.for_each_trace(lambda t: t.update(name={
        "kWh_consumati_totali": "Total kW/h Consumed",
        "spese_per_energia": "Energy Costs €"
    }[t.name]))
    
    fig.update_traces(texttemplate="%{y:.2f}", textposition="inside")
    fig.update_layout(xaxis=dict(tickangle=45), barmode='group')
    st.plotly_chart(fig)
    
    dynamic_dataframe['numero_fattura'] = dynamic_dataframe['numero_fattura'].astype(str)
    dynamic_dataframe = dynamic_dataframe.sort_values(
        by="data_fattura", ascending=False
    )
    dynamic_dataframe.columns = [
        col.replace("_", " ").title() for col in dynamic_dataframe.columns
    ]

    st.dataframe(dynamic_dataframe)