from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='books', lazy=True)

# Create tables in the database
db.create_all()

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users=user_list)

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'condition': book.condition, 'owner_id': book.owner_id} for book in books]
    return jsonify(books=book_list)

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify(message='Book not found'), 404
    book_info = {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre, 'condition': book.condition, 'owner_id': book.owner_id}
    return jsonify(book=book_info)

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], genre=data['genre'], condition=data['condition'], owner_id=data['owner_id'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify(message='Book created successfully'), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)
    if not book:
        return jsonify(message='Book not found'), 404
    book.title = data['title']
    book.author = data['author']
    book.genre = data['genre']
    book.condition = data['condition']
    db.session.commit()
    return jsonify(message='Book updated successfully')

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify(message='Book not found'), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify(message='Book deleted successfully')

if __name__ == '__main__':
    app.run(debug=True)
