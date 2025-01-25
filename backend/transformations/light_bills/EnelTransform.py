import locale
import logging

import numpy as np
import pandas as pd

from backend.resources.constants.common.Constants import df_default_values
from backend.resources.constants.light_bills.LightBillsConstants import light_df_mandatory_fields, light_df_schema
from backend.resources.functions.DataFrameFunctions import select_columns_from_df, cast_columns_with_defaults

# Configura il logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Imposta la localizzazione
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8')


def transform_df(df, columns_to_select):
    logger.info("Inizio della trasformazione del DataFrame.")

    # Aggiungi colonne al DataFrame
    df["note"] = "Script completato con successo"
    df["data_fattura"] = df["data_fattura"].apply(
        lambda x: pd.to_datetime(f"01-{x}", format="%d-%B %Y").date()
    )
    logger.info("Colonne base aggiunte")

    # Verifica i campi obbligatori e aggiorna la colonna 'note' per i campi mancanti
    for field in light_df_mandatory_fields:
        missing_count = df[field].isnull().sum()
        if missing_count > 0:
            logger.warning(f"Ci sono {missing_count} valori mancanti nella colonna '{field}'.")
        df["note"] = df.apply(
            lambda row: row["note"] + f"; Verificare {field} mancante" if pd.isnull(row[field]) else row["note"], axis=1
        )

    selected_df = select_columns_from_df(columns_to_select, df)
    selected_df = cast_columns_with_defaults(selected_df, light_df_schema, df_default_values)

    # Arrotonda i valori float per eccesso a due cifre decimali
    for column, dtype in light_df_schema.items():
        if dtype == "float":
            logger.info(f"Arrotondamento per eccesso della colonna '{column}' a due cifre decimali.")
            selected_df[column] = np.ceil(selected_df[column] * 100) / 100

    logger.info(f"Selezionate {len(columns_to_select)} colonne: {columns_to_select}.")
    logger.info("Trasformazione completata.")

    return selected_df
