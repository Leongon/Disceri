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

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/registro')
def registro():
    return render_template("registro.html")
@app.route('/panel')
def panel():
    return render_template("panel.html")
@app.route('/cursos')
def cursos():
    return render_template("cursos.html")
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
def log():    
    datos = login(request.json['usuario'], request.json['pass'])
    return datos
@app.route('/registrar_usuario',  methods=['POST', 'GET'])
def registrar_usuario():
    try:
        resusuario = doble_usuario(request.json['usuario'])
        print(resusuario)
        rescorreo = doble_correo(request.json['correo'])
        print(rescorreo)
        restelefono= doble_telefono(request.json['telefono'])
        print(restelefono)
        if (resusuario['duplicado'] or rescorreo['duplicado'] or restelefono['duplicado']) == False:
            conn = conexion()
            with conn.cursor() as cursor:
                sql = "INSERT INTO dbDesire.usuarios (usuario, pass, nombres, apellidos, correo, telefono, fkrol, estado)VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}','1','1');".format(request.json['usuario'],request.json['password'],request.json['nombres'],request.json['apellidos'],request.json['correo'],request.json['telefono'])
                cursor.execute(sql)
                conn.commit()                
            return ({"ingreso" : True,'msj': 'Registro correcto'})                
        else:
            
            return ({ "ingreso":False,"dato":(resusuario,rescorreo,restelefono),'msj': 'Datos duplicados'})
    except:
        return
@app.route("/inicio")
def home():
    return render_template("inicio.html")
if __name__ == "__main__":
    app.run(debug=True)
