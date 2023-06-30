from flask import Flask, render_template, request, redirect, url_for
import subprocess
import json

import sqlite3
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        data = {
            'api_key': request.form['api_key'],
            'groups': request.form['groups'],
            'comment': request.form['comment'],
            'total_comment': int(request.form['total_comment'])
        }
        image = request.files['image']
        if image:
            # Save the image file to the server
            image.save('static/imgs/' + image.filename)
            data['image'] = 'static/imgs/' + image.filename

        cookie = request.files['cookie']
        if cookie:
            # Save the cookie file to the server
            cookie.save('static/cookies/' + cookie.filename)
            data['cookie'] = 'static/cookies/' + cookie.filename

        # Save the form data to a JSON file
        with open('config.json', 'w') as json_file:
            json.dump(data, json_file)

    else:
        # Load the form data from the JSON file
        try:
            with open('config.json', 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = None

    return render_template('config.html', data=data)


@app.route('/spammer', methods=['GET', 'POST'])
def spammer():
    if request.method == 'POST':
        if 'run_tool' in request.form:
            # Execute the tool.py Python file
            subprocess.Popen(['python', 'main.py'])

            # Alternatively, you can use the following command if you want to run the file as a background process:
            # subprocess.Popen(['python', 'tool.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            # Redirect to the "Spammer" page or another page as desired
            return redirect(url_for('spammer'))

    return render_template('spammer.html')


@app.route('/fetch_data')
def fetch_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Execute a query to fetch the data
    cursor.execute("SELECT timestamp, post_id FROM records")

    # Fetch all the rows
    rows = cursor.fetchall()

    # Create a list of dictionaries containing the data
    data = [{'timestamp': row[0], 'post_id': row[1]} for row in rows]

    # Close the database connection
    conn.close()

    # Return the data as a JSON response
    return jsonify({'data': data})

if __name__ == '__main__':
    app.run(debug=True)
