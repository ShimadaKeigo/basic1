import json
import random
import time
from datetime import datetime

from flask import Flask, Response, render_template, stream_with_context

import sqlite3

import pandas as pd

application = Flask(__name__)
random.seed()  # Initialize the random number generator


@application.route('/')
def index():
    return render_template('index.html')


@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        dbname = 'data.db'

        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        select_sql = 'SELECT * FROM record'
        '''while True:
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': random.random() * 100, 'value2': random.random() * 100, 'value3': random.random() * 100})
            yield f"data:{json_data}\n\n"
            time.sleep(1)'''
        for row in cur.execute(select_sql):
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'ax': row[0], 'ay': row[1], 'az': row[2], 'gx': row[3], 'gy': row[4], 'gz': row[5], 'magx': row[6], 'magy': row[7], 'magz': row[8]})
            yield f"data:{json_data}\n\n"
            time.sleep(1)
        cur.close()
        conn.close()

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == '__main__':
    application.run(debug=True, threaded=True)