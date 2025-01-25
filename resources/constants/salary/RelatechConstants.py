import datetime

relatech_copilot_info_to_extract = [
    "periodo_di_retribuzione (è una stringa ed è mandatory)",
    "totale_retribuzione_minima_lorda (è un int ed è la somma di Paga Base, Conting, 3Elemen e Sup. ass.) è mandatory",
    "giorni_lavorati (è un double e non sono mandatory, nella sezione LAVORATO quarto valore)",
    "ore_lavorate (è un double e non sono mandatory, ore ordinarie nella sezione LAVORATO quinto valore)",
    "ore_straordinarie (è un double e non sono mandatory, nella sezione LAVORATO)",
    "ritenute_irpef (è un double ed è mandatory)",
    "totale_competenze (è un double ed è mandatory)",
    "totale_trattenute (è un double ed è mandatory)",
    "arrotondamento (è un double ed è mandatory)",
    "netto_del_mese (è un double ed è mandatory)",
    "retribuzione_utile_tfr (è un double ed è mandatory)",
    "quota_tfr (è un double ed è mandatory)",
    "totale_ferie_rimanenti (Saldo Ferie è un double non arrotondare)",
    "totale_permessi_rimanenti (Saldo R.O.L è un double non arrotondare)"
]

relatech_df_mandatory_fields = [
    "periodo_di_retribuzione",
    "totale_retribuzione_minima_lorda",
    "ritenute_irpef",
    "totale_competenze",
    "totale_trattenute",
    "arrotondamento",
    "netto_del_mese",
    "retribuzione_utile_tfr",
    "quota_tfr",
    "totale_ferie_rimanenti",
    "totale_permessi_rimanenti"
]

relatech_df_columns_to_select = [
    "record_key",
    "ragione_sociale_azienda",
    "date_periodo_di_retribuzione",
    "string_periodo_di_retribuzione",
    "retribuzione_minima_lorda",
    "giorni_lavorati",
    "ore_lavorate",
    "percentuale_maggiorazione_ore_straordinario",
    "ore_straordinarie",
    "irpef_pagata",
    "totale_competenze",
    "totale_trattenute",
    "arrotondamento",
    "netto_del_mese",
    "retribuzione_utile_tfr",
    "quota_tfr",
    "totale_ferie_rimanenti",
    "totale_permessi_rimanenti",
    "note"
]

relatech_df_schema = {
    "record_key": str,  # Concatenazione di Periodo di retribuzione e netto del mese
    "ragione_sociale_azienda": str,  # Nome dell'azienda (stringa)
    "date_periodo_di_retribuzione": object,  # Data di inizio periodo di retribuzione (data)
    "string_periodo_di_retribuzione": str,  # Periodo di retribuzione come stringa
    "retribuzione_minima_lorda": float,  # Retribuzione minima lorda (float)
    "giorni_lavorati": int,  # Giorni lavorati (int)
    "ore_lavorate": int,  # Ore lavorate (int)
    "percentuale_maggiorazione_ore_straordinario": int,  # Percentuale di maggiorazione per straordinario (int)
    "ore_straordinarie": int,  # Ore di straordinario lavorate (int)
    "irpef_pagata": float,  # IRPEF pagata (float)
    "totale_competenze": float,  # Totale competenze (float)
    "totale_trattenute": float,  # Totale trattenute (float)
    "arrotondamento": float,  # Arrotondamento (float)
    "netto_del_mese": int,  # Netto del mese (int)
    "retribuzione_utile_tfr": float,  # Retribuzione utile per TFR (float)
    "quota_tfr": float,  # Quota TFR (float)
    "totale_ferie_rimanenti": float,  # Totale ferie rimanenti (float)
    "totale_permessi_rimanenti": float,  # Totale permessi rimanenti (float)
    "note": str  # Note (stringa)
}

relatech_postgresql_table_name = "buste_paga_history"

relatech_postgresql_table_schema = """
CREATE TABLE IF NOT EXISTS buste_paga_history (
    record_key VARCHAR PRIMARY KEY,
    ragione_sociale_azienda VARCHAR,
    date_periodo_di_retribuzione DATE,
    string_periodo_di_retribuzione VARCHAR,
    retribuzione_minima_lorda FLOAT,
    giorni_lavorati INT,
    ore_lavorate INT,
    percentuale_maggiorazione_ore_straordinario INT,
    ore_straordinarie INT,
    irpef_pagata FLOAT,
    totale_competenze FLOAT,
    totale_trattenute FLOAT,
    arrotondamento FLOAT,
    netto_del_mese FLOAT,
    retribuzione_utile_tfr FLOAT,
    quota_tfr FLOAT,
    totale_ferie_rimanenti FLOAT,
    totale_permessi_rimanenti FLOAT,
    note TEXT
);
"""

relatech_postgresql_insert_query = """
INSERT INTO buste_paga_history (
    record_key, ragione_sociale_azienda, date_periodo_di_retribuzione, string_periodo_di_retribuzione,
    retribuzione_minima_lorda, giorni_lavorati, ore_lavorate,
    percentuale_maggiorazione_ore_straordinario, ore_straordinarie,
    irpef_pagata, totale_competenze, totale_trattenute,
    arrotondamento, netto_del_mese, retribuzione_utile_tfr,
    quota_tfr, totale_ferie_rimanenti,
    totale_permessi_rimanenti, note
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

relatech_airtable_table_name = "tbl3pSxuXeWGe1PeV"

relatech_key_field = "record_key"
