import os

from dotenv import load_dotenv
from flask import Flask, send_from_directory

import s3

load_dotenv()
s3.config()
app = Flask(__name__)


@app.route('/static/theme/<file_name>')
def theme(file_name: str):
    
    s3.prepare_static_files()
    
    client = os.getenv('CLIENT')
    return send_from_directory('static', f'{client}/{file_name}')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=False)
