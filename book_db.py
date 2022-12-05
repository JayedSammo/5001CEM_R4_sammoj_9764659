'''
INITIALIZE DATABASE
Connection to database
Create tables in database
'''


from flask import Flask
from flask import render_template
import sqlite3 

# create the database file
con = sqlite3.connect('bookshop.db')
# create books table
con.execute('CREATE TABLE books(bookname VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, date DATETIME NOT NULL, ISBN int unsigned NOT NULL UNIQUE PRIMARY KEY, description TEXT, image TEXT NOT NULL, trade_price DOUBLE NOT NULL, retail_price DOUBLE NOT NULL, quantity int)')

con.close()  
# connect to database
con = sqlite3.connect('bookshop.db')
# insert data to books table
con.execute('INSERT INTO books(bookname, author, date, ISBN, description, image, trade_price, retail_price, quantity) VALUES ("Love Holds No Fear", "Kavya Dixit", "2020-11-18", 9781636697000, "...", "book-images/lovefear.jpg", 12.99, 9.99, 20),("A Silent Voice", "Yoshitoki Ōima", "2014-10-17", 9781632360595, "...", "book-images/silentvoice.jpg", 59.20, 49.99, 15),("The Lord of the Rings", "J. R. R. Tolkien", "1954-07-29", 9780007141326, "...", "book-images/lordrings.jpg", 19.99, 14.99, 20),("Harry Potter and the Philosophers Stone", "J. K. Rowling", "1997-06-26", 9780747532743, "...", "book-images/harrypotter1.jpg", 13.49, 9.99, 20),("The hobbit", "J. R. R. Tolkien", "1937-09-21", 9780547928227, "...", "book-images/hobbit.jpg", 11.91, 7.99, 20),("A Walk to Remember", "Nicholas Sparks", "1999-10-19", 9780446608954, "...", "book-images/walk.jpg", 8.33, 4.99, 20),("Twilight", "Stephenie Meyer", "2005-10-05", 9780316015844, "...", "book-images/twilight.jpg", 14.30, 9.99, 20),("A Game of Thrones", "George R. R. Martin", "1996-08-01", 9780006479888, "...", "book-images/gamethrones.jpg", 16.78, 9.99, 20),("Prince of Thorns", "Mark Lawrence", "2011-08-02", 9781937007683, "...", "book-images/princethorns.jpg", 8.99, 4.99, 15),("The Diary of a Young Girl", "Anne Frank", "1947-06-25", 9780553296983, "...", "book-images/thedairy.jpg", 9.99, 5.99, 20);')
# commit to database
con.commit()
con.close()  
# connect to database
con = sqlite3.connect('bookshop.db')
# create users table
con.execute('CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, pwd PASSWORD)')

con.close()
# connect to database
con = sqlite3.connect('bookshop.db')
# insert data into users table
con.execute('INSERT INTO users(username, pwd) VALUES ("admin", "p455w0rd"),("customer1", "p455w0rd"),("customer2", "p455w0rd");')
# commit to database
con.commit()
con.close()
