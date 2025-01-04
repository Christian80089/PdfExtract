import pandas as pd

info_to_extract = [
    "fornitore (è una stringa ed è mandatory)",
    "numero_fattura (è una stringa ed è mandatory, è il riferimento della bolletta)",
    "data_fattura (è una data, si trova dopo il numero fattura, deve estrarla in questo formato yyyy-mm-dd)"
    "periodo_fornitura (è una stringa ed è mandatory, ad esempio Agosto 2024 - Settembre 2024)",
    "prezzo_unitario_kWh (è un double ed è mandatory)",
    "totale_da_pagare (è un double ed è mandatory, totale della bolletta da pagare)",
    "kWh_consumati_totali (è un int ed è mandatory)",
    "kWh_F1_consumati (è un intero ed è mandatory)",
    "kWh_F2_consumati (è un intero ed è mandatory)",
    "kWh_F3_consumati (è un intero ed è mandatory)",
    "canone_tv (è un double non è sempre presente)",
    "spese_per_energia (è un double, dettaglio specifico)",
    "spese_trasporto_gestione_contatore (è un double, dettaglio specifico)",
    "spese_oneri (è un double, dettaglio specifico)",
    "altre_partite (è un double, dettaglio specifico)",
    "imposte_iva (è un double, dettaglio specifico)"
]

mandatory_fields = [
    "fornitore",
    "numero_fattura",
    "data_fattura",
    "periodo_fornitura",
    "prezzo_unitario_kWh",
    "totale_da_pagare",
    "kWh_consumati_totali",
    "kWh_F1_consumati",
    "kWh_F2_consumati",
    "kWh_F3_consumati",
    "spese_per_energia",
    "spese_trasporto_gestione_contatore",
    "spese_oneri",
    "altre_partite",
    "imposte_iva"
]

columns_to_select = [
    "fornitore",
    "numero_fattura",
    "data_fattura",
    "periodo_fornitura",
    "prezzo_unitario_kWh",
    "totale_da_pagare",
    "kWh_consumati_totali",
    "kWh_F1_consumati",
    "kWh_F2_consumati",
    "kWh_F3_consumati",
    "canone_tv",
    "spese_per_energia",
    "spese_trasporto_gestione_contatore",
    "spese_oneri",
    "altre_partite",
    "imposte_iva",
    "note"
]

schema = {
    "fornitore": str,
    "numero_fattura": str,
    "data_fattura": "datetime64[ns]",
    "periodo_fornitura": str,
    "prezzo_unitario_kWh": float,
    "totale_da_pagare": float,
    "kWh_consumati_totali": int,
    "kWh_F1_consumati": int,
    "kWh_F2_consumati": int,
    "kWh_F3_consumati": int,
    "canone_tv": float,
    "spese_per_energia": float,
    "spese_trasporto_gestione_contatore": float,
    "spese_oneri": float,
    "altre_partite": float,
    "imposte_iva": float,
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
TABLE_NAME = "bollette_luce_history"

# Schema della tabella
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS bollette_luce_history (
    fornitore VARCHAR,
    numero_fattura VARCHAR PRIMARY KEY,
    data_fattura TIMESTAMP,
    periodo_fornitura VARCHAR,
    prezzo_unitario_kWh FLOAT,
    totale_da_pagare FLOAT,
    kWh_consumati_totali INT,
    kWh_F1_consumati INT,
    kWh_F2_consumati INT,
    kWh_F3_consumati INT,
    canone_tv FLOAT,
    spese_per_energia FLOAT,
    spese_trasporto_gestione_contatore FLOAT,
    spese_oneri FLOAT,
    altre_partite FLOAT,
    imposte_iva FLOAT,
    note VARCHAR
);
"""

# Query di inserimento
insert_query = """
INSERT INTO bollette_luce_history (
    fornitore, numero_fattura, data_fattura, periodo_fornitura,
    prezzo_unitario_kWh, totale_da_pagare, kWh_consumati_totali,
    kWh_F1_consumati, kWh_F2_consumati, kWh_F3_consumati, canone_tv,
    spese_per_energia, spese_trasporto_gestione_contatore, spese_oneri,
    altre_partite, imposte_iva, note
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""

# AirTable Constants
table_name = "tbl9W0Qz1oU6dkOOU"

key_field = "numero_fattura"
