from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="mydb"
)

@app.route('/services', methods=['GET'])
def get_services():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM services")
    rows = cursor.fetchall()
    services = []
    for row in rows:
        service = {
            'id': row[0],
            'name': row[1],
            'description': row[2]
        }
        services.append(service)
    return jsonify(services)

@app.route('/services', methods=['POST'])
def add_service():
    name = request.json['name']
    description = request.json.get('description', '')
    cursor = db.cursor()
    sql = "INSERT INTO services (name, description) VALUES (%s, %s)"
    values = (name, description)
    cursor.execute(sql, values)
    db.commit()
    service_id = cursor.lastrowid
    return jsonify({'id': service_id, 'name': name, 'description': description})

@app.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    cursor = db.cursor()
    sql = "DELETE FROM services WHERE id = %s"
    values = (service_id,)
    cursor.execute(sql, values)
    db.commit()
    return jsonify({'message': 'Service deleted'})

if __name__ == '__main__':
    app.run(debug=True)

