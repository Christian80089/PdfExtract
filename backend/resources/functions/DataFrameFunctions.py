import logging

import pandas as pd

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def select_columns_from_df(columns, df):
    """
    Seleziona specifiche colonne da un DataFrame.

    Parameters:
        columns (list): Lista di nomi di colonne da selezionare.
        df (pd.DataFrame): DataFrame di input.

    Returns:
        pd.DataFrame: DataFrame con solo le colonne selezionate.
    """
    if not isinstance(columns, list):
        raise ValueError("Il parametro 'columns' deve essere una lista di stringhe.")

    if not all(isinstance(col, str) for col in columns):
        raise ValueError(
            "Tutti gli elementi della lista 'columns' devono essere stringhe."
        )

    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"Le seguenti colonne non sono presenti nel DataFrame: {missing_columns}"
        )

    return df[columns]


def cast_columns_with_defaults(df, schema, default_values):
    # Fai una copia esplicita del DataFrame
    df = df.copy()

    for col, dtype in schema.items():
        if col in df.columns:
            try:
                # Prova a castare la colonna al tipo definito nello schema
                df.loc[:, col] = df[col].astype(dtype)
                logger.info(f"Colonna '{col}' castata con successo al tipo {dtype}.")
            except Exception as e:
                # In caso di errore, sostituisci con il valore predefinito
                logger.warning(
                    f"Errore nel cast della colonna '{col}' al tipo {dtype}: {e}"
                )
                default_value = default_values.get(dtype, None)
                df[col] = default_value
                logger.info(
                    f"Colonna '{col}' riempita con valore predefinito: {default_value}."
                )
        else:
            # Se la colonna non esiste, aggiungila con il valore predefinito
            default_value = default_values.get(dtype, None)
            df[col] = default_value
            logger.info(
                f"Colonna '{col}' aggiunta al DataFrame con valore predefinito: {default_value}."
            )
    return df
