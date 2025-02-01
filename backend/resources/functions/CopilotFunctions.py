import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from resources.functions.Functions import concat_fields

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def run_copilot(input_text, info_to_extract):
    """
    Automazione dell'interazione con il sito Copilot di Microsoft con logica di fallback.

    Parametri:
    input_text (str): Il testo non formattato che verrà analizzato da Copilot.

    Questo metodo automatizza l'interazione con Copilot: apre il sito, invia richieste e riceve risposte.
    In caso di errori, vengono loggati e il browser viene chiuso correttamente.
    """
    logger.info("Inizio interazione con Copilot.")

    driver = None
    try:
        # Avvia il browser Chrome
        driver = webdriver.Chrome()
        logger.info("Caricamento della pagina Copilot.")
        driver.get("https://copilot.microsoft.com/onboarding")

        # Tentativo di cliccare su "Inizia"
        try:
            logger.info("Tentativo di cliccare sul pulsante 'Inizia'.")
            WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@title="Inizia"]'))
            ).click()
            logger.info("Pulsante 'Inizia' cliccato.")
        except Exception:
            logger.warning(
                "Pulsante 'Inizia' non trovato. Procedo al passaggio successivo."
            )

        # Tentativo di inserire "Christian"
        try:
            logger.info("Tentativo di inserire 'Christian' nella casella di input.")
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.ID, "userInput"))
            ).send_keys("Christian", Keys.RETURN)
            logger.info("'Christian' inserito con successo.")
        except Exception:
            logger.warning(
                "Casella di input per 'Christian' non trovata. Procedo al passaggio successivo."
            )

        # Tentativo di cliccare su "Avanti"
        try:
            logger.info("Tentativo di cliccare sul pulsante 'Avanti'.")
            WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@title="Avanti"]'))
            ).click()
            logger.info("Pulsante 'Avanti' cliccato.")
        except Exception:
            logger.warning(
                "Pulsante 'Avanti' non trovato. Procedo al passaggio successivo."
            )

        # Invio della query
        query = f"Estrai le seguenti informazioni senza commenti, in formato json, su una sola riga e in un blocco di codice: {concat_fields(info_to_extract)} dal seguente testo non formattato: {input_text}"
        logger.info("Invio della query a Copilot.")
        try:
            question_box = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.ID, "userInput"))
            )
            question_box.send_keys(query, Keys.RETURN)
            logger.info("Query inviata con successo.")
        except Exception:
            logger.error(
                "Casella di input per la query non trovata. Interazione fallita."
            )
            return None

        # Attesa della risposta
        logger.info("Attesa della risposta da Copilot.")
        time.sleep(10)
        response_element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located(
                (By.XPATH, '//*[@class="text-sm font-ligatures-none"]')
            )
        )
        logger.info("Risposta ricevuta da Copilot.")

        response_text = response_element.text
        logger.info(response_text)

        return response_text

    except Exception as e:
        # In caso di errore durante l'interazione, viene loggato il messaggio di errore
        logger.error(
            f"Si è verificato un errore durante l'interazione con Copilot: {e}"
        )
    finally:
        # Garantiamo che il driver venga sempre chiuso, anche se si è verificato un errore
        if driver:
            try:
                logger.info("Chiusura del browser.")
                driver.quit()
            except Exception as e:
                logger.error(f"Errore durante la chiusura del browser: {e}")
