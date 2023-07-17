from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import configparser
import os

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
    return render_template('home.html')

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

if __name__ == '__main__':
    app.run(debug=True)
