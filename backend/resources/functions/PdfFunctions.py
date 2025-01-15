import logging

import pdfplumber

# Configurazione del logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


def extract_pdf_data(pdf_path, pages_to_extract=None, include_last_two=False, max_chars=8000):
    """
    Estrae il testo da un file PDF specificato, con la possibilità di limitare l'estrazione
    a pagine specifiche, includere la penultima e l'ultima pagina e impostare un limite massimo di caratteri.

    Parametri:
    pdf_path (str): Il percorso del file PDF da cui estrarre il testo.
    pages_to_extract (list[int], opzionale): Lista di indici delle pagine da estrarre (0-based).
                                             Se None, estrae tutte le pagine.
    include_last_two (bool, opzionale): Se True, include sempre la penultima e l'ultima pagina.
    max_chars (int, opzionale): Numero massimo di caratteri da estrarre. Default è 8000.

    Ritorna:
    str: Il testo estratto dalle pagine specificate o da tutto il PDF. In caso di errore, restituisce una stringa vuota.
    """
    logger.info(f"Inizio estrazione dati dal PDF: {pdf_path}")
    try:
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
            logger.info(f"Il PDF contiene {num_pages} pagina/e.")

            # Se pages_to_extract è None, estrai da tutte le pagine
            if pages_to_extract is None:
                pages_to_extract = list(range(num_pages))

            # Verifica che le pagine specificate esistano
            valid_pages = [i for i in pages_to_extract if i < num_pages]

            # Aggiungi la penultima e l'ultima pagina se richiesto
            if include_last_two and num_pages > 1:
                last_two_pages = {num_pages - 2, num_pages - 1}
                valid_pages = list(set(valid_pages).union(last_two_pages))

            valid_pages.sort()  # Ordina gli indici per sicurezza
            if not valid_pages:
                logger.warning("Nessuna delle pagine specificate esiste nel PDF.")
                return ""

            # Estrai il testo dalle pagine valide e limita i caratteri
            full_text = ""
            for i in valid_pages:
                if len(full_text) >= max_chars:
                    break
                page_text = pdf.pages[i].extract_text() or ""  # Evita None in caso di errori nella pagina
                full_text += page_text[:max_chars - len(full_text)]

        logger.info(f"Estrazione completata, {len(full_text)} caratteri estratti.")
        return full_text
    except Exception as e:
        logger.error(f"Errore durante l'estrazione del PDF: {e}")
        return ""  # Restituisce una stringa vuota in caso di errore
