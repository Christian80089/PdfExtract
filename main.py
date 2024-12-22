import json
import logging
import os
import re

import pandas as pd

from utils import FunctionsV2, Transformations, Constants
from utils.FunctionsV2 import save_to_excel_in_append_mode

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/relatech"
    checkpoint_file = "resources/checkpoints/processed_files.txt"
    processed_files = FunctionsV2.load_processed_files(checkpoint_file)  # Carica i file già elaborati

    excel_path = "output/relatech_buste_paga_history.xlsx"
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Directory '{output_folder}' creata.")

    for filename in os.listdir(pdf_folder_path):
        if filename.endswith('.pdf') and filename not in processed_files:
            pdf_path = os.path.join(pdf_folder_path, filename)
            logger.info(f"Processing file: {filename}")
            text = FunctionsV2.extract_pdf_data(pdf_folder_path + "/" + filename)

            formatted_text = re.sub(r'\s+', ' ', text)
            formatted_text = formatted_text.strip()

            response_copilot = FunctionsV2.run_copilot(formatted_text)

            data = json.loads(response_copilot)

            # Trasforma il DataFrame per il file corrente
            df = pd.DataFrame([data])  # Crea il DataFrame solo con i dati del file corrente
            transformed_df = Transformations.transform_df(df, Constants.columns_to_select)

            # Salva i dati trasformati in Excel
            save_to_excel_in_append_mode(excel_path, transformed_df)

            # Aggiorna il checkpoint con il file appena processato
            FunctionsV2.update_checkpoint(checkpoint_file, [filename])
            logger.info(f"File {filename} elaborato e salvato.")

    logger.info("Elaborazione completata.")
