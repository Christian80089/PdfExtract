import logging

import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def write_google_sheet_from_excel(file_path, folder_id):
    """
    Carica un file su Google Drive come Google Fogli. Se esiste già, lo sovrascrive.

    Args:
        file_path (str): Percorso del file da caricare.
        folder_id (str): ID della cartella di Google Drive.
    """
    from os.path import splitext

    # Autenticazione
    credentials = service_account.Credentials.from_service_account_file(
        "resources/google/quiet-dimension-421414-f1378bc8723b.json",
        scopes=[
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/spreadsheets",
        ],
    )
    drive_service = build("drive", "v3", credentials=credentials)
    sheets_service = build("sheets", "v4", credentials=credentials)

    # Ottieni il nome del file senza estensione
    file_name = file_path.split("/")[-1]
    base_name, _ = splitext(file_name)

    # Cerca se il file esiste già nella cartella (senza considerare l'estensione)
    query = (
        f"'{folder_id}' in parents and name contains '{base_name}' and trashed=false"
    )
    response = (
        drive_service.files()
        .list(q=query, spaces="drive", fields="files(id, name)")
        .execute()
    )
    files = response.get("files", [])

    # Se il file esiste, ottieni il suo ID
    file_id = None
    if files:
        file_id = files[0]["id"]
        logger.info(f"File esistente trovato con ID: {file_id}")

    # Leggi il file Excel con pandas
    df = pd.read_excel(file_path)

    # Converte le colonne di tipo datetime in stringhe
    for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
        df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")

    # Converte il DataFrame in una lista di liste (formato richiesto da Google Sheets)
    data = df.values.tolist()

    # Se il file esiste, sovrascrivi il contenuto
    if file_id:
        try:
            # Sovrascrivi tutto il contenuto del foglio
            update_request = (
                sheets_service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=file_id,
                    range="Sheet1!A1",  # Puoi specificare un altro intervallo se necessario
                    body={"values": data},  # Aggiungi qui i dati che vuoi sovrascrivere
                    valueInputOption="RAW",
                )
            )
            update_request.execute()

            logger.info(f"Contenuto del file '{file_name}' sovrascritto.")
        except HttpError as err:
            logger.error(f"Errore nell'aggiornare il file: {err}")
    else:
        # Se il file non esiste, carica come nuovo
        file_metadata = {
            "name": file_name,
            "parents": [folder_id],
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }
        media = MediaFileUpload(
            file_path,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        uploaded_file = (
            drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        logger.info(
            f"File '{file_name}' caricato come Google Fogli con ID: {uploaded_file.get('id')}"
        )
