import pandas as pd
import streamlit as st

# Titolo dell'app
st.title("La mia dashboard con Streamlit")

csv_path = ""
# Generazione di un dataframe di esempio
df = pd.read_csv(csv_path, delimiter=';', header=0)

# Visualizzazione del dataframe
st.write(df)

# Un semplice grafico
st.line_chart(df)
