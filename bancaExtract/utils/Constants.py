import pandas as pd

info_to_extract = [
    "banca (è una stringa ed è mandatory)",
    "numero_conto_corrente (estrailo come stringa)",
    "data_estratto_conto (è una data, deve estrarla in questo formato yyyy-mm-dd)",
    "codice_iban",
    "data_operazione (è una data, deve estrarla in questo formato yyyy-mm-dd)",
    "uscite (valori double)",
    "entrate (valori double)",
    "descrizione (estrai una breve descrizione che abbia senso per ogni movimento)",
    "causale (prova a categorizzare il movimento dell'estratto conto)"
]

mandatory_fields = [
    "banca",
    "numero_conto_corrente",
    "data_estratto_conto",
    "codice_iban",
    "data_operazione",
    "uscite",
    "entrate",
    "descrizione",
    "causale"
]

columns_to_select = [
    "record_key",
    "banca",
    "numero_conto_corrente",
    "data_estratto_conto",
    "codice_iban",
    "data_operazione",
    "uscite",
    "entrate",
    "descrizione",
    "causale",
    "note"
]

schema = {
    "record_key": str,
    "banca": str,
    "numero_conto_corrente": str,
    "data_estratto_conto": "datetime64[ns]",
    "codice_iban": str,
    "data_operazione": "datetime64[ns]",
    "uscite": float,
    "entrate": float,
    "descrizione": str,
    "causale": str,
    "note": str
}

# Valori predefiniti per i tipi
default_values = {
    str: "",
    "datetime64[ns]": pd.NaT,
    float: 0.0,
    int: 0
}

# Dettagli di connessione al database
TABLE_NAME = "movimenti_banca_history"

# Schema della tabella
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS movimenti_banca_history (
    record_key VARCHAR, 
    banca VARCHAR,
    numero_conto_corrente VARCHAR,
    data_estratto_conto TIMESTAMP,
    codice_iban VARCHAR,
    data_operazione TIMESTAMP,
    uscite FLOAT,
    entrate FLOAT,
    descrizione VARCHAR,
    causale VARCHAR,
    note VARCHAR
);
"""

# Query di inserimento
insert_query = """
INSERT INTO movimenti_banca_history (
    record_key, banca, numero_conto_corrente, data_estratto_conto,
    codice_iban, data_operazione, uscite,
    entrate, descrizione, causale, note
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""

# AirTable Constants
table_name = "tblRwAoWEmI3RrxPh"

key_field = "record_key"
