import hashlib
import locale

from resources.constants.common.Constants import df_default_values
from resources.constants.salary.RelatechConstants import *
from resources.functions.DataFrameFunctions import *

# Configura il logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Imposta la localizzazione
locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")


def transform_df(df, columns_to_select, extracted_date):
    logger.info("Inizio della trasformazione del DataFrame.")

    # Aggiungi colonne al DataFrame
    df["banca"] = "Deutsche Bank"
    df["numero_conto_corrente"] = "823503"
    df["codice_iban"] = "IT90R0310439841000000823503"
    df["descrizione"] = df["Categoria"]
    df["uscite"] = (
        df["Dare"]
        .astype(str)
        .str.replace("-", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
        * -1
    )
    df["entrate"] = (
        df["Avere"]
        .astype(str)
        .str.replace("+", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
    df["causale"] = df["Operazione"]
    df["note"] = "File Estratto Conto Trimestrale - Script completato con successo"
    df["data_operazione"] = df["Valuta"].apply(
        lambda x: pd.to_datetime(f"01-{x}", format="%d/%m/%Y").date()
    )
    df["concatenated_key"] = (
        df["data_operazione"].astype(str)
        + "|"
        + df["uscite"].astype(str)
        + "|"
        + df["entrate"].astype(str)
        + "|"
        + df["descrizione"].astype(str)
        + "|"
        + df["causale"].astype(str)
    )
    df["record_key"] = df["concatenated_key"].apply(
        lambda x: hashlib.sha256(x.encode()).hexdigest()
    )
    df_filtered = df[
        ~df["descrizione"]
        .astype(str)
        .str.contains("Saldo iniziale|Saldo finale", case=True, na=True)
    ]
    df["data_estratto_conto"] = extracted_date  # Aggiungi la colonna con la data
    df["data_estratto_conto"] = df["data_estratto_conto"].apply(
        lambda x: pd.to_datetime(f"01-{x}", format="%d/%m/%Y").date()
    )

    logger.info("Colonne base aggiunte")

    # Verifica i campi obbligatori e aggiorna la colonna 'note' per i campi mancanti
    for field in relatech_df_mandatory_fields:
        missing_count = df[field].isnull().sum()
        if missing_count > 0:
            logger.warning(
                f"Ci sono {missing_count} valori mancanti nella colonna '{field}'."
            )
        df["note"] = df.apply(
            lambda row: (
                row["note"] + f"; Verificare {field} mancante"
                if pd.isnull(row[field])
                else row["note"]
            ),
            axis=1,
        )

    selected_df = select_columns_from_df(columns_to_select, df_filtered)
    selected_df = cast_columns_with_defaults(
        selected_df, relatech_df_schema, df_default_values
    )

    logger.info(f"Selezionate {len(columns_to_select)} colonne: {columns_to_select}.")
    logger.info("Trasformazione completata.")

    return selected_df
