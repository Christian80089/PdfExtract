import json
import logging
import os
import re
from datetime import datetime

import pandas as pd

from utils import FunctionsV2, Transformations, Constants

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

if __name__ == '__main__':
    pdf_folder_path = "resources/relatech"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_array = []
    for filename in os.listdir(pdf_folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, filename)
            logger.info(f"Processing file: {filename}")
            text = FunctionsV2.extract_pdf_data(pdf_folder_path + "/" + filename)

            formatted_text = re.sub(r'\s+', ' ', text)
            formatted_text = formatted_text.strip()

            response_copilot = FunctionsV2.run_copilot(formatted_text)

            data = json.loads(response_copilot)
            json_array.append(data)

    df = pd.DataFrame(json_array)

    transformed_df = Transformations.transform_df(df, Constants.columns_to_select)

    print(transformed_df.to_string(index=False))

    csv_path = f"output/relatech_buste_paga_history_{timestamp}.csv"
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logger.info(f"Directory '{output_folder}' creata.")

    # Salva il DataFrame trasformato come CSV
    transformed_df.to_csv(csv_path, index=False)

    print(f"File CSV salvato in: {csv_path}")
