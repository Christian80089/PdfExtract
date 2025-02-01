import plotly.express as px

from Utils import *


def bank_transactions_charts(input_df):
    st.title("Bank Transactions Dashboard")
    st.header("General Statistics")

    start_date, end_date = date_range_filter(input_df, "data_operazione")
    selected_categories = multiselect_from_dataframe(
        "Categories", input_df, "causale", sidebar=True, default=["Select All"]
    )

    # Filter data based on date range
    dynamic_dataframe = input_df[
        (input_df["data_operazione"].between(start_date, end_date))
        & (input_df["causale"].isin(selected_categories))
    ]
    dynamic_dataframe = dynamic_dataframe.copy()

    today = pd.Timestamp.today()
    start_of_period = (today - pd.DateOffset(months=6)).replace(day=1)

    static_dataframe = input_df[
        (input_df["data_operazione"].between(start_of_period, today))
        & (input_df["causale"].isin(selected_categories))
    ]
    static_dataframe = static_dataframe.copy()

    # Clean and convert columns
    dynamic_dataframe = clean_and_convert(dynamic_dataframe, ["entrate", "uscite"])
    static_dataframe = clean_and_convert(static_dataframe, ["entrate", "uscite"])

    # Calculate key metrics
    total_income = dynamic_dataframe["entrate"].sum()
    total_expenses = dynamic_dataframe["uscite"].sum()
    balance = total_income + total_expenses

    dynamic_dataframe["month"] = (
        dynamic_dataframe["data_operazione"].dt.to_period("M").astype(str)
    )
    static_dataframe["month"] = (
        static_dataframe["data_operazione"].dt.to_period("M").astype(str)
    )

    monthly_stats = dynamic_dataframe.groupby("month").agg(
        {"entrate": "sum", "uscite": "sum"}
    )
    average_monthly_income = monthly_stats["entrate"].mean()
    average_monthly_expenses = monthly_stats["uscite"].mean()
    average_balance = average_monthly_income + average_monthly_expenses

    # Calculate and format key metrics
    metrics = {
        "Total Income": total_income,
        "Total Expenses": total_expenses,
        "Balance": balance,
        "Average Monthly Income": average_monthly_income,
        "Average Monthly Expenses": average_monthly_expenses,
        "Average Balance": average_balance,
    }

    formatted_metrics = format_number(
        pd.DataFrame([metrics]), list(metrics.keys())
    ).iloc[0]

    cols = st.columns(3)
    metrics_labels = [
        ("Total Income (€)", "Total Income"),
        ("Total Expenses (€)", "Total Expenses"),
        ("Balance (€)", "Balance"),
        ("Average Monthly Income (€)", "Average Monthly Income"),
        ("Average Monthly Expenses (€)", "Average Monthly Expenses"),
        ("Average Balance (€)", "Average Balance"),
    ]

    for i, (label, key) in enumerate(metrics_labels):
        cols[i % 3].metric(label, f"{formatted_metrics[key]} €")

    # Monthly Expenses Trend
    df_aggregated = static_dataframe.groupby("month", as_index=False).agg(
        {"uscite": "sum"}
    )
    fig = px.bar(
        df_aggregated,
        x="month",
        y="uscite",
        title="Monthly Expenses Trend",
        labels={"month": "Period", "uscite": "Expenses (€)"},
        color_discrete_sequence=["red"],
    )

    fig.update_traces(texttemplate="%{y:.2f} €", textposition="outside")
    fig.update_layout(
        xaxis=dict(tickangle=45), yaxis=dict(title="Amount (€)"), bargap=0.2
    )
    st.plotly_chart(fig)

    # Monthly Income Trend
    df_aggregated = static_dataframe.groupby("month", as_index=False).agg(
        {"entrate": "sum"}
    )
    fig = px.bar(
        df_aggregated,
        x="month",
        y="entrate",
        title="Monthly Income Trend",
        labels={"month": "Period", "entrate": "Income (€)"},
        color_discrete_sequence=["green"],
    )

    fig.update_traces(texttemplate="%{y:.2f} €", textposition="outside")
    fig.update_layout(
        xaxis=dict(tickangle=45), yaxis=dict(title="Amount (€)"), bargap=0.2
    )
    st.plotly_chart(fig)

    # Expenses Pie Chart
    df_category_expenses = dynamic_dataframe.groupby("causale", as_index=False).agg(
        {"uscite": "sum"}
    )
    df_category_expenses["uscite"] = df_category_expenses["uscite"].abs()
    df_category_expenses = df_category_expenses[df_category_expenses["uscite"] != 0]
    fig_pie = px.pie(
        df_category_expenses,
        names="causale",
        values="uscite",
        title="Expense Distribution by Category",
        labels={"causale": "Category", "uscite": "Amount (€)"},
        color="causale",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig_pie.update_traces(
        textinfo="percent+label", pull=[0.1] * len(df_category_expenses)
    )
    st.plotly_chart(fig_pie)
