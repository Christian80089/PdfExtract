from bancaExtract.utils import TransformationsIng, TransformationsDeutsche
from bancaExtract.utils.Constants import *
from constants.CommonConstants import *
from functions.FunctionsV2 import *

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/banche"
    checkpoint_file = "resources/checkpoints/processed_files.txt"

    new_files_processed = False  # Flag per verificare se ci sono nuovi file processati
    initialLoadOnDB = False
    if initialLoadOnDB:
        csv_path = "resources/output/ing_movimenti_banca_history.csv"
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
            if filename.endswith('.csv') and filename not in processed_files:
                file_path = os.path.join(root, filename)
                logger.info(f"Inizio elaborazione del file: {filename}")

                try:
                    # Estrai la data dal nome del file
                    extracted_date = extract_date_from_filename(filename)

                    # Trasformazione dei dati in DataFrame
                    df = pd.read_csv(file_path, delimiter=';',
                                     header=0)  # Crea il DataFrame solo con i dati del file corrente
                    if extracted_date:
                        df["data_estratto_conto"] = extracted_date  # Aggiungi la colonna con la data
                        df["data_estratto_conto"] = pd.to_datetime(df["data_estratto_conto"], format='%d-%m-%Y')

                    # Determina la trasformazione da applicare in base alla cartella o al nome del file
                    if "deutsche" in root.lower() or "deutsche" in filename.lower():
                        transformed_df = TransformationsDeutsche.transform_df(df, columns_to_select)
                        # Scrittura su AirTable
                        # upload_to_airtable_from_dataframe(personal_token, base_id, deutsche_table_name, transformed_df, key_field)
                        transformed_df.to_csv(f'resources/output/{filename.lower()}', index=False, sep=';')
                    elif "ing" in root.lower() or "ing" in filename.lower():
                        transformed_df = TransformationsIng.transform_df(df, columns_to_select)
                        # Scrittura su AirTable
                        upload_to_airtable_from_dataframe(personal_token, base_id, ing_table_name, transformed_df, key_field)
                        # Scrittura su PostgresSQL
                        write_df_to_table(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, NEW_DB_NAME, TABLE_NAME,
                                           transformed_df, insert_query)
                    else:
                        logger.warning(
                            f"Impossibile determinare il tipo di trasformazione per il file {filename}. File saltato.")
                        continue

                    # Aggiorna il checkpoint
                    update_checkpoint(checkpoint_file, [filename])
                    logger.info(f"File {filename} elaborato e salvato con successo.")

                    new_files_processed = True  # Imposta il flag a True

                except Exception as e:
                    # Gestione degli errori per ogni fase dell'elaborazione del file
                    logger.error(f"Errore durante l'elaborazione del file {filename}: {e}")

    logger.info("Elaborazione completata.")
