import json
import re

from beRebelExtract.utils import Transformations
from beRebelExtract.utils.Constants import *
from constants.CommonConstants import *
from functions.FunctionsV2 import *

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/berebel"
    checkpoint_file = "resources/checkpoints/processed_files.txt"
    excel_path = "output/berebel_history.xlsx"
    output_folder = "output"

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

                # Scrittura su AirTable
                upload_to_airtable_from_dataframe(personal_token, base_id, table_name, transformed_df, key_field)

                # Aggiorna il checkpoint
                update_checkpoint(checkpoint_file, [filename])
                logger.info(f"File {filename} elaborato e salvato con successo.")

                new_files_processed = True  # Imposta il flag a True

            except Exception as e:
                # Gestione degli errori per ogni fase dell'elaborazione del file
                logger.error(f"Errore durante l'elaborazione del file {filename}: {e}")

    logger.info("Elaborazione completata.")
