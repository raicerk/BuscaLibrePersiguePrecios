import Database as database
import time
import os
import threading
import logging

def thread_function():

    try:
        db = database.database()
    
        while True:        
            if time.strftime("%H:%M:%S") == os.getenv('HORA_SCRAPING'):
                db.getListalink()
                logging.info("Scraping realizado.")
            time.sleep(1)
    except Exception as error:
        logging.info(error)

if __name__ == "__main__":
    
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,datefmt="%d-%m-%Y %H:%M:%S")
    
    logging.info("Iniciando proceso...")
    x = threading.Thread(target=thread_function)
    x.start()