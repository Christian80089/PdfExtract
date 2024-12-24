# PDF Extract

Questo script automatizza l'elaborazione di file, estraendo i dati da file PDF e salvandoli in un formato strutturato in un file Excel. Il processo include l'interazione con un'API per l'estrazione e la trasformazione dei dati, e consente di monitorare l'avanzamento dei file processati tramite un checkpoint.

## Requisiti

- Python 3.7 o superiore
- Librerie:
  - `pandas`
  - `pdfplumber`
  - `openpyxl`
  - `selenium`
  - `numpy`

## Installazione

1. Clona questo repository:
   ```bash
   git clone https://github.com/Christian80089/PdfExtract.git
   ```

2. Naviga nella directory del progetto:
   ```bash
   cd PdfExtract
   ```

3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Configurazione

Prima di eseguire il codice, assicurati di configurare i seguenti file:

- `checkpoint_file`: Percorso del file che tiene traccia dei file già processati.
- `pdf_folder_path`: Percorso della cartella contenente i file PDF da elaborare.
- `excel_path`: Percorso del file Excel dove salvare i dati elaborati.
- `Transformations`: Adatta le trasformazioni ai tuoi dati estratti

## Come Eseguire il Codice

1. Assicurati che il percorso dei file PDF e dei file di output siano configurati correttamente.
2. Esegui lo script:
   ```bash
   python main.py
   ```
3. I risultati verranno salvati nel file Excel specificato nel percorso `excel_path`.

Lo script elaborerà i file PDF nella cartella specificata, estrarrà i dati, interagirà con il sito Copilot e salverà i dati elaborati nel file Excel di output.

## Struttura del Codice

- **Funzioni principali:**
  - `concat_fields()`: Concatena i campi in una stringa.
  - `extract_pdf_data()`: Estrae il testo da un file PDF.
  - `run_copilot()`: Gestisce l'interazione con il sito Copilot.
  - `transform_df()`: Trasforma i dati in un DataFrame.
  - `save_to_excel_in_append_mode()`: Salva i dati nel file Excel in modalità append.

- **Elenco dei moduli:**
  - `FunctionsV2.py`: Contiene funzioni di utilità per la manipolazione dei dati.
  - `Constants.py`: Contiene costanti e schemi di dati per la trasformazione.

## Esempio di Esecuzione

Input (file PDF):
- Il file PDF contenente i dati delle buste paga.

Output (file Excel):
- Un file Excel che contiene i dati trasformati, inclusi i campi come `ragione_sociale_azienda`, `totale_retribuzione_minima_lorda`, `netto_del_mese`, ecc.

## Contributi

1. Fork questo repository.
2. Crea un nuovo branch (`git checkout -b feature-nome-feature`).
3. Fai le tue modifiche e aggiungi i test necessari.
4. Invia una pull request.

## Contatti

Christian - [christiandelprete01@gmail.com](mailto:christiandelprete01@gmail.com)
