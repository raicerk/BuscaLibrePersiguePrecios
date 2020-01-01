import psycopg2
import os
import Scraping as scraping
import logging
import datetime


class database:

    connection = object
    link = ""
    idusuario = 0
    idlink = 0
    idchat = 0

    def __init__(self):
        logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,datefmt="%H:%M:%S")
        self.connection = psycopg2.connect(
                user = os.getenv('POSTGRES_USER'),
                password = os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                database=os.getenv('POSTGRES_DB')
            )

    def setLink(self):

        try:
            scr = scraping.scraping()
            scr.url = self.link
            result = scr.scrap()
            logging.info(result)
            insert_query = "INSERT INTO link (link, nombre, autor, estado) values ('{}','{}','{}',{}) RETURNING id;".format(self.link, scr.name, scr.author, True)
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            id_inserted = cursor.fetchone()[0]
            self.connection.commit()
            count = cursor.rowcount
            logging.info(count, "Record inserted successfully into table")
            logging.info(id_inserted, "ID inserted successfully into table")
            return id_inserted

        except (Exception, psycopg2.Error) as error:
            logging.error(error)

    def setUsuarioLink(self):

        try:
            insert_query = "INSERT INTO usuario_link (idusuario, idlink, estado) values ('{}',{}, {}) RETURNING id".format(self.idusuario, self.idlink, True)
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            id_inserted = cursor.fetchone()[0]
            self.connection.commit()
            count = cursor.rowcount
            logging.info(count, "Record inserted successfully into table")
            logging.info(id_inserted, "ID inserted successfully into table")
            return id_inserted

        except (Exception, psycopg2.Error) as error:
            logging.info(error)

    def setUsuario(self):

        try:
            insert_query = "INSERT INTO usuariotelegram (idusuario, idchat, estado) values ('{}',{},{}) RETURNING id;".format(self.idusuario,self.idchat, True)
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            id_inserted = cursor.fetchone()[0]
            self.connection.commit()
            count = cursor.rowcount
            logging.info(count, "Record inserted successfully into table")
            logging.info(id_inserted, "ID inserted successfully into table")
            return id_inserted

        except (Exception, psycopg2.Error) as error:
            logging.info(error)

    def getListaPreciosUsuarioChat(self):
        
        try:
            select_query = '''SELECT link.link,
                    link.nombre,
                    link.autor,
                    precio.fecha,
                    precio.precio,
                    link.id
            FROM public.usuariotelegram AS usutel
            INNER JOIN public.usuario_link AS usulink
            ON usutel.idusuario = usulink.idusuario
            INNER JOIN public.link AS link
            ON usulink.idlink = link.id
            INNER JOIN public.precio AS precio
            ON link.id = precio.idlink
            WHERE 
            usutel.idchat = {} AND
            usutel.estado = true AND
            precio.nuevo = true
            '''.format(self.idchat)

            cursor = self.connection.cursor()
            cursor.execute(select_query)
            datos = cursor.fetchall()                
            self.connection.commit()
            arraylibros = []
            for row in datos:

                select_query_precio_anterior = '''
                    SELECT precio.fecha,
                            precio.precio
                    FROM public.precio as precio
                    where precio.idlink = {} and
                    precio.nuevo = false
                    order by precio.fecha desc
                    limit 1
                '''.format(row[5])

                cursor2 = self.connection.cursor()
                cursor2.execute(select_query_precio_anterior)
                datas = cursor2.fetchone()               
                self.connection.commit()

                arraylibros.append({
                    "link":row[0],
                    "nombre": row[1],
                    "autor":row[2],
                    "fechanuevo":row[3].strftime("%d-%m-%Y"),
                    "precionuevo":row[4],
                    "idlink": row[5],
                    "fechaanterior":datas[0].strftime("%d-%m-%Y"),
                    "precioanterior":datas[1]
                })
            return arraylibros
        except (Exception, psycopg2.Error) as error:
            logging.info(error)

    def getListaLibrosActivos(self):
        try:
            select_query = '''select link.id,
                    link.nombre,
                    link.autor,
                    usutel.idchat
            from usuariotelegram as usutel
            inner join usuario_link usulink
            on usutel.idusuario = usulink.idusuario
            inner join link as link
            on usulink.idlink = link.id
            where usutel.idchat = {} and
            usulink.estado = true
            '''.format(self.idchat)

            cursor = self.connection.cursor()
            cursor.execute(select_query)
            datos = cursor.fetchall()                
            self.connection.commit()
            arraylibros = []
            for row in datos:
                arraylibros.append({
                    "id":row[0],
                    "nombre": row[1],
                    "autor":row[2],
                    "idusuario": row[3]
                })
            return arraylibros
        except (Exception, psycopg2.Error) as error:
            logging.info(error)
            return error

    def set_estadolinkusuario(self):
        
        try:
            update_query = "UPDATE public.usuario_link SET estado = false WHERE idusuario={} AND idlink={};".format(self.idusuario, self.idlink)
            cursor = self.connection.cursor()
            cursor.execute(update_query)
            self.connection.commit()
            count = cursor.rowcount
            logging.info(count, "Record updated successfully into table")
            return count

        except (Exception, psycopg2.Error) as error:
            logging.info(error)

    def getUsuariosConLinkYLibros(self):

        try:

            sq = '''select ul.idusuario 
            from usuario_link ul
            where ul.estado = true
            group by ul.idusuario
            '''

            dat = self.select(sq)

            arrayListaNotificar = []

            for usuario in dat:

                select_query = '''SELECT link.link,
                        link.nombre,
                        link.autor,
                        precio.fecha,
                        precio.precio,
                        link.id
                FROM public.usuariotelegram AS usutel
                INNER JOIN public.usuario_link AS usulink
                ON usutel.idusuario = usulink.idusuario
                INNER JOIN public.link AS link
                ON usulink.idlink = link.id
                INNER JOIN public.precio AS precio
                ON link.id = precio.idlink
                WHERE 
                usutel.idchat = {} AND
                usutel.estado = true AND
                usulink.estado = true AND
                precio.nuevo = true
                '''.format(usuario[0])

                datos = self.select(select_query)        
                self.connection.commit()
                arraylibros = []
                for row in datos:
                    
                    select_query_precio_anterior = '''
                        SELECT precio.fecha,
                                precio.precio
                        FROM public.precio as precio
                        where precio.idlink = {} and
                        precio.nuevo = false
                        order by precio.fecha desc
                        limit 1
                    '''.format(row[5])

                    datas = self.select(select_query_precio_anterior)

                    if (len(datas) == 0):
                        datas.append((datetime.datetime.now(), 0))

                    select_query_precio_mejor = '''
                        select min(precio)
                        FROM public.precio as precio
                        where precio.idlink = {} and
                        precio.nuevo = false and
                        precio.precio > 0
                    '''.format(row[5])

                    data3 = self.select(select_query_precio_mejor)

                    if (data3[0][0] is None):
                        data3[0] = (row[4],)

                    arraylibros.append({
                        "link":row[0],
                        "nombre": row[1],
                        "autor":row[2],
                        "fechanuevo":row[3].strftime("%d-%m-%Y"),
                        "precionuevo":row[4],
                        "idlink": row[5],
                        "fechaanterior":datas[0][0].strftime("%d-%m-%Y"),
                        "precioanterior":datas[0][1],
                        "preciomejor": data3[0][0]
                    })

                arrayListaNotificar.append({
                    'idchat': usuario[0],
                    'libros': arraylibros
                })

            return arrayListaNotificar
        except (Exception, psycopg2.Error) as error:
            logging.info("***************************")
            logging.info(error)
            logging.info("***************************")
            return error

    def select(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        datos = cursor.fetchall()                
        self.connection.commit()
        return datos