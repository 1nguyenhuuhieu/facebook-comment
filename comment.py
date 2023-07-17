import json
import sqlite3
from login import *
from selenium.webdriver.common.by import By
import os

DATABASE = 'facebook_auto_comment.db'

class Post:
    def __init__(self, comment=None, photo_filename=None):
        self.comment = comment
        self.photo_filename = photo_filename

    @classmethod
    def from_json(cls, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
            return cls(data.get('comment'), data.get('photo_filename'))
        

def get_posts():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM posts WHERE is_commented = 0 AND can_comment = 1')
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_post_is_commented(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE posts SET is_commented = 1 WHERE post_id = ?', (post_id,))
    conn.commit()
    conn.close()




if __name__ == "__main__":

    post_comment = Post.from_json('post.json')

    image_directory = 'static\\comment_images'
    image_filename = post_comment.photo_filename
    image_file_path = os.path.join(os.getcwd(), image_directory, image_filename)

    posts = get_posts()

    # Iterate over the retrieved posts
    for post in posts:

        try:
            post_id = str(post['post_id'])
            post_url = r'https://www.facebook.com/' + post_id
            driver.get(post_url)
            time.sleep(5)
            print(post_url)
            textarea = driver.find_element(By.ID, 'composerInput')
            textarea.send_keys(post_comment.comment)
            try:
                image_input = driver.find_element(By.XPATH, "//input[@type='file']")
                image_input.send_keys(image_file_path)
                time.sleep(10)
            except:
                pass
            time.sleep(2)
            submit_btn = driver.find_element(By.NAME, "submit")
            submit_btn.click()
            time.sleep(3)
            update_post_is_commented(post_id)
    
        except:
            try:
                driver.quit()
            except:
                pass
            driver = login()

        time.sleep(5)