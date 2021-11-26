import psycopg2
from config import access_secrets
from flask import Flask, render_template, request, url_for, flash, redirect
#from werkzeug.exceptions import abort
from datetime import datetime
#from init_db import do_init


def connect():
    try:
        con = psycopg2.connect(
            dbname=access_secrets("fall-week7-2", "database", "latest"),
            password=access_secrets("fall-week7-2", "password", "latest"),
            host=access_secrets("fall-week7-2", "ip", "latest"),
            user=access_secrets("fall-week7-2", "username", "latest"),
            port=5432
        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return con


def get_post(post_id):
    try:
        con = connect()
        cursor = con.cursor()
        cursor.execute('SELECT * FROM posts WHERE id = %s',
                            (post_id,))
        post = cursor.fetchone()
        cursor.close()
        con.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # if con is not None:
    #     con.close()
    return post
    
# juttu = get_post(1)
# print(juttu)

# SQL = """ INSERT INTO "posts" (title, content)
#     VALUES (%s,%s);"""
# records_to_insert = (title, content)
# cursor.executemany(SQL, (records_to_insert,))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'do_not_touch_or_you_will_be_fired'


# this function is used to format date to a finnish time format from database format
# e.g. 2021-07-20 10:36:36 is formateed to 20.07.2021 klo 10:36

def format_date(post_date):
    post_date = str(post_date)
    isodate = post_date[:19]
    newdate = datetime.fromisoformat(isodate)
    return newdate.strftime('%d.%m.%Y') + ' klo ' + newdate.strftime('%H:%M')


# this index() gets executed on the front page where all the posts are
@app.route('/')
def index():
    try:
        con = connect()
        cursor = con.cursor()
        SQL = 'SELECT * FROM posts'
        cursor.execute(SQL)
        posts = cursor.fetchall()
        cursor.close()
        con.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    # we need to iterate over all posts and format their date accordingly
    sanakirja = []

    for row in posts:
        yksirowi = {'id': row[0], 'created': row[1], 'title': row[2], 'content': row[3]}
        sanakirja.append(yksirowi)

    for post in sanakirja:
        # using our custom format_date(...)
        post['created'] = format_date(post['created'])

    return render_template('index.html', posts=sanakirja)


# here we get a single post and return it to the browser
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    post_dictionary = {"id": post[0], "created": post[1], "title": post[2], "content": post[3]}
    post_dictionary['created'] = format_date(post_dictionary['created'])
    return render_template('post.html', post=post_dictionary)


# here we create a new post
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            try:
                con = connect()
                cursor = con.cursor()
                SQL = """ INSERT INTO "posts" (title, content)
                    VALUES (%s,%s);"""
                records_to_insert = (title, content)
                cursor.executemany(SQL, (records_to_insert,))
                con.commit()
                cursor.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if con is not None:
                    con.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)
    post_dictionary = {"id": post[0], "created": post[1], "title": post[2], "content": post[3]}
    post_dictionary['created'] = format_date(post_dictionary['created'])
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            try:
                con = connect()
                cursor = con.cursor()
                SQL = """ UPDATE posts
                    SET title = %s, content = %s
                    WHERE id = %s """
                records_to_insert = (title, content, id)
                cursor.executemany(SQL, (records_to_insert,))
                con.commit()
                cursor.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            finally:
                if con is not None:
                    con.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post_dictionary)


# Here we delete a SINGLE post.
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    post_title = {'title': post[2]}
    try:
        con = connect()
        cursor = con.cursor()
        SQL = """ DELETE FROM posts
              WHERE id = '%s'; """
        records_to_insert = (id,)
        cursor.execute(SQL, records_to_insert)
        con.commit()
        cursor.close()
        flash('"{}" was successfully deleted!'.format(post_title['title']))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()
    return redirect(url_for('index'))