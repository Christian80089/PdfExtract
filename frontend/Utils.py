import os

import pandas as pd
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


def get_csv_path(relative_path):
    """Get absolute path for a CSV file in the resources folder."""
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


def date_range_filter(input_df, date_column, sidebar_title="Filter by Period"):
    """Genera un filtro di intervallo di date personalizzabile per Streamlit.

    Args:
        input_df (pd.DataFrame): DataFrame contenente la colonna delle date.
        date_column (str): Nome della colonna delle date.
        sidebar_title (str, optional): Titolo della sezione nella sidebar. Default "Filter by Period".

    Returns:
        tuple: (start_date, end_date) scelti dall'utente.
    """
    st.sidebar.header(sidebar_title)

    # Converti la colonna in formato datetime se non lo è già
    input_df[date_column] = pd.to_datetime(input_df[date_column])

    # Ottieni i limiti delle date disponibili
    min_date, max_date = input_df[date_column].min(), input_df[date_column].max()
    min_year, min_month = min_date.year, min_date.month
    max_year, max_month = max_date.year, max_date.month

    available_years = sorted(input_df[date_column].dt.year.unique(), reverse=True)
    months = list(range(1, 13))

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_year = st.selectbox("Start Year", available_years, key=f"start_year_{date_column}",
                                  index=available_years.index(min_year))
    with col2:
        start_month = st.selectbox(
            "Start Month", months, format_func=lambda x: pd.to_datetime(f"{x}", format="%m").strftime("%B"),
            key=f"start_month_{date_column}", index=min_month - 1
        )

    col3, col4 = st.sidebar.columns(2)
    with col3:
        end_year = st.selectbox("End Year", available_years, key=f"end_year_{date_column}",
                                index=available_years.index(max_year))
    with col4:
        end_month = st.selectbox(
            "End Month", months, format_func=lambda x: pd.to_datetime(f"{x}", format="%m").strftime("%B"),
            key=f"end_month_{date_column}", index=max_month - 1
        )

    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = pd.Timestamp(year=end_year, month=end_month, day=1) + pd.DateOffset(months=1) - pd.DateOffset(days=1)

    if start_date > end_date:
        st.sidebar.error("⚠️ La data di inizio deve essere precedente alla data di fine!")

    return start_date, end_date
