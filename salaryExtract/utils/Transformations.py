import locale
import logging

import pandas as pd

from utils import FunctionsV2, Constants

# Configura il logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Imposta la localizzazione
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')


def transform_df(df, columns_to_select):
    logger.info("Inizio della trasformazione del DataFrame.")

    # Aggiungi colonne al DataFrame
    df["ragione_sociale_azienda"] = "Relatech Spa"
    df["date_periodo_di_retribuzione"] = pd.to_datetime("10-" + df["periodo_di_retribuzione"], format="%d-%B %Y")
    df["string_periodo_di_retribuzione"] = df["periodo_di_retribuzione"]
    df["retribuzione_minima_lorda"] = df["totale_retribuzione_minima_lorda"]
    df["percentuale_maggiorazione_ore_straordinario"] = "15"
    df["irpef_pagata"] = df["ritenute_irpef"]
    df["note"] = "Script completato con successo"

    logger.info("Colonne base aggiunte ('ragione_sociale_azienda', 'date_periodo_di_retribuzione', etc.).")

    # Verifica i campi obbligatori e aggiorna la colonna 'note' per i campi mancanti
    for field in Constants.mandatory_fields:
        missing_count = df[field].isnull().sum()
        if missing_count > 0:
            logger.warning(f"Ci sono {missing_count} valori mancanti nella colonna '{field}'.")
        df["note"] = df.apply(
            lambda row: row["note"] + f"; Verificare {field} mancante" if pd.isnull(row[field]) else row["note"], axis=1
        )

    selected_df = FunctionsV2.select_columns_from_df(columns_to_select, df)

    logger.info(f"Selezionate {len(columns_to_select)} colonne: {columns_to_select}.")
    logger.info("Trasformazione completata.")

    return selected_df
