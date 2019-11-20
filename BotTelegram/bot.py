import telebot
import time
import requests
import os
import json
from urllib.parse import urlparse
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot(os.getenv('TOKEN_TELEGRAM'))

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

    print(r.json())

    bot.send_message(message.chat.id, "Bienvenido a BuscaLibre persigue precios Bot")

    while True:
        if time.strftime("%H:%M:%S") == os.getenv('HORA_ALERTA'):
            res = requests.post("http://{}/librospreciosnuevos".format(os.getenv('API_HOST')), json={
                "idchat": message.from_user.id
            })
            miresponse = res.json()
            for lst in miresponse['lista']:
                print(lst)
                bot.send_message(message.chat.id, "El libro '{}' del autor '{}', a cambiado de precio, de ${} a un nuevo valor de ${}, el link del libro es: {}".format(
                    lst['nombre'], lst['autor'], lst['precioanterior'], lst['precionuevo'], lst['link']))
        time.sleep(1)

@bot.message_handler(commands=['seguir'])
def send_forward(message):
    bot.send_message(message.chat.id,"A partir de ahora, cualquier link de un libro de buscalibre que nos envies sera analizado y te avisaremos a penas el precio del libro cambie 🙂")
    bot.send_message(message.chat.id,"Para dejar de analizar los precios de un link de un libro usa el comando /parar")

@bot.message_handler(commands=['parar'])
def send_stop(message):
    
    res = requests.post("http://{}/librosactivossusuario".format(os.getenv('API_HOST')), json={
        "idchat": message.from_user.id
    })
    miresponse = res.json()
    
    markup = InlineKeyboardMarkup()
    for libro in miresponse['lista']:
        markup.row(InlineKeyboardButton("'{}' escrito por '{}'".format(libro["nombre"], libro["autor"]), callback_data=libro['id']))
    bot.send_message(message.chat.id, "Selecciona un libro para dejar de analizarlo:", reply_markup=markup)

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
        
        print(r.json())

        if r:
            bot.send_message(message_id,"Link registrado correctamente, te avisaremos apenas cambie el precio del libro 🙂")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    r = requests.post("http://{}/estadolibrousuario".format(os.getenv('API_HOST')), json={
        "idusuario": call.user_from.id,
        "idlink": call.data
    })

    print(r.json())

    opciones = []
    
    for iter in call.message.json["reply_markup"]["inline_keyboard"]:
        opciones.append(iter[0])

    filtrado = list(filter(lambda iter: iter["callback_data"] == call.data, opciones))

    bot.send_message(call.from_user.id, "Se elimino del analisis el libro {}".format(filtrado[0]["text"]))

@bot.message_handler(commands=['help', 'ayuda'])
def send_help(message):
    message_id = message.chat.id
    bot.send_message(message_id, "Ayuda con los comandos del bot")

bot.polling()