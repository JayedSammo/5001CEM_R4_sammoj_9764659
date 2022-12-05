'''
The application file
'''

# Interface, function and routes for server

# Import modules

from flask import Flask
import sqlite3
from flask import flash, session, url_for, render_template, request, redirect, make_response, jsonify, send_from_directory
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir


import datetime
import os
from werkzeug.utils import secure_filename

# configure the application
app = Flask(__name__)
# set the secret key to random string
app.secret_key = "its secret!"

# configure session application
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

'''
START
Input: None
Output: Books in the database
Return the books list
'''
@app.route('/')
@app.route('/home')
def home():
    # This is the home page which displays items in the bookshop.
    try:
        # connects to the bookshop.db database
        con = sqlite3.connect('bookshop.db')
        # set cursor for the connection
        cur = con.cursor();
        # execute SQL statement
        cur.execute("SELECT * FROM books")
        # fetch all rows for the query
        rows = cur.fetchall()
        # render home.html layout
        # books tables is fetched by rows query
        return render_template('home.html', books=rows)
    except Exception as e:
        # defines the argument as except statement
        print(e)
    finally:
        cur.close()
        con.close()

'''
REGISTER
Input: username and pwd
Output: Register user in users table
Implements registration with POST method
'''
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user reached route via POST
    if request.method == 'POST':
        # if username and pwd was submitted
        return do_the_registration(request.form['username'], request.form['pwd'])
    else:
        # if user reacher route via GET
        return show_the_registration_form();

def show_the_registration_form():
    # render reg.html for page register
    return render_template('reg.html',page=url_for('register'))

def do_the_registration(u,p):  
    # connect to database
    con = sqlite3.connect('bookshop.db')
    # execute statement; register username and password to the database
    con.execute("INSERT INTO users(username, pwd) VALUES(?,?);", (u, p))
    # commit to the database
    con.commit()
    # closes the connection
    con.close()
    # returns the defined function which shows the login form
    return show_the_login_form()

'''
LOGIN
Input: username and pwd
Output: login using users table
Implements the login with POST method
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    # if user reached route via POST
    if request.method == 'POST':
        # User log in by submitted form data
        try:
            # if username was submitted
            username = request.form["uname"]
            # if password was submitted
            password = request.form["pwd"]
            # if username and password is the admin
            if username == "admin" and password == "p455w0rd":
                # start session
                session["id"] = 0
                # session is admin
                session["username"] = "admin"
                # redirect to admin page
                return redirect('/admin')
            else:
                # if user not admin then login to database
                return do_the_login(request.form['uname'], request.form['pwd'])
        except Exception as e:
            print(e)
    # else if user reached route via GET
    else:
        # return the function
        return show_the_login_form()

def show_the_login_form():
    # render login.html page for login
    return render_template('login.html',page=url_for('login'))

def do_the_login(u,p):
    # clears all session
    session.clear()
    # connect database
    con = sqlite3.connect('bookshop.db')
    cur = con.cursor();
    # execute stament; login to the server; query database for username and pwd
    cur.execute("SELECT count(*) FROM users WHERE username=? AND pwd=?;", (u, p))
    if(int(cur.fetchone()[0]))>0:
        flash("Welcome!")
        # redirect to books page
        return redirect(url_for('.books'))
    else:
        # redirect to home page
        return redirect('/home')

'''
LOGOUT
Input: None
Output: Home
Returns the home page
'''
@app.route('/logout')
def logout():
    # clear the session
    session.clear()
    # session id is None
    session["id"] = None
    # session username is None
    session["username"] = None
    # redirect to home page
    return redirect('/home')

'''
BOOKS
Input: None
Output: Bookshop database
Returns the books in bookshop database
'''
@app.route('/books')
def books():
    # SHOW BOOKS IN THE DATABASE!
    try:
        # connect to database
        con = sqlite3.connect('bookshop.db')
        cur = con.cursor();
        # select all from books table
        cur.execute("SELECT * FROM books")
        # fetch all rows from books table
        rows = cur.fetchall()
        # render books.html page
        return render_template('books.html', books=rows)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()

'''
ADMIN
Input: 'admin' username
Output: admin.html
Returns the admin page
'''
@app.route('/admin')
def admin():
    # if user is admin
    if session is not None and 'username' in session and session['username'] == 'admin':
        try:
            # connect database
            con = sqlite3.connect('bookshop.db')
            cur = con.cursor();
            # execute statement; select all from books table
            cur.execute("SELECT * FROM books")
            # query fetch all rows
            rows = cur.fetchall()
            # render admin.html
            return render_template('admin.html', books=rows)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            con.close()
    # if user is not admin
    else:
        # return to login page
        return redirect('/login')

'''
STOCK
Input: None
Output: Book list
Return the stock for books table
'''
@app.route("/stock", methods=["GET", "POST"])
def stock():
    # if session is 'admin'
    if session is not None and 'username' in session and session['username'] == 'admin':
        try:
            # connect to database
            con = sqlite3.connect('bookshop.db')
            cur = con.cursor();
            # select all from books table
            cur.execute("SELECT * FROM books")
            # fetch all rows
            rows = cur.fetchall()
            # show the stock.html file as render
            return render_template("stock.html", books=rows)
        except Exception as e:
            print(e)
        finally:
            cur.close()
            con.close()
    else:
        # redirect to admin page
        return redirect('/admin')

'''
ADD STOCK PAGE
input: bookname, author, date, ISBN, description, image, trade_price, retail_price, quantity
output: add new book to database
Implement adding new books to stock
'''
@app.route('/addstock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # if bookname, author, date, ISBN, description, image, trade_price, retail_price, quantity was submitted
        return do_add_stock(request.form['bookname'], request.form['author'], request.form['date'], request.form['ISBN'], request.form['description'], request.files['image'], request.form['trade_price'], request.form['retail_price'], request.form['quantity'])
    else:
        # return the function for add stock form
        return show_add_stock_form();

def show_add_stock_form():
    # render add_stock.html template file and page url is add_stock
    return render_template('add_stock.html',page=url_for('add_stock'))

def do_add_stock(bookname,author,date,ISBN,description,image,trade_price,retail_price,quantity):
    try:
        # connect to database
        con = sqlite3.connect('bookshop.db')
        cur = con.cursor();

        # check if ISBN is 13 digits
        if ISBN is not None and len(ISBN) == 13:
            # select quantity for specific book ISBN
            cur.execute("SELECT quantity FROM books WHERE ISBN = ?;", (ISBN))
            # fetch one row
            row = cur.fetchone()
            # ensures row is present
            if row is not None:
                # quantity is sum of existing quantity and new quantity
                qty = row[0] + int(quantity)
                # updates the books table for quantity
                cur.execute("UPDATE books SET quantity = ? WHERE ISBN = ?;", (qty, ISBN))
                con.commit()
                cur.close()
                con.close()
                # returns the stock page
                return redirect('/stock')
            else:
                # save the uploaded image
                image.save(os.path.join('static/images', image.filename))
                # insert new book data
                cur.execute("INSERT INTO books(bookname, author, date, ISBN, description, image, trade_price, retail_price, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", (bookname, author, date, ISBN, description, image, trade_price, retail_price, quantity))
                con.commit()
                con.close()
                # returns the stock page
                return redirect('/stock')
        else:
            # render add_stock.html page
            return render_template("add_stock.html")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()


'''
BOOKSHOP CART
GET: get cart data
POST: add book to cart
'''
@app.route('/add', methods=['POST', 'GET'])
def add_books_to_cart():
    cursor = None
    try:
        # if ISBN was submitted
        ISBN = request.form['ISBN']
        # if quantity was submitted
        quantity = int(request.form['quantity'])

        # if method is POST
        if request.method == 'POST':
            
            # connect to database
            con = sqlite3.connect('bookshop.db')
            cur = con.cursor();
            # select all from books table for given ISBN
            cur.execute("SELECT * FROM books WHERE ISBN = ?;", [ISBN])
            # fetch one row
            row = cur.fetchone()
            # create an item array
            itemArray = { row[3] : {'bookname' : row[0], 'ISBN' : row[3], 'quantity' : quantity, 'trade_price' : row[6], 'image' : row[5], 'total_price' : quantity * row[6], 'postage' : quantity + 2}}
            # print the array
            print('itemArray is', itemArray)

            # sets the value to 0
            all_total_price = 0
            # sets the value to 0
            all_total_quantity = 0

            session.modified = True

            # if there is item in cart session
            if 'cart_item' in session:
                # prints the session
                print('in session')
                # checks if the row is in cart session
                if row[3] in session['cart_item']:
                    for key, value in session['cart_item'].items():
                        # set as key
                        if row[3] == key:
                            # sets key for quantity
                            old_quantity = session['cart_item'][key]['quantity']
                            # calculates total quantity
                            total_quantity = old_quantity + quantity
                            session['cart_item'][key]['quantity'] = total_quantity
                            session['cart_item'][key]['total_price'] = total_quantity * row[6]
                            session['cart_item'][key]['postage'] = float(total_quantity + 2)
                            
                else:
                    session['cart_item'] = array_merge(session['cart_item'], itemArray)

                for key, value in session['cart_item'].items():
                    individual_quantity = int(session['cart_item'][key]['quantity'])
                    individual_price = float(session['cart_item'][key]['total_price'])
                    individual_postage = float(session['cart_item'][key]['postage'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price + individual_postage

            else:
                session['cart_item'] = itemArray
                # calculates final amount for quantity
                all_total_quantity = all_total_quantity + quantity
                # calculates final amount of total price
                all_total_price = all_total_price + quantity * row[6] + (quantity + 2)

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = float(all_total_price)

            # redirect to books page
            return redirect('/books')

        # if method is get
        else:
            # redirect to home page
            return redirect('/home')
            
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
        
'''
CHECKOUT
Input: None
Output: checkout.html
Implements the checkout system
'''
@app.route('/checkout')
def checkout():
    # render checkout file
    return render_template('checkout.html')

'''
PAYMENT
Input: None
Output: payment.html
Shows the dummy payment system
'''
@app.route('/pay')
def pay():
    # render payment file
    return render_template('payment.html')

'''
CART
Shows cart items
'''
@app.route('/cart')
def cart():
    # render cart file
    return render_template('cart.html')

'''
EMPTY CART
Remove all books from cart.
'''
@app.route('/empty')
def empty_cart():
	try:
		# clear the session
        session.clear()
		# redirect to books page
        return redirect('/books')
	except Exception as e:
		print(e)

'''
DELETE BOOK
Remove a book from cart
'''
@app.route('/delete/<int:ISBN>')
def delete_book(ISBN):
	try:
		all_total_price = 0
		all_total_quantity = 0
		session.modified = True
		
		# get the book to remove
        for item in session['cart_item'].items():
			# get the book from cart
            if item[0] == ISBN:				
				session['cart_item'].pop(item[0], None)
				if 'cart_item' in session:
					# find the cart item
                    for key, value in session['cart_item'].items():
						individual_quantity = int(session['cart_item'][key]['quantity'])
						individual_price = float(session['cart_item'][key]['total_price'])
						all_total_quantity = all_total_quantity + individual_quantity
						all_total_price = all_total_price + individual_price
				break
		# if no book in cart, set quantity to 0
		if all_total_quantity == 0:
			session.clear()
		else:
			# remove book and set quantity and price
            session['all_total_quantity'] = all_total_quantity
			session['all_total_price'] = all_total_price
		return redirect('/cart')
	except Exception as e:
		print(e)
		
'''
MERGE TWO ARRAY
'''
def array_merge( first_array , second_array ):
	if isinstance( first_array , list ) and isinstance( second_array , list ):
		return first_array + second_array
	elif isinstance( first_array , dict ) and isinstance( second_array , dict ):
		return dict( list( first_array.items() ) + list( second_array.items() ) )
	elif isinstance( first_array , set ) and isinstance( second_array , set ):
		return first_array.union( second_array )
	return False		
		
if __name__ == "__app__":
    app.run()


