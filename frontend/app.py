import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Percorso del file CSV nella cartella resources
base_path = os.path.abspath(os.path.dirname(__file__))
csv_path = os.path.join(base_path, "../resources/output_data/salary/salary_history.csv")

# Carica il CSV
def load_data():
    try:
        data = pd.read_csv(csv_path)
        return data
    except FileNotFoundError:
        st.error("Il file CSV non è stato trovato. Verifica il percorso e riprova.")
        return None

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

    # Filtra i dati
    filtered_data = data[(data['date_periodo_di_retribuzione'] >= pd.to_datetime(start_date)) &
                         (data['date_periodo_di_retribuzione'] <= pd.to_datetime(end_date))]

    st.header("Statistiche generali")

    # Calcolo delle metriche principali
    totale_netto = filtered_data['netto_del_mese'].sum()
    media_netto = filtered_data['netto_del_mese'].mean()
    totale_lordo = filtered_data['totale_competenze'].sum()
    media_ore_lavorate = filtered_data['ore_lavorate'].mean()
    totale_straordinari = filtered_data['ore_straordinarie'].sum()
    totale_irpef = filtered_data['irpef_pagata'].sum()
    ferie_rimanenti = filtered_data['totale_ferie_rimanenti'].iloc[-1]
    permessi_rimanenti = filtered_data['totale_permessi_rimanenti'].iloc[-1]

    # Visualizzazione delle metriche principali
    col1, col2, col3 = st.columns(3)
    col1.metric("Totale Stipendio Netto", f"{totale_netto:,.2f} €")
    col2.metric("Media Stipendio Netto", f"{media_netto:,.2f} €")
    col3.metric("Totale Retribuzione Lorda", f"{totale_lordo:,.2f} €")

    col4, col5, col6 = st.columns(3)
    col4.metric("Media Ore Lavorate", f"{media_ore_lavorate:,.2f}")
    col5.metric("Totale Ore Straordinarie", f"{totale_straordinari:,.2f}")
    col6.metric("Totale IRPEF Pagata", f"{totale_irpef:,.2f} €")

    col7, col8 = st.columns(2)
    col7.metric("Ferie Rimanenti", ferie_rimanenti)
    col8.metric("Permessi Rimanenti", permessi_rimanenti)

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

    st.header("Grafico temporale delle ore lavorate e straordinarie")

    # Grafico temporale delle ore lavorate e straordinarie
    fig2 = px.bar(
        filtered_data,
        x='date_periodo_di_retribuzione',
        y=['ore_lavorate', 'ore_straordinarie'],
        title='Confronto tra Ore Lavorate e Straordinarie',
        labels={"value": "Ore", "date_periodo_di_retribuzione": "Periodo"},
        barmode='group'
    )
    st.plotly_chart(fig2)

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
