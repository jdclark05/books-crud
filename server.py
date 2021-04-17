from flask import Flask,render_template,redirect,request
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)

@app.route('/')
def index():
    return redirect("/authors")

@app.route('/authors', methods=['GET'])
def authors():
    query = "SELECT * FROM authors;"
    authors = connectToMySQL('books_schema').query_db(query)
    return render_template("authors.html",authors=authors)

@app.route('/books', methods=['GET'])
def books():
    query = "SELECT * FROM books;"
    books = connectToMySQL('books_schema').query_db(query)
    return render_template("books.html", books=books)

@app.route('/add_author', methods=["POST"])
def add_author():
        query = "INSERT INTO authors (first_name, last_name) VALUES (%(first_name)s, %(last_name)s);"
        data = {
            "first_name":request.form['first_name'],
            "last_name":request.form['last_name']
        }
        authors = connectToMySQL('books_schema').query_db(query, data)
        return redirect("/")

@app.route('/add_book', methods=["POST"])
def add_book():
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        data = {
            "title":request.form['title'],
            "num_of_pages":request.form['num_of_pages']
        }
        books = connectToMySQL('books_schema').query_db(query, data)
        return redirect("/books")


@app.route('/author_show/<int:author_id>', methods=['GET', 'POST'])
def author_show(author_id):
        query ="SELECT authors.id AS author_id, authors.first_name, authors.last_name, books.id AS book_id, books.title, books.num_of_pages FROM books RIGHT JOIN favorites ON favorites.book_id = books.id RIGHT JOIN authors on favorites.author_id = authors.id WHERE authors.id = %(author_id)s;"
        data = {
            "author_id":author_id
        }
        favorites = connectToMySQL('books_schema').query_db(query, data)
        query = "SELECT * FROM books WHERE id NOT IN (SELECT book_id FROM favorites WHERE author_id=%(author_id)s)"
        notLiked = connectToMySQL('books_schema').query_db(query, data)
        authors = connectToMySQL('books_schema').query_db("SELECT * FROM authors WHERE id=%(id)s;",{
            "id":author_id
        })
        return render_template("/author_show.html", favorites=favorites, notLiked=notLiked, author_id=author_id,author=authors[0])

@app.route('/book_show/<int:book_id>', methods=['GET', 'POST'])
def book_show(book_id):
        query = "SELECT authors.id AS author_id, authors.first_name, authors.last_name, books.id AS book_id, books.title FROM books RIGHT JOIN favorites ON favorites.book_id = books.id RIGHT JOIN authors on favorites.author_id = authors.id WHERE books.id = %(book_id)s;"
        data = {
            "book_id":book_id
        }
        favorites = connectToMySQL('books_schema').query_db(query, data)
        query = "SELECT * FROM authors WHERE id NOT IN (SELECT author_id FROM favorites WHERE book_id=%(book_id)s)"
        notLiked = connectToMySQL('books_schema').query_db(query, data)
        books = connectToMySQL('books_schema').query_db("SELECT * FROM books WHERE id=%(id)s;",{
            "id":book_id
        })
        return render_template("/book_show.html", favorites=favorites, notLiked=notLiked, book_id=book_id,book=books[0])

@app.route('/book_fav_update/<int:book_id>', methods=["POST"])
def book_fav_update(book_id):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        data = {
            'book_id': book_id,
            "author_id":request.form['author_id'],
        }
        books= connectToMySQL('books_schema').query_db(query, data)
        return redirect(f"/book_show/{book_id}")

@app.route('/author_fav_update/<int:author_id>', methods=["POST"])
def author_fav_update(author_id):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        data = {
            'author_id': author_id,
            "book_id":request.form['book_id']
        }
        authors= connectToMySQL('books_schema').query_db(query, data)
        return redirect(f"/author_show/{author_id}")

if __name__ == "__main__":
    app.run(debug=True)