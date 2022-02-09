from dataclasses import dataclass
from flask import Flask, render_template, request, session
from flask import jsonify

import pymysql
app = Flask(__name__)
app.secret_key = "@112"
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
                session["iduser"]= datos[0][0]                
                session["usuario"]= datos[0][1]
                session["nombre"]= datos[0][3]
                session["rol"]= datos[0][7]
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
#cursos
def obtener_cursos():
    try:
        conn = conexion()
        datos = []
        respuesta = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM cursos where estado = 1")
            datos = cursor.fetchall()
            for fila in datos:
                item={'id':fila[0],'curso':fila[1],'descripcion':fila[3],'precio':fila[4],'fknivel':fila[5]}
                respuesta.append(item)
        conn.close()
        return jsonify({'msj': respuesta})
    except:
        return jsonify({'msj': 'Error en la bd'})
def obtener_modulos(idcurso):
    try:
        conn = conexion()
        datos = []
        respuesta = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT modulocurso.idmodulocurso, modulocurso.url,modulocurso.titulo, modulocurso.descripcion FROM cursos INNER JOIN modulocurso ON cursos.idcursos = modulocurso.fkcursomodulo WHERE cursos.idcursos = '{}';".format(idcurso))
            datos = cursor.fetchall()
            i = 1
            for fila in datos:
                i += 1
                item={'nro': i , 'idmodulo':fila[0],'url':fila[1], 'titulo':fila[2], 'descripcion':fila[3], 'acceso': True}
                respuesta.append(item)             
        conn.close()
        return respuesta
    except:
        return jsonify({'msj': 'Error en la bd'})
def obtener_archivos(idcurso):
    try:
        conn = conexion()
        datos = []
        respuesta = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT modulocurso.idmodulocurso, archivoscurso.urlpdf FROM (cursos INNER JOIN modulocurso ON cursos.idcursos = modulocurso.fkcursomodulo) INNER JOIN archivoscurso ON modulocurso.idmodulocurso = archivoscurso.fkmodulocurso WHERE cursos.idcursos = '{}';".format(idcurso))
            datos = cursor.fetchall()
            i = 0
            for filapdf in datos:
                i += 1               
                item={'idmodulocurso':filapdf[0],'url':filapdf[1]}
                respuesta.append(item)           
        conn.close()
        return  respuesta
    except:
        return jsonify({'msj': 'Error en la bd'})
    
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/panel')
def panel():
    if "usuario" in session:
        return render_template("panel.html")
    return render_template("index.html")
#rutas usuario
@app.route('/registro')
def registro():
    return render_template("registro.html")
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
        rescorreo = doble_correo(request.json['correo'])        
        restelefono= doble_telefono(request.json['telefono'])        
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
    if "usuario" in session:
        urlvideo = obtener_modulos(1)
        urlpdf = obtener_archivos(1)
        
        return jsonify({'urlvideo': urlvideo,"urlpdf":urlpdf})
        
    return jsonify({'msj': "inicie session","estado":False})
@app.route("/get_cursos")

def get_cursos():
    datos = obtener_cursos()    

    return "da"
if __name__ == "__main__":
    app.run(debug=True)