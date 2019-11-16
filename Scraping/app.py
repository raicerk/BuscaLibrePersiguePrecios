import Database as database
import time
import os
import threading
import logging

def thread_function():

    db = database.database()
    
    while True:        
        if time.strftime("%H:%M:%S") == os.getenv('HORA_SCRAPING'):
            db.getListalink()
            logging.info("::::::: Scraping realizado :::::::")
        time.sleep(1)

if __name__ == "__main__":
    
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,datefmt="%H:%M:%S")
    logging.info("::::::: Iniciando proceso :::::::")
    x = threading.Thread(target=thread_function)
    x.start()