import json
import logging
import os
import re
import pandas as pd
from salaryExtract.utils import Transformations, FunctionsV2, Constants
from salaryExtract.utils.FunctionsV2 import save_to_excel_in_append_mode

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/relatech"
    checkpoint_file = "resources/checkpoints/processed_files.txt"
    excel_path = "output/relatech_buste_paga_history.xlsx"
    output_folder = "output"

    # Crea la directory di output se non esiste
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Directory '{output_folder}' creata.")

    try:
        processed_files = FunctionsV2.load_processed_files(checkpoint_file)  # Carica i file già elaborati
    except Exception as e:
        logger.error(f"Errore durante il caricamento dei file processati: {e}")
        processed_files = []

    for filename in os.listdir(pdf_folder_path):
        if filename.endswith('.pdf') and filename not in processed_files:
            pdf_path = os.path.join(pdf_folder_path, filename)
            logger.info(f"Inizio elaborazione del file: {filename}")

            try:
                # Estrazione dei dati dal PDF
                text = FunctionsV2.extract_pdf_data(pdf_path)
                formatted_text = re.sub(r'\s+', ' ', text).strip()

                # Interazione con Copilot
                response_copilot = FunctionsV2.run_copilot(formatted_text)
                data = json.loads(response_copilot)

                # Trasformazione dei dati in DataFrame
                df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
                transformed_df = Transformations.transform_df(df, Constants.columns_to_select)

                # Salvataggio dei dati trasformati nel file Excel
                save_to_excel_in_append_mode(excel_path, transformed_df)

                # Aggiorna il checkpoint
                FunctionsV2.update_checkpoint(checkpoint_file, [filename])
                logger.info(f"File {filename} elaborato e salvato con successo.")

            except Exception as e:
                # Gestione degli errori per ogni fase dell'elaborazione del file
                logger.error(f"Errore durante l'elaborazione del file {filename}: {e}")

    logger.info("Elaborazione completata.")
