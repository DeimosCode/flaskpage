from flask import Flask, render_template, request, url_for, redirect, jsonify
import mariadb


app = Flask(__name__)

#datos para conectar mysql
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'roort'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'cursos'

# Configura la conexión a la base de datos MariaDB
conexion = mariadb.connect(
    user="root",
    password="1234",
    host="127.0.0.1",  # Cambia esto a la dirección de tu servidor MariaDB si es necesario
    database="cursos"
)




@app.before_request
def before_request():
    print("antes de la peticion")
    
@app.after_request
def after_request(response):
    print("despues de la peticion")
    return response

@app.route('/')
def index():
    cursos = ['php','python','java','kotlin','dart','javascript']
    data={
        'titulo':'resortera.cl',
        'bienvenido':'!saludos',
        'cursos': cursos,
        'numeros_cursos': len(cursos)
    }
    return render_template('index.html',data=data)

@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre,edad):
    data={
        'titulo':'contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return "ok"

@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        cursor = conexion.cursor()
        sql = "SELECT codigo, nombre, creditos FROM cursos ORDER BY nombre ASC"
        cursor.execute(sql)
        cursos = cursor.fetchall()
        data['mensaje'] = 'exito'
        data['cursos'] = cursos
    except Exception as ex:
        data['mensaje'] = 'Error ...'
    return jsonify(data)

def pagina_no_encontrada(error):
    return render_template('404.html'), 404
    # return redirect(url_for('index'))

if __name__=='__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True,port=5000)