import telebot
import time
import requests
import os
import json
import threading
import logging

bot = telebot.TeleBot(os.getenv('TOKEN_TELEGRAM'))


def thread_function(message):

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

    


bot.polling(none_stop=False, interval=0, timeout=20)

if __name__ == "__main__":
    message = object
    threading.Thread(target=thread_function, args=(message,)).start()