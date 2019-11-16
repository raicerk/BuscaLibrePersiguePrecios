import telebot
import time
import requests
import os

bot = telebot.TeleBot(os.getenv('TOKEN_TELEGRAM'))

@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.send_message(
        message.chat.id, "Bienvenido a BuscaLibre persigue precios Bot")
    r = requests.post("http://{}/creausuario".format(os.getenv('API_HOST')), json={
        "idusuario": message.chat.id,
        "idchat": message.from_user.id
    })

    print(r.json())

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
    user_id = message.from_user.id
    message_id = message.chat.id
    message_text = message.text
    if len(message_text.split('/seguir ')) > 0:
        link = message_text.split('/seguir ')[1]
        r = requests.post("http://{}/almacenaLink".format(os.getenv('API_HOST')), json={
            "link": link,
            "idusuario": user_id,
            "idchat": message_id
        })

        print(r.json())

    bot.send_message(message_id, link + "registrado correctamente!")


@bot.message_handler(commands=['help', 'ayuda'])
def send_help(message):
    message_id = message.chat.id
    bot.send_message(message_id, "Ayuda con los comandos del bot")


bot.polling()
