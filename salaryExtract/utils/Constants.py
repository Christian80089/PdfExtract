import pandas as pd

info_to_extract = [
    "periodo_di_retribuzione (è una stringa ed è mandatory)",
    "totale_retribuzione_minima_lorda (è un int ed è la somma di Paga Base, Conting, 3Elemen e Sup. ass.) è mandatory",
    "giorni_lavorati (è un double e non sono mandatory, nella sezione LAVORATO quarto valore)",
    "ore_lavorate (è un double e non sono mandatory, ore ordinarie nella sezione LAVORATO quinto valore)",
    "ore_straordinarie (è un double e non sono mandatory, nella sezione LAVORATO sesto valore)",
    "ritenute_irpef (è un double ed è mandatory)",
    "totale_competenze (è un double ed è mandatory)",
    "totale_trattenute (è un double ed è mandatory)",
    "arrotondamento (è un double ed è mandatory)",
    "netto_del_mese (è un double ed è mandatory)",
    "retribuzione_utile_tfr (è un double ed è mandatory)",
    "quota_tfr (è un double ed è mandatory)",
    "ferie_giorni_residuo_anno_precedente (è un double e non è mandatory Ferie Residuo AP)",
    "permessi_ore_residuo_anno_precedente (è un double e non è mandatory, ROL Residuo AP)",
    "ferie_giorni_spettante (è un double o un int ed è mandatory)",
    "permessi_ore_spettante (è un double o un int ed è mandatory)",
    "ferie_giorni_goduto (è un double o un int e non è mandatory)",
    "permessi_ore_goduto (è un double o un int e non è mandatory)",
    "totale_ferie_rimanenti (è un double o un int ed è mandatory)",
    "totale_permessi_rimanenti (è un double o un int ed è mandatory)"
]

mandatory_fields = [
    "periodo_di_retribuzione",
    "totale_retribuzione_minima_lorda",
    "ritenute_irpef",
    "totale_competenze",
    "totale_trattenute",
    "arrotondamento",
    "netto_del_mese",
    "retribuzione_utile_tfr",
    "quota_tfr",
    "ferie_giorni_residuo_anno_precedente",
    "permessi_ore_residuo_anno_precedente",
    "ferie_giorni_spettante",
    "permessi_ore_spettante",
    "totale_ferie_rimanenti",
    "totale_permessi_rimanenti"
]

columns_to_select = [
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
    "ferie_giorni_residuo_anno_precedente",
    "permessi_ore_residuo_anno_precedente",
    "ferie_giorni_spettante",
    "permessi_ore_spettante",
    "totale_ferie_rimanenti",
    "totale_permessi_rimanenti",
    "note"
]

schema = {
    "ragione_sociale_azienda": str,  # Nome dell'azienda (stringa)
    "date_periodo_di_retribuzione": "datetime64[ns]",  # Data di inizio periodo di retribuzione (data)
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
    "ferie_giorni_residuo_anno_precedente": float,  # Ferie residue anno precedente (float)
    "permessi_ore_residuo_anno_precedente": float,  # Permessi ore residue anno precedente (float)
    "ferie_giorni_spettante": float,  # Ferie spettanti (float)
    "permessi_ore_spettante": float,  # Permessi spettanti (float)
    "totale_ferie_rimanenti": float,  # Totale ferie rimanenti (float)
    "totale_permessi_rimanenti": float,  # Totale permessi rimanenti (float)
    "note": str  # Note (stringa)
}

# Valori predefiniti per i tipi
default_values = {
    str: "",
    "datetime64[ns]": pd.NaT,
    float: 0.0,
    int: 0
}

# Dettagli di connessione al database
TABLE_NAME = "relatech_buste_paga_history"

# Schema della tabella relatech_buste_paga_history
TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS relatech_buste_paga_history (
    ragione_sociale_azienda VARCHAR,
    date_periodo_di_retribuzione TIMESTAMP,
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
    netto_del_mese INT,
    retribuzione_utile_tfr FLOAT,
    quota_tfr FLOAT,
    ferie_giorni_residuo_anno_precedente FLOAT,
    permessi_ore_residuo_anno_precedente FLOAT,
    ferie_giorni_spettante FLOAT,
    permessi_ore_spettante FLOAT,
    totale_ferie_rimanenti FLOAT,
    totale_permessi_rimanenti FLOAT,
    note VARCHAR
);
"""

# Query di inserimento per relatech_buste_paga_history
insert_query = """
INSERT INTO relatech_buste_paga_history (
    ragione_sociale_azienda, date_periodo_di_retribuzione, string_periodo_di_retribuzione,
    retribuzione_minima_lorda, giorni_lavorati, ore_lavorate,
    percentuale_maggiorazione_ore_straordinario, ore_straordinarie,
    irpef_pagata, totale_competenze, totale_trattenute,
    arrotondamento, netto_del_mese, retribuzione_utile_tfr,
    quota_tfr, ferie_giorni_residuo_anno_precedente,
    permessi_ore_residuo_anno_precedente, ferie_giorni_spettante,
    permessi_ore_spettante, totale_ferie_rimanenti,
    totale_permessi_rimanenti, note
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
