import numpy as np
import pandas as pd
import streamlit as st

# Titolo dell'app
st.title("La mia dashboard con Streamlit")

# Generazione di un dataframe di esempio
df = pd.DataFrame({
    'A': np.random.rand(10),
    'B': np.random.rand(10)
})

# Visualizzazione del dataframe
st.write(df)

# Un semplice grafico
st.line_chart(df)
