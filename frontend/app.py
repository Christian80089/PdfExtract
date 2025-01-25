import os
import pandas as pd
import plotly.express as px
import streamlit as st

# Percorso del file CSV nella cartella resources
base_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.join(base_path, "../resources/output_data/salary/salary_history.csv")

# Carica il CSV
def load_data():
    try:
        csv_data = pd.read_csv(csv_path)
        return csv_data
    except FileNotFoundError:
        st.error("Il file CSV non è stato trovato. Verifica il percorso e riprova.")
        return None


# Funzione per formattare i numeri con punto per le migliaia e virgola per i decimali
def format_number(value):
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Funzione principale
st.title("Dashboard Analisi Stipendi")
data = load_data()

if data is not None:
    # Conversione della colonna delle date
    data['date_periodo_di_retribuzione'] = pd.to_datetime(data['date_periodo_di_retribuzione'])

    # Selezione del range temporale
    st.sidebar.header("Filtra per periodo")
    start_date, end_date = st.sidebar.date_input(
        "Seleziona il range di date",
        [data['date_periodo_di_retribuzione'].min(), data['date_periodo_di_retribuzione'].max()]
    )

    # Filtro per ragione sociale azienda
    st.sidebar.header("Filtra per azienda")
    azienda_options = data['ragione_sociale_azienda'].unique()
    azienda_selezionata = st.sidebar.selectbox(
        "Seleziona Azienda",
        azienda_options,
        index=list(azienda_options).index("Relatech Spa")  # Imposta "Relatech Spa" come valore predefinito
    )

    # Filtra i dati in base al range di date e azienda
    filtered_data = data[
        (data['date_periodo_di_retribuzione'] >= pd.to_datetime(start_date)) &
        (data['date_periodo_di_retribuzione'] <= pd.to_datetime(end_date)) &
        (data['ragione_sociale_azienda'] == azienda_selezionata)
    ]

    st.header("Statistiche generali")

    # Calcolo delle metriche principali
    totale_netto = filtered_data['netto_del_mese'].sum()
    media_netto = filtered_data['netto_del_mese'].mean()
    totale_lordo = filtered_data['totale_competenze'].sum()
    media_ore_lavorate = filtered_data['ore_lavorate'].mean()
    totale_straordinari = filtered_data['ore_straordinarie'].sum()
    totale_irpef = filtered_data['irpef_pagata'].sum()
    ferie_rimanenti = round(filtered_data['totale_ferie_rimanenti'].iloc[-1], 2)
    permessi_rimanenti = round(filtered_data['totale_permessi_rimanenti'].iloc[-1], 2)

    # Visualizzazione delle metriche principali
    col1, col2, col3 = st.columns(3)
    col1.metric("Totale Stipendio Netto", f"{format_number(totale_netto)} €")
    col2.metric("Media Stipendio Netto", f"{format_number(media_netto)} €")
    col3.metric("Totale Retribuzione Lorda", f"{format_number(totale_lordo)} €")

    col4, col5, col6 = st.columns(3)
    col4.metric("Ferie Rimanenti (Giorni)", format_number(ferie_rimanenti))
    col5.metric("Permessi Rimanenti (Ore)", format_number(permessi_rimanenti))
    col6.metric("Totale IRPEF Pagata", f"{format_number(totale_irpef)} €")

    st.header("Grafico temporale dello stipendio netto")

    # Grafico temporale dello stipendio netto
    fig = px.line(
        filtered_data,
        x='date_periodo_di_retribuzione',
        y='netto_del_mese',
        title='Andamento dello Stipendio Netto Mensile',
        labels={"date_periodo_di_retribuzione": "Periodo", "netto_del_mese": "Stipendio Netto"}
    )
    st.plotly_chart(fig)

    st.header("Ripartizione tra competenze e trattenute")

    # Grafico a torta tra competenze e trattenute
    totale_competenze = filtered_data['totale_competenze'].sum()
    totale_trattenute = filtered_data['totale_trattenute'].sum()
    pie_data = pd.DataFrame({
        "Categoria": ["Competenze", "Trattenute"],
        "Totale": [totale_competenze, totale_trattenute]
    })
    fig3 = px.pie(pie_data, values='Totale', names='Categoria', title='Ripartizione tra Competenze e Trattenute')
    st.plotly_chart(fig3)
else:
    st.warning("Carica un file CSV per iniziare.")
