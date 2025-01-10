import json

from bolletteLuceExtract.utils import Transformations
from bolletteLuceExtract.utils.Constants import *
from constants.CommonConstants import *
from functions.FunctionsV2 import *

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/fornitori"
    checkpoint_file = "resources/checkpoints/processed_files.txt"

    new_files_processed = False  # Flag per verificare se ci sono nuovi file processati
    initialLoadOnDB = False
    if initialLoadOnDB:
        csv_path = "resources/output/bollette_luce_history.csv"
        create_database_and_table(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME, NEW_DB_NAME, TABLE_NAME,
                                  TABLE_SCHEMA)
        write_csv_to_table(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, NEW_DB_NAME, TABLE_NAME, csv_path, insert_query)

    try:
        processed_files = load_processed_files(checkpoint_file)  # Carica i file già elaborati
    except Exception as e:
        logger.error(f"Errore durante il caricamento dei file processati: {e}")
        processed_files = []

    # Usa os.walk per scansionare ricorsivamente tutte le subfolder
    for root, _, files in os.walk(pdf_folder_path):
        for filename in files:
            if filename.endswith('.pdf') and filename not in processed_files:
                pdf_path = os.path.join(root, filename)
                logger.info(f"Inizio elaborazione del file: {filename}")

                try:
                    # Estrazione dei dati dal PDF
                    text = extract_pdf_data(pdf_path, pages_to_extract=[0, 1], include_last_two=True)
                    formatted_text = re.sub(r'\s+', ' ', text).strip()

                    # Interazione con Copilot
                    response_copilot = run_copilot(formatted_text, info_to_extract)
                    data = json.loads(response_copilot)

                    # Trasformazione dei dati in DataFrame
                    df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
                    transformed_df = Transformations.transform_df(df, columns_to_select)

                    # Scrittura su AirTable
                    upload_to_airtable_from_dataframe(personal_token, base_id, table_name, transformed_df, key_field)

                    # Scrittura su PostgresSQL
                    write_df_to_table(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, NEW_DB_NAME, TABLE_NAME,
                                       transformed_df, insert_query)
                    # Aggiorna il checkpoint
                    update_checkpoint(checkpoint_file, [filename])
                    logger.info(f"File {filename} elaborato e salvato con successo.")

                    new_files_processed = True  # Imposta il flag a True

                except Exception as e:
                    # Gestione degli errori per ogni fase dell'elaborazione del file
                    logger.error(f"Errore durante l'elaborazione del file {filename}: {e}")

    logger.info("Elaborazione completata.")
