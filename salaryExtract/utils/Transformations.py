import locale
import logging

import numpy as np
import pandas as pd

from functions.FunctionsV2 import cast_columns_with_defaults, select_columns_from_df
from salaryExtract.utils import Constants
from salaryExtract.utils.Constants import schema, default_values

# Configura il logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Imposta la localizzazione
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')


def transform_df(df, columns_to_select):
    logger.info("Inizio della trasformazione del DataFrame.")

    # Aggiungi colonne al DataFrame
    df["ragione_sociale_azienda"] = "Relatech Spa"
    df["date_periodo_di_retribuzione"] = pd.to_datetime("01-" + df["periodo_di_retribuzione"], format="%d-%B %Y")
    df["string_periodo_di_retribuzione"] = df["periodo_di_retribuzione"]
    df["retribuzione_minima_lorda"] = df["totale_retribuzione_minima_lorda"]
    df["percentuale_maggiorazione_ore_straordinario"] = 15
    df["irpef_pagata"] = df["ritenute_irpef"]
    df["note"] = "Script completato con successo"
    df["record_key"] = df["string_periodo_di_retribuzione"].astype(str) + "|" + df["netto_del_mese"].astype(int).astype(str)

    logger.info("Colonne aggiunte.")

    # Verifica i campi obbligatori e aggiorna la colonna 'note' per i campi mancanti
    for field in Constants.mandatory_fields:
        missing_count = df[field].isnull().sum()
        if missing_count > 0:
            logger.warning(f"Ci sono {missing_count} valori mancanti nella colonna '{field}'.")
        df["note"] = df.apply(
            lambda row: row["note"] + f"; Verificare {field} mancante" if pd.isnull(row[field]) else row["note"], axis=1
        )

    selected_df = select_columns_from_df(columns_to_select, df)
    selected_df = cast_columns_with_defaults(selected_df, schema, default_values)

    # Arrotonda i valori float per eccesso a due cifre decimali
    for column, dtype in schema.items():
        if dtype == "float":
            logger.info(f"Arrotondamento per eccesso della colonna '{column}' a due cifre decimali.")
            selected_df[column] = np.ceil(selected_df[column] * 100) / 100

    logger.info(f"Selezionate {len(columns_to_select)} colonne: {columns_to_select}.")
    logger.info("Trasformazione completata.")

    return selected_df
