from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
import sqlite3
import configparser
import os
import json
import subprocess
app = Flask(__name__)
DATABASE = 'facebook_auto_comment.db'
CONFIG_FILE = 'config.ini'
UPLOAD_FOLDER = 'cookies'

# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database table
def initialize_database():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS source_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            type TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to save configuration to config.ini
def save_config(api_key, cookies_filename):
    config = configparser.ConfigParser()
    config['TMProxy'] = {'APIKey': api_key}
    config['Cookies'] = {'AccountFacebook': cookies_filename}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# Initialize the database table before each request
@app.before_request
def before_request():
    initialize_database()

# Home page route
@app.route('/')
def home():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE is_commented = 1')
    rows = cursor.fetchall()
    conn.close()

    return render_template('home.html', rows=rows)

# Settings page route
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        url = request.form['url']
        post_type = request.form['type']

        # Insert the form data into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO source_posts (url, type) VALUES (?, ?)', (url, post_type))
        conn.commit()
        conn.close()

        return redirect(url_for('settings'))

    # Fetch all the source posts from the database
    conn = get_db_connection()
    source_posts = conn.execute('SELECT * FROM source_posts').fetchall()
    conn.close()

    return render_template('settings.html', source_posts=source_posts)

# Delete source post route
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM source_posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('settings'))

# Proxy and Cookies config page route
@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        api_key = request.form['api_key']
        cookies_file = request.files['cookies_file']

        # Save uploaded cookies file
        if cookies_file and cookies_file.filename.endswith('.json'):
            filename = 'cookies.json'
            cookies_file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            filename = ''

        # Save configuration to config.ini
        save_config(api_key, filename)

        return redirect(url_for('config'))

    # Read configuration from config.ini
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    api_key = config.get('TMProxy', 'APIKey', fallback='')
    cookies_filename = config.get('Cookies', 'AccountFacebook', fallback='')

    return render_template('config.html', api_key=api_key, cookies_filename=cookies_filename)





@app.route('/posts')
def posts():
    # Load data from post.json file
    post = {}
    if os.path.exists('post.json'):
        with open('post.json', 'r') as file:
            post = json.load(file)

    photo = f"comment_images/{post['photo_filename']}"
    # Retrieve data from the posts table
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts')
    rows = cursor.fetchall()
    conn.close()

    return render_template('posts.html', post=post, rows=rows, photo=photo)

@app.route('/posts_ajax')
def posts_ajax():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)
    
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch the latest rows from the posts table based on page and size
    cursor.execute('SELECT * FROM posts ORDER BY timestamp DESC LIMIT ? OFFSET ?',
                   (size, (page - 1) * size))
    rows = cursor.fetchall()

    # Count the total number of rows in the table for pagination
    cursor.execute('SELECT COUNT(*) FROM posts')
    total_rows = cursor.fetchone()[0]
    
    conn.close()

    return jsonify({
        'table': render_template('posts_table.html', rows=rows),
        'pagination': render_template('pagination.html', page=page, size=size, total_rows=total_rows)
    })




@app.route('/submit_post', methods=['POST'])
def submit_post():
    comment = request.form.get('comment')
    photo = request.files.get('photo')

    # Save comment to JSON file
    post_data = {
        'comment': comment,
        'photo_filename': None
    }

    if photo:
        # Save uploaded photo to the comment_images folder
        filename = photo.filename
        photo.save(os.path.join('static/comment_images', filename))
        post_data['photo_filename'] = filename

    with open('post.json', 'w') as file:
        json.dump(post_data, file)

    # Redirect back to the "Posts" page
    return redirect('/posts')
@app.route('/run_comment_script', methods=['POST'])
def run_comment_script():
    subprocess.run(['python', 'comment.py'])
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
