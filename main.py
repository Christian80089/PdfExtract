import json
import logging
import os
import re

import pandas as pd

from utils import FunctionsV2, Transformations, Constants

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/relatech"
    json_array = []
    new_files = []  # Lista per memorizzare i nuovi file da elaborare
    checkpoint_file = "resources/checkpoints/processed_files.txt"
    processed_files = FunctionsV2.load_processed_files(checkpoint_file)  # Carica i file già elaborati

    for filename in os.listdir(pdf_folder_path):
        if filename.endswith('.pdf') and filename not in processed_files:
            pdf_path = os.path.join(pdf_folder_path, filename)
            logger.info(f"Processing file: {filename}")
            text = FunctionsV2.extract_pdf_data(pdf_folder_path + "/" + filename)

            formatted_text = re.sub(r'\s+', ' ', text)
            formatted_text = formatted_text.strip()

            response_copilot = FunctionsV2.run_copilot(formatted_text)

            data = json.loads(response_copilot)
            json_array.append(data)

            new_files.append(filename)

            if new_files:
                df = pd.DataFrame(json_array)

                transformed_df = Transformations.transform_df(df, Constants.columns_to_select)

                print(transformed_df.to_string(index=False))


                csv_path = f"output/relatech_buste_paga_history.csv"
                output_folder = "output"
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                    logger.info(f"Directory '{output_folder}' creata.")

                file_exists = os.path.exists(csv_path)

                # Salva il DataFrame trasformato come CSV
                transformed_df.to_csv(csv_path, mode='a', header=not file_exists, index=False)
                logger.info(f"Nuovi dati aggiunti al file CSV consolidato: {csv_path}")

                FunctionsV2.update_checkpoint(checkpoint_file, new_files)
            else:
                logger.info("Nessun nuovo file da elaborare.")