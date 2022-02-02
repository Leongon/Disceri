from flask import Flask, render_template, request
from flask import jsonify

import pymysql
app = Flask(__name__)
# Parametros para la conexion
def conexion():
    return pymysql.connect(host='localhost',
                            user='root',
                            password='',
                            db='dbdesire')

# Definir funciones para las consultas
#Usuarios
def login(usuario, password):
    try:
        conn = conexion()
        datos = []
        respuesta = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios where usuario = '{0}' and pass = '{1}'".format(usuario, password))
            datos = cursor.fetchall()
            if not len(datos) == 0:
                conn.close()
                return {"acceso" : True, "msj": "Bienvenido"}
            else:
                conn.close()
                return {"acceso" : False, "msj": "El usuario o la contraseña son incorrectos"}     
    except:
        return jsonify({'msj': 'Error en la bd'})
def obtener_usuarios():
    try:
        conn = conexion()
        datos = []
        respuesta = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM usuarios where estado = 1")
            datos = cursor.fetchall()
            for fila in datos:
                item={'id':fila[0],'usuario':fila[1],'nombres':fila[3],'apellidos':fila[4],'correo':fila[5],'telefono':fila[6],'rol':fila[7]}
                respuesta.append(item)
        conn.close()
        return jsonify({'msj': respuesta})
    except:
        return jsonify({'msj': 'Error en la bd'})

def obtener_usuario(idUsuario):
    try:
        conn = conexion()
        datos = []
        respuesta = []
        with conn.cursor() as cursor:
            sql = "SELECT * FROM usuarios where id = '{0}'".format(idUsuario)
            cursor.execute(sql)
            datos = cursor.fetchall()          
            for fila in datos:
                item={'id':fila[0],'usuario':fila[1],'nombres':fila[3],'apellidos':fila[4],'correo':fila[5],'telefono':fila[6],'rol':fila[7]}
                respuesta.append(item)
        conn.close()
        return jsonify({'msj': respuesta})
    except:
        return jsonify({'msj': 'Error en la bd'})
def doble_usuario(usuario):
    try:
        conn = conexion()
        datos = []
        with conn.cursor() as cursor:
            sql = "SELECT * FROM usuarios where usuario = '{0}'".format(usuario)
            cursor.execute(sql)
            datos = cursor.fetchall()          
            if not len(datos) == 0:
                conn.close()
                return {"duplicado" : True, "msj": "El usuario ya fue registrado"}
            else:
                conn.close()
                return {"duplicado" : False, "msj": "Usuario disponible"}     
    except:
        return jsonify({'msj': 'Error en la bd'})
def doble_correo(correo):
    try:
        conn = conexion()
        datos = []
        with conn.cursor() as cursor:
            sql = "SELECT * FROM usuarios where correo = '{0}'".format(correo)
            cursor.execute(sql)
            datos = cursor.fetchall()          
            if not len(datos) == 0:
                conn.close()
                return {"duplicado" : True, "msj": "El correo ya fue registrado"}
            else:
                conn.close()
                return {"duplicado" : False, "msj": "Correo disponible"}     
    except:
        return jsonify({'msj': 'Error en la bd'})
def doble_telefono(telefono):
    try:
        conn = conexion()
        datos = []
        with conn.cursor() as cursor:
            sql = "SELECT * FROM usuarios where telefono = '{0}'".format(telefono)
            cursor.execute(sql)
            datos = cursor.fetchall()          
            if not len(datos) == 0:
                conn.close()
                return {"duplicado" : True, "msj": "El numero telefonico ya fue registrado"}
            else:
                conn.close()
                return {"duplicado" : False, "msj": "Numero telefonico disponible"}     
    except:
        return jsonify({'msj': 'Error en la bd'})

def registrar_usuario(usuario, password, nombre, apellido, correo, telefono):
    try:
        resusuario = doble_usuario(usuario)
        rescorreo = doble_correo(correo)
        restelefono= doble_telefono(telefono)
        if(resusuario['duplicado'],rescorreo['duplicado'],restelefono['duplicado']) != True:
            conn = conexion()
            with conn.cursor() as cursor:
                sql = "".format()
                cursor.execute(sql)
            return jsonify({'msj': 'Registro correcto'})    
            conn.close()
        else:
            return jsonify({'msj': 'Ocurrio un error'})
    except:
        return
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/registro')
def registro():
    return render_template("Registro.html")
@app.route('/inicio')
def ini():
    return render_template("inicio.html")

@app.route('/get_usuarios', )
def get_usuarios():
    datos = obtener_usuarios()
    return datos
@app.route('/get_usuario')
def get_usuario():
    id = request.args.get('id', '')
    datos = obtener_usuario(id)
    return datos
@app.route('/login', methods=['POST', 'GET'])
def inicio():    
    datos = login(request.json['usuario'], request.json['pass'])
    return datos
@app.route('/registrar_usuario',  methods=['POST', 'GET'])
def registrar_usuarios():  
    datos = registrar_usuario(request.json['usuario'], request.json['nombre'], request.json['apellido'], request.json['correo'], request.json['telefono'])
    return datos
if __name__ == "__main__":
    app.run(debug=True)
