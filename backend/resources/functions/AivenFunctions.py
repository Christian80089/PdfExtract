import logging

import pandas as pd
import psycopg2

# Configurazione del logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def create_database_and_table(
    host, port, user, password, db_name, new_db_name, table_name, table_schema
):
    try:
        # Connessione al database principale
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=db_name
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Creazione del database se non esiste
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{new_db_name}'")
        if cursor.fetchone() is None:
            cursor.execute(f"CREATE DATABASE {new_db_name}")
            logger.info(f"Database '{new_db_name}' creato con successo.")
        else:
            logger.info(f"Database '{new_db_name}' già esistente.")

        cursor.close()
        conn.close()

        # Connessione al nuovo database per creare la tabella
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=new_db_name
        )
        cursor = conn.cursor()

        # Creazione della tabella se non esiste
        cursor.execute(table_schema)
        conn.commit()
        logger.info(f"Tabella '{table_name}' pronta all'uso.")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.info("Errore:", e)


def write_csv_to_table(
    host,
    port,
    user,
    password,
    db_name,
    table_name,
    csv_path,
    insert_query,
    delimiter=",",
):
    try:
        # Connessione al database
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=db_name
        )
        cursor = conn.cursor()

        # Leggi l'Excel con Pandas
        df = pd.read_csv(csv_path, sep=delimiter)
        df = df.applymap(
            lambda x: str(x).replace(",", ".") if isinstance(x, str) else x
        )
        df = df.apply(
            pd.to_numeric, errors="ignore"
        )  # Converte le colonne numeriche, ignora quelle non numeriche

        # Overwrite dei dati nella tabella
        cursor.execute(f"TRUNCATE TABLE {table_name}")
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        logger.info(f"Dati caricati con successo nella tabella '{table_name}'.")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error("Errore:", e)


def write_df_to_table(
    host, port, user, password, db_name, table_name, df, insert_query
):
    try:
        # Connessione al database
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=db_name
        )
        cursor = conn.cursor()

        # Usa df
        df = df.applymap(
            lambda x: str(x).replace(",", ".") if isinstance(x, str) else x
        )
        df = df.apply(
            pd.to_numeric, errors="ignore"
        )  # Converte le colonne numeriche, ignora quelle non numeriche

        # Overwrite dei dati nella tabella
        for _, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))

        conn.commit()
        logger.info(f"Dati caricati con successo nella tabella '{table_name}'.")

        cursor.close()
        conn.close()

    except Exception as e:
        logger.error("Errore:", e)
