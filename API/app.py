from flask import Flask, jsonify, request
import json
import Database as db
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def get_ping():
    return jsonify({
        'respuesta': 'Hola Mundo'
    })

@app.route('/almacenaLink', methods=['POST'])
def set_link():

    try:
        data = request.json
    
        dtb = db.database()
    
        dtb.link = data['link']
        dtb.idlink = dtb.setLink()
        dtb.idusuario = data['idusuario']
        dtb.idchat = data['idchat']
        dtb.setUsuarioLink()
        
        return jsonify({
            'ok': 200
        })

    except Exception as error:
        print(error)
        return jsonify({
            'ok': 400
        })

@app.route('/creausuario', methods=['POST'])
def set_usuario():

    try:
        data = request.json
    
        dtb = db.database()
        dtb.idusuario = data['idusuario']
        dtb.idchat = data['idchat']
        dtb.setUsuario()
        
        return jsonify({
            'ok': 200
        })
    except Exception as error:
        print(error)
        return jsonify({
            'ok': 400
        })

@app.route('/librospreciosnuevos', methods=['POST'])
def get_preciosnuevos():

    try:
        data = request.json
    
        dtb = db.database()
        dtb.idchat = data['idchat']
        lista = dtb.getListaPreciosUsuarioChat()
        return jsonify({
            'ok': 200,
            "lista": lista
        })
    except Exception as error:
        print(error)
        return jsonify({
            'ok': 400
        })

@app.route('/librosactivossusuario', methods=['POST'])
def get_librosusuario():

    try:
        data = request.json
    
        dtb = db.database()
        dtb.idchat = data['idchat']
        lista = dtb.getListaLibrosActivos()
        return jsonify({
            'ok': 200,
            "lista": lista
        })
    except Exception as error:
        print(error)
        return jsonify({
            'ok': 400
        })

@app.route('/estadolibrousuario', methods=['POST'])
def set_estadolibrousuario():

    try:
        data = request.json
    
        dtb = db.database()
        dtb.idusuario = data['idusuario']
        dtb.idlink = data['idlink']
        updated = dtb.set_estadolinkusuario()
        return jsonify({
            'ok': 200
        })
    except Exception as error:
        print(error)
        return jsonify({
            'ok': 400
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
