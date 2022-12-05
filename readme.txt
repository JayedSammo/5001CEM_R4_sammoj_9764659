Terminal:
$ sudo apt update

Change Directory:
$ cd Bookshop

Virtual Environment Setup:
$ sudo apt-get install python3-venv

Create a Virtual Environment:
$ python3 -m venv venv

Activate Virtual Environment:
$ . venv/bin/activate

Export Flask:
$ export FLASK_APP=app

Run Flask:
$ flask run --host=0.0.0.0

URL:
https://mercuryformula-vertigocomet-5000.codio-box.uk
{server port must be 5000 for Flask}
$ ctrl+c                            (Exit host)

Install Flask:
$ pip install Flask

Database Setup:
$ pip install Flask-SQLAlchemy

Cross-Site:
$ pip install flask-cors

Database SQLite3:
$ sudo apt-get install sqlite3

SQLite3 initialize:
$ sqlite3 mydatabase.db

SQLite3 commands:
sqlite> .tables
sqlite> select * from students;     (students is table name)
sqlite> insert into students values('a', x);
sqlite> ctrl+D                      (Exit sqlite3)


Further installs:
$ pip install cs50                  (Command line tool)
$ pip install flask_session         (Server-side session)
$ pip install passlib               (Password hashing library)
$ pip install flask_jsglue          (Hook flask with front end)


GITHUB-

$ git config --global user.name "sammoj"

$ git config --global user.email "sammoj@coventry.ac.uk"

$ git config --global push.default matching

$ git config --global alias.co checkout

Initialize Git:
$ git init

$ git add .

$ git remote add origin git@github.coventry.ac.uk:5001CEM-2122/5001CEM_R4_sammoj_9764659.git

$ git commit -am 'initial commit'

$ git push -u origin master

$ git add .

$ git commit -am 'comment'

$ git push


