import psycopg2
import Scraping as scraping
import time
import os
import logging

class database:

    connection = object
    idlink = 0
    link = ""
    nombre=""
    autor=""
    fecha=""
    precio = 0

    def __init__(self): 
        self.connection = psycopg2.connect(
                user = os.getenv('POSTGRES_USER'),
                password = os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                database=os.getenv('POSTGRES_DB')
            )
        logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,datefmt="%d-%m-%Y %H:%M:%S")

    def setPrecio(self):

        try:
            logging.info("Ejecutando SetPrecio.....")
            insert_query = "INSERT INTO precio (idlink, precio, fecha, nuevo) values ({}, {}, '{}', {}) RETURNING id;".format(self.idlink, self.precio, self.fecha, True)
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            id_inserted = cursor.fetchone()[0]
            self.connection.commit()
            count = cursor.rowcount
            logging.info("Retorno datos SetPrecio")
            return id_inserted

        except (Exception, psycopg2.Error) as error:
            logging.info("Error en SetPrecio")
            return error

    def getListalink(self):

        try:
            logging.info("Ejecutando GetListaLink...")
            self.updatePrecioNuevo()
            logging.info("1")

            select_query = '''SELECT link.id,
                link.link        
            FROM public.link AS link
            '''
            logging.info("2")
            cursor = self.connection.cursor()
            logging.info("3")
            cursor.execute(select_query)
            datos = cursor.fetchall()
            logging.info("4")
            self.connection.commit()
            logging.info("5")
            arrayprecios = []
            logging.info(":::::::::::::::::::::::")
            logging.info(datos)
            logging.info(":::::::::::::::::::::::")
            for row in datos:
                logging.info("6")
                scr = scraping.scraping()
                logging.info("7")
                scr.url = row[1]
                logging.info("7.1")
                result = scr.scrap()
                logging.info("8")
                select_query_precio_anterior = '''
                    SELECT precio.precio
                    FROM public.precio as precio
                    where precio.idlink = {} and
                    precio.nuevo = false
                    order by precio.fecha desc
                    limit 1
                '''.format(row[0])
                logging.info("9")
                cursor2 = self.connection.cursor()
                logging.info("10")
                cursor2.execute(select_query_precio_anterior)
                logging.info("11")
                datas = cursor2.fetchone()
                logging.info("12")
                self.connection.commit()
                logging.info("13")
                self.precio = scr.price
                logging.info("14")
                self.idlink = row[0]
                logging.info("5")
                self.fecha = time.strftime("%Y-%m-%d")
                logging.info("16")
                if(datas is None):
                    logging.info("17")
                    arrayprecios.append(self.setPrecio())
                elif((scr.price != datas[0])):
                    logging.info("18")
                    arrayprecios.append(self.setPrecio())

            logging.info("Retorna datos GetListaLink")
            return arrayprecios
        except (Exception, psycopg2.Error) as error:
            logging.info("Error en GetListaLink: {}".format(error))
            return error

    def updatePrecioNuevo(self):

        try:
            logging.info("Ejecutando UpdatePrecioNuevo...")
            update_query = "UPDATE public.precio SET nuevo=false"
            cursor = self.connection.cursor()
            cursor.execute(update_query)
            self.connection.commit()
            count = cursor.rowcount
            logging.info("Retorna datos UpdatePrecioNuevo")
            return count

        except (Exception, psycopg2.Error) as error:
            logging.info("Error en UpdatePrecioNuevo")
            return error