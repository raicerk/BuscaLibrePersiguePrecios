import telebot
import time
import requests
import os
import json
from urllib.parse import urlparse
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import logging
import formato as frm

bot = telebot.TeleBot(os.getenv('TOKEN_TELEGRAM'))


def hilo():

    try:
        while True:
            if time.strftime("%H:%M:%S") == os.getenv('HORA_ALERTA'):
                res = requests.post(
                    "http://{}/librospreciosnuevos".format(os.getenv('API_HOST')))
                miresponse = res.json()
                for lst in miresponse['datos']:
                    for libro in lst['libros']:
                        bot.send_message(lst['idchat'],
"""El libro '{}' del autor '{}' a cambiado de precio,
su mejor precio fue ${:miles}
su precio anterior era de ${:miles}
su precio actual es de ${:miles}
el link del libro es: {}""".format(
                            libro['nombre'],
                            libro['autor'],
                            frm.formato(libro['preciomejor']),
                            frm.formato(libro['precioanterior']),
                            frm.formato(libro['precionuevo']),
                            libro['link'])
                        )
            time.sleep(1)
    except (Exception) as error:
        logging.info(error)


def is_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message):

    r = requests.post("http://{}/creausuario".format(os.getenv('API_HOST')), json={
        "idusuario": message.chat.id,
        "idchat": message.from_user.id
    })

    bot.send_message(
        message.chat.id, "Bienvenido a BuscaLibre persigue precios Bot")
    bot.send_message(
        message.chat.id, "A partir de ahora, cualquier link de un libro de buscalibre que nos envies sera analizado y te avisaremos a penas el precio del libro cambie 🙂")
    bot.send_message(
        message.chat.id, "Para dejar de analizar los precios de un link de un libro usa el comando /parar")


@bot.message_handler(commands=['parar'])
def send_stop(message):

    res = requests.post("http://{}/librosactivossusuario".format(os.getenv('API_HOST')), json={
        "idchat": message.from_user.id
    })
    miresponse = res.json()

    markup = InlineKeyboardMarkup()
    for libro in miresponse['lista']:
        markup.row(InlineKeyboardButton("'{}' escrito por '{}'".format(
            libro["nombre"], libro["autor"]), callback_data=libro['id']))
    bot.send_message(
        message.chat.id, "Selecciona un libro para dejar de analizarlo:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def echo_all(message):

    if is_url(message.text):

        user_id = message.from_user.id
        message_id = message.chat.id
        message_text = message.text

        r = requests.post("http://{}/almacenaLink".format(os.getenv('API_HOST')), json={
            "link": message_text,
            "idusuario": user_id,
            "idchat": message_id
        })

        if r:
            bot.send_message(
                message_id, "Link registrado correctamente, te avisaremos apenas cambie el precio del libro 🙂")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    r = requests.post("http://{}/estadolibrousuario".format(os.getenv('API_HOST')), json={
        "idusuario": call.from_user.id,
        "idlink": call.data
    })

    opciones = []

    for iter in call.message.json["reply_markup"]["inline_keyboard"]:
        opciones.append(iter[0])

    filtrado = list(
        filter(lambda iter: iter["callback_data"] == call.data, opciones))

    bot.send_message(call.from_user.id, "Se elimino del analisis el libro {}".format(
        filtrado[0]["text"]))


@bot.message_handler(commands=['help', 'ayuda'])
def send_help(message):
    message_id = message.chat.id
    bot.send_message(message_id, "Ayuda con los comandos del bot")

@bot.message_handler(commands=['stop'])
def send_stop(message):

    r = requests.post("http://{}/disableusuario".format(os.getenv('API_HOST')), json={
        "idusuario": message.from_user.id
    })

    bot.send_message(message.chat.id, "Se ha desactivado BuscaLibre persigue precios Bot")

if __name__ == "__main__":

    logging.basicConfig(format="%(asctime)s: %(message)s",
                        level=logging.INFO, datefmt="%H:%M:%S")

    threading.Thread(target=hilo).start()

    bot.polling()
