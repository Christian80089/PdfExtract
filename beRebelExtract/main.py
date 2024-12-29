import json
import re

from beRebelExtract.utils import Transformations
from beRebelExtract.utils.Constants import *
from functions.FunctionsV2 import *

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/berebel"
    checkpoint_file = "resources/checkpoints/processed_files.txt"
    excel_path = "output/berebel_history.xlsx"
    output_folder = "output"

    # Crea la directory di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Directory '{output_folder}' creata.")

    new_files_processed = False  # Flag per verificare se ci sono nuovi file processati

    try:
        processed_files = load_processed_files(checkpoint_file)  # Carica i file già elaborati
    except Exception as e:
        logger.error(f"Errore durante il caricamento dei file processati: {e}")
        processed_files = []

    for filename in os.listdir(pdf_folder_path):
        if filename.endswith('.pdf') and filename not in processed_files:
            pdf_path = os.path.join(pdf_folder_path, filename)
            logger.info(f"Inizio elaborazione del file: {filename}")

            try:
                # Estrazione dei dati dal PDF
                text = extract_pdf_data(pdf_path)
                formatted_text = re.sub(r'\s+', ' ', text).strip()

                # Interazione con Copilot
                response_copilot = run_copilot(formatted_text, info_to_extract)
                data = json.loads(response_copilot)

                # Trasformazione dei dati in DataFrame
                df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
                transformed_df = Transformations.transform_df(df, columns_to_select)

                # Salvataggio dei dati trasformati nel file Excel
                save_to_excel_in_append_mode(excel_path, transformed_df)

                # Aggiorna il checkpoint
                update_checkpoint(checkpoint_file, [filename])
                logger.info(f"File {filename} elaborato e salvato con successo.")

                new_files_processed = True  # Imposta il flag a True

            except Exception as e:
                # Gestione degli errori per ogni fase dell'elaborazione del file
                logger.error(f"Errore durante l'elaborazione del file {filename}: {e}")

    # Salvataggio dell Excel su Google Drive
    if new_files_processed:
        file_path = 'output/berebel_history.xlsx'
        folder_id = '1tsr2ScFi4RAMy3uHE41tN5Odnx0zmS8Y'
        upload_file_as_google_sheet(file_path, folder_id)
        logger.info("File caricato su Google Drive.")

        # Creazione database e tabella
        logger.info("Inizio creazione database e tabella.")
        create_database_and_table(
            DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, NEW_DB_NAME, TABLE_NAME, TABLE_SCHEMA
        )
        logger.info("Database e tabella pronti.")

        # Scrittura dei dati dall'Excel alla tabella
        logger.info("Inizio caricamento dati nella tabella.")
        write_excel_to_table(
            DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, NEW_DB_NAME, TABLE_NAME, file_path, insert_query
        )
        logger.info("Caricamento dati completato.")
    else:
        logger.info("Nessun nuovo file elaborato. Salto il caricamento su Google Drive.")

    logger.info("Elaborazione completata.")
