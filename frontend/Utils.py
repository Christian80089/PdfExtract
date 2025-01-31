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
