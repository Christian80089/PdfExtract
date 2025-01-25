berebel_copilot_info_to_extract = [
    "minimo_mensile (è un double ed è mandatory)",
    "periodo_estratto_conto (è una string ed è mandatory, esempio: Novembre 2024)"
    "costo_al_km (è un double ed è mandatory",
    "targa (è una string ed è mandatory)",
    "km_percorsi (è un intero ed è mandatory - è il primo valore dei quattro)",
    "km_inclusi (è un intero ed è mandatory - è il secondo valore dei quattro)",
    "km_da_pagare (è un intero ed è mandatory - è il terzo valore dei quattro)",
    "km_residui (è un intero ed è mandatory - è il quarto valore dei quattro)",
    "premio_di_conguaglio (è un double ed è mandatory)",
    "totale_pagato (è un double ed è mandatory)"
]

berebel_df_mandatory_fields = [
    "minimo_mensile",
    "periodo_estratto_conto",
    "costo_al_km",
    "targa",
    "km_percorsi",
    "km_inclusi",
    "km_da_pagare",
    "km_residui",
    "premio_di_conguaglio",
    "totale_pagato"
]

berebel_df_columns_to_select = [
    "periodo_estratto_conto",
    "date_estratto_conto",
    "targa",
    "minimo_mensile",
    "costo_al_km",
    "km_percorsi",
    "km_inclusi",
    "km_da_pagare",
    "km_residui",
    "premio_di_conguaglio",
    "totale_pagato",
    "note"
]

berebel_df_schema = {
    "periodo_estratto_conto": str,
    "date_estratto_conto": object,
    "targa": str,
    "minimo_mensile": float,
    "costo_al_km": float,
    "km_percorsi": int,
    "km_inclusi": int,
    "km_da_pagare": int,
    "km_residui": int,
    "premio_di_conguaglio": float,
    "totale_pagato": float,
    "note": str
}

berebel_postgresql_table_name = "berebel_history"

berebel_postgresql_table_schema = """
CREATE TABLE IF NOT EXISTS berebel_history (
    periodo_estratto_conto VARCHAR,
    date_estratto_conto DATE,
    targa VARCHAR,
    minimo_mensile FLOAT,
    costo_al_km FLOAT,
    km_percorsi INT,
    km_inclusi INT,
    km_da_pagare INT,
    km_residui INT,
    premio_di_conguaglio FLOAT,
    totale_pagato FLOAT,
    note VARCHAR
);
"""

berebel_postgresql_insert_query = """
INSERT INTO berebel_history (
    periodo_estratto_conto, date_estratto_conto, targa,
    minimo_mensile, costo_al_km, km_percorsi, km_inclusi,
    km_da_pagare, km_residui, premio_di_conguaglio,
    totale_pagato, note
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

berebel_airtable_table_name = "tblYr6mF4ZO1oVat1"

berebel_key_field = "periodo_estratto_conto"
