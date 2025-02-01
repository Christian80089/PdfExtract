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


def format_number(df, columns, decimals=2):
    """Formats the selected columns with commas for thousands and dots for decimals.

    Args:
        df (pd.DataFrame): DataFrame containing the columns to format.
        columns (list): List of columns to format.
        decimals (int, optional): Number of decimals to display. Default = 2.

    Returns:
        pd.DataFrame: DataFrame with columns formatted to the specified number of decimals.
    """
    df = df.copy()
    for col in columns:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: (
                    f"{x:,.{decimals}f}".replace(",", "_")
                    .replace(".", ",")
                    .replace("_", ".")
                    if pd.notnull(x)
                    else None
                )
            )
    return df


def get_csv_path(relative_path):
    """Get absolute path for a CSV file in the resources folder."""
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


def date_range_filter(input_df, date_column, sidebar_title="Filter by Period"):
    """Generates a customizable date range filter for Streamlit.

    Args:
        input_df (pd.DataFrame): DataFrame containing the date column.
        date_column (str): Name of the date column.
        sidebar_title (str, optional): Title of the section in the sidebar. Default "Filter by Period".

    Returns:
        tuple: (start_date, end_date) chosen by the user.
    """
    st.sidebar.header(sidebar_title)

    # Convert the column to datetime format if it is not already
    input_df[date_column] = pd.to_datetime(input_df[date_column])

    # Get the limits of the available dates
    min_date, max_date = input_df[date_column].min(), input_df[date_column].max()
    min_year, min_month = min_date.year, min_date.month
    max_year, max_month = max_date.year, max_date.month

    available_years = sorted(input_df[date_column].dt.year.unique(), reverse=True)
    months = list(range(1, 13))

    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_year = st.selectbox(
            "Start Year",
            available_years,
            key=f"start_year_{date_column}",
            index=available_years.index(min_year),
        )
    with col2:
        start_month = st.selectbox(
            "Start Month",
            months,
            format_func=lambda x: pd.to_datetime(f"{x}", format="%m").strftime("%B"),
            key=f"start_month_{date_column}",
            index=min_month - 1,
        )

    col3, col4 = st.sidebar.columns(2)
    with col3:
        end_year = st.selectbox(
            "End Year",
            available_years,
            key=f"end_year_{date_column}",
            index=available_years.index(max_year),
        )
    with col4:
        end_month = st.selectbox(
            "End Month",
            months,
            format_func=lambda x: pd.to_datetime(f"{x}", format="%m").strftime("%B"),
            key=f"end_month_{date_column}",
            index=max_month - 1,
        )

    start_date = pd.Timestamp(year=start_year, month=start_month, day=1)
    end_date = (
        pd.Timestamp(year=end_year, month=end_month, day=1)
        + pd.DateOffset(months=1)
        - pd.DateOffset(days=1)
    )

    if start_date > end_date:
        st.sidebar.error("⚠️ The start date must be earlier than the end date!")

    return start_date, end_date


def add_date_features(df, date_column):
    """Adds derived columns from the date for advanced analysis.

    Args:
        df (pd.DataFrame): DataFrame containing the date column.
        date_column (str): Name of the date column.

    Returns:
        pd.DataFrame: DataFrame with new derived columns from the date.
    """
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])  # Ensure it is datetime

    # Adding new useful columns
    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month
    df["month_name"] = df[date_column].dt.strftime("%B")
    df["day"] = df[date_column].dt.day
    df["weekday"] = df[date_column].dt.dayofweek  # 0=Monday, 6=Sunday
    df["weekday_name"] = df[date_column].dt.strftime("%A")
    df["quarter"] = df[date_column].dt.quarter
    df["semester"] = df["quarter"].apply(lambda x: 1 if x in [1, 2] else 2)
    df["year_month"] = df[date_column].dt.to_period("M").astype(str)  # Format YYYY-MM

    return df


import streamlit as st
import pandas as pd


def multiselect_from_dataframe(label, df, column, sidebar=True, default=None):
    """Creates a multi-select dropdown with a 'Select All' option based on a column from a DataFrame.

    Args:
        label (str): Name of the filter.
        df (pd.DataFrame): DataFrame containing the column with options.
        column (str): Name of the column to extract unique values from.
        sidebar (bool, optional): If True, display in the sidebar. Default = True.
        default (list, optional): Default selected options. Default = None.

    Returns:
        list: List of selected items.
    """
    if column not in df.columns:
        st.error(f"⚠️ The column '{column}' does not exist in the DataFrame!")
        return []

    # Get unique sorted values
    options = sorted(df[column].dropna().unique())
    select_all_option = "Select All"
    options_with_all = [select_all_option] + options

    # If no default value is provided, use "Select All"
    default = default if default is not None else [select_all_option]

    # Create the multiselect
    if sidebar:
        selected = st.sidebar.multiselect(label, options_with_all, default=default)
    else:
        selected = st.multiselect(label, options_with_all, default=default)

    # If "Select All" is chosen, return all options
    if select_all_option in selected:
        return options

    return selected


# Helper function to clean and convert columns
def clean_and_convert(df, columns):
    for col in columns:
        df[col] = df[col].str.replace(",", ".", regex=False).astype(float).fillna(0)
    return df
