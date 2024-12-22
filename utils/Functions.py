import time

import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from Constants import info_to_extract


def concat_fields(fields):
    result = ' - '.join(fields)
    return result


def extract_pdf_data(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""

        # Extract text from all pages
        for page in pdf.pages:
            full_text += page.extract_text()

    return full_text


def run_copilot(input_text):
    driver = webdriver.Chrome()
    driver.get("https://copilot.microsoft.com/onboarding")

    time.sleep(5)

    element = driver.find_element(By.XPATH, '//*[@title="Inizia"]')
    element.click()

    time.sleep(2)

    question_box = driver.find_element(By.ID, "userInput")
    question_box.send_keys("Christian")
    question_box.send_keys(Keys.RETURN)

    time.sleep(2)

    element = driver.find_element(By.XPATH, '//*[@title="Avanti"]')
    element.click()

    time.sleep(2)

    question_box = driver.find_element(By.ID, "userInput")
    question_box.send_keys("Estrai le seguenti informazioni, se presenti, in formato json su una sola riga: " +
                           concat_fields(info_to_extract) +
                           "dal seguente testo non formattato: " +
                           input_text)
    question_box.send_keys(Keys.RETURN)

    time.sleep(10)

    response_element = driver.find_element(By.XPATH, '//*[@class="text-sm font-ligatures-none"]')
    response_text = response_element.text
    print(response_text)

    time.sleep(10)

    # Chiudere il browser
    driver.quit()

    return response_text
