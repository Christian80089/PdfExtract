import hashlib
import locale

from resources.constants.bank_transactions.BankConstants import *
from resources.constants.common.Constants import *
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
    
    df = df[
        ~df["DESCRIZIONE OPERAZIONE"].str.contains(
            "Saldo iniziale|Saldo finale", case=True, na=True
        )
    ]
    # Aggiungi colonne al DataFrame
    df["banca"] = "Ing Arancio"
    df["numero_conto_corrente"] = "2686433"
    df["codice_iban"] = "IT74D0347501605CC0012686433"
    df["descrizione"] = df["DESCRIZIONE OPERAZIONE"]
    df["uscite"] = (
        df["USCITE"]
        .str.replace("-", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
        * -1
    )
    df["entrate"] = (
        df["ENTRATE"]
        .str.replace("+", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["causale"] = df["CAUSALE"]
    df["note"] = "File Estratto Conto Trimestrale - Script completato con successo"
    df["data_operazione"] = pd.to_datetime(df["DATA VALUTA"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")

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
    df["data_estratto_conto"] = extracted_date  # Aggiungi la colonna con la data
    df["data_estratto_conto"] = pd.to_datetime(df["data_estratto_conto"])  # Converti la colonna in formato datetime
    df["data_estratto_conto"] = df["data_estratto_conto"].dt.strftime("%d/%m/%Y")  # Applica il formato desiderato

    logger.info("Colonne base aggiunte")

    # Verifica i campi obbligatori e aggiorna la colonna 'note' per i campi mancanti
    for field in bank_df_mandatory_fields:
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

    selected_df = select_columns_from_df(columns_to_select, df)
    selected_df = cast_columns_with_defaults(
        selected_df, bank_df_schema, df_default_values
    )

    logger.info(f"Selezionate {len(columns_to_select)} colonne: {columns_to_select}.")
    logger.info("Trasformazione completata.")

    return selected_df
