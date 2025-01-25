import json

from backend.resources.constants.bank_transactions.BankConstants import bank_key_field, bank_df_columns_to_select, \
    bank_copilot_info_to_extract
from backend.resources.constants.berebel.BerebelConstants import berebel_key_field, berebel_df_columns_to_select, \
    berebel_copilot_info_to_extract
from backend.resources.constants.light_bills.LightBillsConstants import light_key_field, light_df_columns_to_select, \
    light_copilot_info_to_extract
from backend.resources.constants.salary.RelatechConstants import relatech_df_columns_to_select, relatech_key_field, \
    relatech_copilot_info_to_extract
from backend.resources.functions.CopilotFunctions import run_copilot
from backend.resources.functions.PdfFunctions import extract_pdf_data
from backend.transformations.bank_transactions import IngTransform
from backend.transformations.berebel import BerebelTransform
from backend.transformations.light_bills import EnelTransform
from backend.transformations.salary import RelatechTransform
from backend.resources.functions.Functions import *

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    input_data_folder_path = "../resources/input_data"
    checkpoints_folder_path = "resources/checkpoints/"

    new_files_processed = False  # Flag per verificare se ci sono nuovi file processati
    processed_files = []

    try:
        processed_files = load_processed_files(checkpoints_folder_path)  # Carica i file già elaborati
    except Exception as e:
        logger.error(f"Errore durante il caricamento dei file processati: {e}")

    # Usa os.walk per scansionare ricorsivamente tutte le subfolder
    for root, _, files in os.walk(input_data_folder_path):
        for filename in files:
            if (filename.endswith('.csv') or filename.endswith('.pdf')) and filename not in processed_files:
                file_path = os.path.join(root, filename)
                logger.info(f"Inizio elaborazione del file: {filename}")

                try:
                    # Estrai la data dal nome del file
                    extracted_date = extract_date_from_filename(filename)

                    if filename.endswith('.csv'):
                        # Trasformazione dei dati in DataFrame
                        df = pd.read_csv(file_path, delimiter=';',
                                         header=0)  # Crea il DataFrame solo con i dati del file corrente
                        if "bank_transactions" in root.lower():
                            checkpoint_file = "resources/checkpoints/bank_transactions_processed_files.txt"
                            output_path = "resources/output_data/bank_transactions/ing/bank_transactions_history.csv"
                            transformed_df = IngTransform.transform_df(df, bank_df_columns_to_select, extracted_date)
                            upsert_to_csv(transformed_df, output_path, bank_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        elif "berebel" in root.lower():
                            checkpoint_file = "resources/checkpoints/berebel_processed_files.txt"
                            output_path = "resources/output_data/berebel/berebel_history.csv"
                            transformed_df = BerebelTransform.transform_df(df, berebel_df_columns_to_select)
                            upsert_to_csv(transformed_df, output_path, berebel_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        elif "light_bills" in root.lower():
                            checkpoint_file = "resources/checkpoints/light_bills_processed_files.txt"
                            output_path = "resources/output_data/light_bills/light_bills_history.csv"
                            transformed_df = EnelTransform.transform_df(df, light_df_columns_to_select)
                            upsert_to_csv(transformed_df, output_path, light_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        elif "salary" in root.lower():
                            checkpoint_file = "resources/checkpoints/salary_processed_files.txt"
                            output_path = "resources/output_data/salary/salary_history.csv"
                            transformed_df = RelatechTransform.transform_df(df, relatech_df_columns_to_select)
                            upsert_to_csv(transformed_df, output_path, relatech_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        else:
                            logger.error(f"Folder non gestita: {root.lower()}")
                    elif filename.endswith('.pdf'):
                        # Estrazione dei dati dal PDF
                        text = extract_pdf_data(file_path)
                        formatted_text = re.sub(r'\s+', ' ', text).strip()

                        if "bank_transactions" in root.lower():
                            checkpoint_file = "resources/checkpoints/bank_transactions_processed_files.txt"
                            # Interazione con Copilot
                            response_copilot = run_copilot(formatted_text, bank_copilot_info_to_extract)
                            data = json.loads(response_copilot)
                            # Trasformazione dei dati in DataFrame
                            df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
                            output_path = "resources/output_data/bank_transactions/ing/bank_transactions_history.csv"
                            transformed_df = IngTransform.transform_df(df, bank_df_columns_to_select, extracted_date)
                            upsert_to_csv(transformed_df, output_path, bank_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        elif "berebel" in root.lower():
                            checkpoint_file = "resources/checkpoints/berebel_processed_files.txt"
                            # Interazione con Copilot
                            response_copilot = run_copilot(formatted_text, berebel_copilot_info_to_extract)
                            data = json.loads(response_copilot)
                            # Trasformazione dei dati in DataFrame
                            df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
                            output_path = "resources/output_data/berebel/berebel_history.csv"
                            transformed_df = BerebelTransform.transform_df(df, berebel_df_columns_to_select)
                            upsert_to_csv(transformed_df, output_path, berebel_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        elif "light_bills" in root.lower():
                            checkpoint_file = "resources/checkpoints/light_bills_processed_files.txt"
                            # Interazione con Copilot
                            response_copilot = run_copilot(formatted_text, light_copilot_info_to_extract)
                            data = json.loads(response_copilot)
                            # Trasformazione dei dati in DataFrame
                            df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
                            output_path = "resources/output_data/light_bills/light_bills_history.csv"
                            transformed_df = EnelTransform.transform_df(df, light_df_columns_to_select)
                            upsert_to_csv(transformed_df, output_path, light_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        elif "salary" in root.lower():
                            checkpoint_file = "resources/checkpoints/salary_processed_files.txt"
                            # Interazione con Copilot
                            response_copilot = run_copilot(formatted_text, relatech_copilot_info_to_extract)
                            data = json.loads(response_copilot)
                            # Trasformazione dei dati in DataFrame
                            df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
                            output_path = "resources/output_data/salary/salary_history.csv"
                            transformed_df = RelatechTransform.transform_df(df, relatech_df_columns_to_select)
                            upsert_to_csv(transformed_df, output_path, relatech_key_field)
                            # Aggiorna il checkpoint
                            update_checkpoint(checkpoint_file, [filename])
                            logger.info(f"File {filename} elaborato e salvato con successo.")
                        else:
                            logger.error(f"Folder non gestita: {root.lower()}")

                    new_files_processed = True  # Imposta il flag a True

                except Exception as e:
                    # Gestione degli errori per ogni fase dell'elaborazione del file
                    logger.error(f"Errore durante l'elaborazione del file {filename}: {e}")

    logger.info("Elaborazione completata.")
