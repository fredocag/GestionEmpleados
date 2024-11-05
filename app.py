from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

mysql = MySQL(app)

# Endpoint para crear un empleado
@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    name = data.get('name')
    job = data.get('job')
    salary = data.get('salary')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO employees (name, job, salary) VALUES (%s, %s, %s)", (name, job, salary))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Empleado creado exitosamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener un empleado por ID
@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
        employee = cursor.fetchone()
        cursor.close()
        if employee:
            return jsonify({'id': employee[0], 'name': employee[1], 'job': employee[2], 'salary': employee[3]})
        else:
            return jsonify({'message': 'Empleado no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para actualizar un empleado
@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()
    name = data.get('name')
    job = data.get('job')
    salary = data.get('salary')
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE employees SET name = %s, job = %s, salary = %s WHERE id = %s", (name, job, salary, id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Empleado actualizado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para eliminar un empleado
@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'Empleado eliminado exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para listar todos los empleados
@app.route('/employees', methods=['GET'])
def list_employees():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()
        employees_list = [{'id': emp[0], 'name': emp[1], 'job': emp[2], 'salary': emp[3]} for emp in employees]
        return jsonify(employees_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
