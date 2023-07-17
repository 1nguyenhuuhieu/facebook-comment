import sqlite3
from datetime import datetime
from selenium.webdriver.common.by import By
from login import *
from urllib.parse import parse_qs, urlparse
DATABASE = 'facebook_auto_comment.db'


def save_post(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the posts table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            post_id TEXT,
            is_commented BOOLEAN DEFAULT 0,
            can_comment BOOLEAN DEFAULT 1
        )
    ''')

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO posts (timestamp, post_id) VALUES (?, ?)',
                   (timestamp, post_id))
    conn.commit()
    conn.close()

def get_source_posts():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM source_posts')
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_post_id(url):
    query_string = urlparse(url).query
    query_params = parse_qs(query_string)
    sid = query_params.get('sid')
    if sid:
        sid = sid[0]
        return sid
    else:
        return None

def is_post_id_exists(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT EXISTS(SELECT 1 FROM posts WHERE post_id = ? LIMIT 1)', (post_id,))
    result = cursor.fetchone()[0]
    conn.close()
    return bool(result)

def save_post_id(source_url):
    driver = login()
    time.sleep(5)
    driver.get(source_url)
    time.sleep(5)
    
    all_links = driver.find_elements(By.TAG_NAME, 'a')
    for link in all_links:
        if link.get_attribute('data-sigil') == 'share-popup':
            url = link.get_attribute('href')
            post_id = get_post_id(url)

            if post_id:
                exists = is_post_id_exists(post_id)
                if not exists:
                    save_post(post_id)
     
source_posts = get_source_posts()
for source in source_posts:
    source_url = source['url']
    save_post_id(source_url)
    time.sleep(5)

