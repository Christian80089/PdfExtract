bank_copilot_info_to_extract = [
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

bank_df_mandatory_fields = [
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

bank_df_columns_to_select = [
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

bank_df_schema = {
    "record_key": str,
    "banca": str,
    "numero_conto_corrente": str,
    "data_estratto_conto": object,
    "codice_iban": str,
    "data_operazione": object,
    "uscite": float,
    "entrate": float,
    "descrizione": str,
    "causale": str,
    "note": str
}

bank_postgresql_table_name = "movimenti_banca_history"

bank_postgresql_table_schema = """
CREATE TABLE IF NOT EXISTS movimenti_banca_history (
    record_key VARCHAR, 
    banca VARCHAR,
    numero_conto_corrente VARCHAR,
    data_estratto_conto DATE,
    codice_iban VARCHAR,
    data_operazione DATE,
    uscite FLOAT,
    entrate FLOAT,
    descrizione VARCHAR,
    causale VARCHAR,
    note VARCHAR
);
"""

bank_postgresql_insert_query = """
INSERT INTO movimenti_banca_history (
    record_key, banca, numero_conto_corrente, data_estratto_conto,
    codice_iban, data_operazione, uscite,
    entrate, descrizione, causale, note
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""

bank_airtable_ing_table_name = "tblRwAoWEmI3RrxPh"

bank_airtable_deutsche_table_name = "tblB7XCUmNxnF38AT"

bank_key_field = "record_key"
