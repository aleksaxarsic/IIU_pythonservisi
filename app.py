from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Netflix.2024!",
    database="mydb"
)

@app.route('/books', methods=['GET'])
def get_books():
    cursor = db.cursor()
    cursor.execute("SELECT id, naziv, autor, zanr FROM books")
    rows = cursor.fetchall()
    books = []
    for row in rows:
        book = {
            'id': row[0],
            'naziv': row[1],
            'autor': row[2],
            'zanr': row[3]
        }
        books.append(book)
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    naziv = data.get('naziv')
    autor = data.get('autor')
    zanr = data.get('zanr')
    
    if not naziv or not autor or not zanr:
        return jsonify({'error': 'Nedostaju podaci'}), 400
    
    cursor = db.cursor()
    sql = "INSERT INTO books (naziv, autor, zanr) VALUES (%s, %s, %s)"
    values = (naziv, autor, zanr)
    cursor.execute(sql, values)
    db.commit()
    book_id = cursor.lastrowid
    return jsonify({'id': book_id, 'naziv': naziv, 'autor': autor, 'zanr': zanr}), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    cursor = db.cursor()
    sql = "DELETE FROM books WHERE id = %s"
    values = (book_id,)
    cursor.execute(sql, values)
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Knjiga nije pronađena'}), 404
    
    return jsonify({'message': 'Knjiga obrisana'}), 200

if __name__ == '__main__':
    app.run(debug=True)
