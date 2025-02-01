import logging

import numpy as np
import pandas as pd
import requests

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def write_to_airtable_from_excel(personal_token, base_id, table_name, excel_file_path):
    """
    Carica dati in una tabella di Airtable a partire da un file Excel.

    Args:
        personal_token (str): Il Personal Access Token di Airtable.
        base_id (str): L'ID della base Airtable.
        table_name (str): Il nome della tabella in cui caricare i dati.
        excel_file_path (str): Percorso del file Excel contenente i dati.

    Returns:
        dict: La risposta dell'API di Airtable o None in caso di errore.
    """
    # Validazione del percorso del file Excel
    if not excel_file_path.endswith((".xls", ".xlsx")):
        logger.error("Errore: Il file specificato non è un file Excel valido.")
        return None

    # Leggi il file Excel e converti in una lista di dizionari
    try:
        df = pd.read_excel(excel_file_path)

        if df.empty:
            logger.error("Errore: Il file Excel è vuoto.")
            return None

        # Converti tutte le colonne datetime in stringhe ISO 8601
        for column in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                df[column] = df[column].apply(
                    lambda x: x.isoformat() if pd.notnull(x) else None
                )

        records = df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Errore nella lettura del file Excel: {e}")
        return None

    # Endpoint API di Airtable per la tabella specificata
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    # Intestazioni per l'autenticazione e il tipo di contenuto
    headers = {
        "Authorization": f"Bearer {personal_token}",
        "Content-Type": "application/json",
    }

    # Prepara i dati nel formato richiesto da Airtable
    payload = {"records": [{"fields": record} for record in records]}

    try:
        # Esegue la richiesta POST per caricare i dati
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Solleva un'eccezione per eventuali errori HTTP

        # Restituisce la risposta in formato JSON
        logger.info("Dati caricati con successo su AirTable!")
        return response.json()
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Errore nella richiesta: {req_err}")
    except Exception as e:
        logger.error(f"Errore imprevisto: {e}")

    return None


def write_to_airtable_from_dataframe(
    personal_token, base_id, table_name, dataframe, key_field
):
    """
    Carica dati in una tabella di Airtable a partire da un DataFrame Pandas.
    Controlla se un record con una chiave specifica esiste già prima di aggiungerlo.

    Args:
        personal_token (str): Il Personal Access Token di Airtable.
        base_id (str): L'ID della base Airtable.
        table_name (str): Il nome della tabella in cui caricare i dati.
        dataframe (pd.DataFrame): DataFrame contenente i dati da caricare.
        key_field (str): Nome del campo chiave da usare per verificare l'esistenza dei record.

    Returns:
        list: Lista delle risposte per ogni operazione effettuata (aggiunta o verifica).
    """
    # Verifica che il campo chiave esista nel DataFrame
    if key_field not in dataframe.columns:
        logger.error(f"Errore: Il campo chiave '{key_field}' non esiste nel DataFrame.")
        return None

    # Converti tutte le colonne datetime in stringhe ISO 8601
    for column in dataframe.columns:
        if pd.api.types.is_datetime64_any_dtype(dataframe[column]):
            dataframe[column] = dataframe[column].apply(
                lambda x: x.isoformat() if pd.notnull(x) else None
            )

    # Sostituisci valori non JSON-compliant (NaN, Infinity, -Infinity) con None
    dataframe = dataframe.replace([np.nan, np.inf, -np.inf], None)

    # Endpoint API di Airtable per la tabella specificata
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {personal_token}",
        "Content-Type": "application/json",
    }

    # Ottieni tutti i record esistenti su Airtable
    existing_records = {}
    try:
        offset = None
        while True:
            response = requests.get(url, headers=headers, params={"offset": offset})
            response.raise_for_status()
            data = response.json()
            for record in data.get("records", []):
                existing_records[record["fields"].get(key_field)] = record["id"]
            offset = data.get("offset")
            if not offset:
                break
    except requests.exceptions.RequestException as req_err:
        logger.error(
            f"Errore nella richiesta per ottenere i record esistenti: {req_err}"
        )
        return None

    # Lista delle risposte delle operazioni
    responses = []

    # Itera sui record del DataFrame
    for _, row in dataframe.iterrows():
        key_value = row[key_field]
        if key_value in existing_records:
            logger.info(
                f"Record con chiave '{key_value}' già esistente. Nessuna azione intrapresa."
            )
            continue

        # Prepara il record da aggiungere
        payload = {"records": [{"fields": row.to_dict()}]}

        # Esegui la richiesta POST per aggiungere il record
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            responses.append(response.json())
            logger.info(f"Record con chiave '{key_value}' aggiunto con successo.")
        except requests.exceptions.RequestException as req_err:
            logger.error(
                f"Errore nella richiesta per aggiungere il record '{key_value}': {req_err}"
            )
            responses.append(None)

    return responses
