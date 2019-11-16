import psycopg2
import os

class database:

    connection = object
    link = ""
    idusuario = 0
    idlink = 0
    idchat = 0

    def __init__(self): 
        self.connection = psycopg2.connect(
                user = os.getenv('POSTGRES_USER'),
                password = os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                database=os.getenv('POSTGRES_DB')
            )

    def setLink(self):

        try:
            insert_query = "INSERT INTO link (link, estado) values ('{}',{}) RETURNING id;".format(self.link, True)
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            id_inserted = cursor.fetchone()[0]
            self.connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into table")
            print (id_inserted, "ID inserted successfully into table")
            return id_inserted

        except (Exception, psycopg2.Error) as error:
            print(error)

    def setUsuarioLink(self):

        try:
            insert_query = "INSERT INTO usuario_link (idusuario, idlink) values ('{}',{}) RETURNING id".format(self.idusuario, self.idlink, True)
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            id_inserted = cursor.fetchone()[0]
            self.connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into table")
            print (id_inserted, "ID inserted successfully into table")
            return id_inserted

        except (Exception, psycopg2.Error) as error:
            print(error)

    def setUsuario(self):

        try:
            insert_query = "INSERT INTO usuariotelegram (idusuario, idchat, estado) values ('{}',{},{}) RETURNING id;".format(self.idusuario,self.idchat, True)
            cursor = self.connection.cursor()
            cursor.execute(insert_query)
            id_inserted = cursor.fetchone()[0]
            self.connection.commit()
            count = cursor.rowcount
            print (count, "Record inserted successfully into table")
            print (id_inserted, "ID inserted successfully into table")
            return id_inserted

        except (Exception, psycopg2.Error) as error:
            print(error)

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
            print(error)