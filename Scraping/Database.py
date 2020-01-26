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
            select_query = '''SELECT link.id,
                link.link        
            FROM public.link AS link
            '''
            cursor = self.connection.cursor()
            cursor.execute(select_query)
            datos = cursor.fetchall()
            self.connection.commit()
            arrayprecios = []
            for row in datos:
                scr = scraping.scraping()
                scr.url = row[1]
                result = scr.scrap()
                select_query_precio_anterior = '''
                    SELECT precio.precio
                    FROM public.precio as precio
                    where precio.idlink = {} and
                    precio.nuevo = false
                    order by precio.fecha desc
                    limit 1
                '''.format(row[0])
                cursor2 = self.connection.cursor()
                cursor2.execute(select_query_precio_anterior)
                datas = cursor2.fetchone()
                self.connection.commit()
                self.precio = scr.price
                self.idlink = row[0]
                self.fecha = time.strftime("%Y-%m-%d")
                if(datas is None):
                    arrayprecios.append(self.setPrecio())
                elif((scr.price != datas[0])):
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