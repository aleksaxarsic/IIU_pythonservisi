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

#Ažuriranje knjige u potpunosti, sa svim parametrima
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    naziv = data.get('naziv')
    autor = data.get('autor')
    zanr = data.get('zanr')
    
    if not naziv or not autor or not zanr:
        return jsonify({'error': 'Nedostaju podaci'}), 400
    
    cursor = db.cursor()
    sql = "UPDATE books SET naziv = %s, autor = %s, zanr = %s WHERE id = %s"
    values = (naziv, autor, zanr, book_id)
    cursor.execute(sql, values)
    db.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'Knjiga nije pronađena'}), 404
    
    return jsonify({'message': 'Knjiga ažurirana'}), 200

#Delimično ažuriranje knjige
@app.route('/books/<int:book_id>', methods=['PATCH'])
def partial_update_book(book_id):
    data = request.json
    fields = []
    values = []

    if 'naziv' in data:
        fields.append("naziv = %s")
        values.append(data['naziv'])
    if 'autor' in data:
        fields.append("autor = %s")
        values.append(data['autor'])
    if 'zanr' in data:
        fields.append("zanr = %s")
        values.append(data['zanr'])

    if not fields:
        return jsonify({'error': 'Nema podataka za ažuriranje'}), 400

    values.append(book_id)
    fields_str = ', '.join(fields)
    sql = f"UPDATE books SET {fields_str} WHERE id = %s"
    cursor = db.cursor()
    cursor.execute(sql, tuple(values))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Knjiga nije pronađena'}), 404

    return jsonify({'message': 'Knjiga delimično ažurirana'}), 200

#Provera da li knjiga sa određenim id-em postoji u bazi
@app.route('/books/<int:book_id>', methods=['HEAD'])
def head_book(book_id):
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM books WHERE id = %s", (book_id,))
    exists = cursor.fetchone()

    if exists:
        return '', 200
    else:
        return '', 404

#Pretraživanje knjige po autoru 
@app.route('/books/search', methods=['GET'])
def search_books():
    autor = request.args.get('autor')
    cursor = db.cursor(dictionary=True)
    
    if autor:
        sql = "SELECT id, naziv, autor, zanr FROM books WHERE autor = %s"
        values = (autor,)
    else:
        sql = "SELECT id, naziv, autor, zanr FROM books"
        values = ()
    
    cursor.execute(sql, values)
    rows = cursor.fetchall()
    books = [dict(row) for row in rows]
    
    return jsonify(books)

#Dodavanje više knjiga odjednom
@app.route('/books/bulk', methods=['POST'])
def add_books_bulk():
    data = request.json
    books = data.get('books', [])
    
    if not books:
        return jsonify({'error': 'Nema knjiga za dodavanje'}), 400
    
    cursor = db.cursor()
    sql = "INSERT INTO books (naziv, autor, zanr) VALUES (%s, %s, %s)"
    
    values = [(book['naziv'], book['autor'], book['zanr']) for book in books]
    cursor.executemany(sql, values)
    db.commit()
    
    return jsonify({'message': 'Knjige dodate'}), 201

#Prikaz knjige po žanru
@app.route('/books/genre/<string:genre>', methods=['GET'])
def get_books_by_genre(genre):
    cursor = db.cursor(dictionary=True)
    sql = "SELECT id, naziv, autor, zanr FROM books WHERE zanr = %s"
    values = (genre,)
    cursor.execute(sql, values)
    rows = cursor.fetchall()
    books = [dict(row) for row in rows]
    
    if not books:
        return jsonify({'message': 'Nema knjiga za dati žanr'}), 404
    
    return jsonify(books)



if __name__ == '__main__':
    app.run(debug=True)
