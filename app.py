from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta por defecto.
@app.route('/')
def index():
    return 'Index Page'

# Ruta de prueba.
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'Respuesta': 'pong!'})

# Ruta para obtener datos de la tabla.
@app.route('/tareas', methods=['GET'])
def obtTareas():
    cur = mysql.connection.cursor()
    cur.execute('Select * From Tareas')
    data = cur.fetchall()
    cur.close()
    #return jsonify({'Tareas': data})
    return jsonify({"tareas": data, "message": "Tareas's Records"})

# Ruta para obtener un dato de la tabla.
@app.route('/tareas/<int:idTarea>', methods=['GET'])
def obtTarea(idTarea):
    cur = mysql.connection.cursor()
    cur.execute('Select * From Tareas Where Id = %s', (idTarea, ))
    data = cur.fetchall()
    cur.close()
    if (len(data) > 0):
        return jsonify({'Tarea': data[0]})
    return jsonify({'Mensaje': 'Tarea no encontrada.'})

# Ruta para crear tarea pendiente.
@app.route('/tareas', methods=['POST'])
def agrTarea():
    print(request.json['fecha'])
    cur = mysql.connection.cursor()
    cur.execute("Insert Into Tareas (Descripcion, fecha, usuario, estado) VALUES (%s,Current_TimeStamp,%s,%s)", 
               (request.json['descripcion'], #request.json['fecha'], 
                request.json['usuario'], request.json['estado']))
    mysql.connection.commit()
    cur.execute('Select * From Tareas')
    data = cur.fetchall()
    cur.close()
    #return jsonify({'Tareas': data})
    return jsonify({"tareas": data, "message": "Tareas's Records"})

# Ruta para actualizar tarea pendiente.
@app.route('/tareas/<int:idTarea>', methods=['PUT'])
def editTarea(idTarea):
    cur = mysql.connection.cursor()
    cur.execute("""
            UpDate Tareas
              Set Descripcion = %s,
                  Fecha = %s,
                  Usuario = %s,
                  Estado = %s
              Where Id = %s
        """, (request.json['descripcion'], request.json['fecha'], 
              request.json['usuario'], request.json['estado'], 
              idTarea))
    mysql.connection.commit()
    cur.execute('Select * From Tareas Where Id = %s', (idTarea, ))
    data = cur.fetchall()
    cur.close()
    if (len(data) > 0):
        return jsonify({'Tarea actualizada:': data[0]})
    return jsonify({'Mensaje': 'Tarea no encontrada.'})

# Ruta para eliminar la tarea.
@app.route('/tareas/<int:idTarea>', methods=['DELETE'])
def borTarea(idTarea):
    cur = mysql.connection.cursor()
    cur.execute('Select * From Tareas Where Id = %s', (idTarea, ))
    data = cur.fetchall()
    cur.execute('Delete From Tareas Where Id = {0}'.format(idTarea))
    mysql.connection.commit()
    cur.close()
    if (len(data) > 0):
        return jsonify({'Tarea eliminada:': data[0]})
    return jsonify({'Mensaje': 'Tarea no encontrada.'})

if __name__ == '__main__':
    app.config['MYSQL_HOST'] = 'localhost' 
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'pendientes'
    mysql = MySQL(app)
    app.run(debug=True, port=4000)