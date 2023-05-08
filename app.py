import os
from flask import Flask, request, render_template, make_response
import cv2
import numpy as np
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    img = request.files['image']
    filename = img.filename
    img.save('uploads/' + filename)
    img = cv2.imread('uploads/' + filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert the image to black and white
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    _, img_encoded = cv2.imencode('.jpg', thresh)
    response = make_response(img_encoded.tobytes())
    response.headers.set('Content-Type', 'image/jpeg')

    # Add information about the file, date, and user's IP address to the database
    conn = mysql.connector.connect(host=os.getenv('MYSQL_HOST'), user=os.getenv('MYSQL_USER'), passwd=os.getenv('MYSQL_PASSWORD'), db=os.getenv('MYSQL_DATABASE'))
    cur = conn.cursor()
    cur.execute("INSERT INTO images (name, date, ip_address) VALUES (%s, NOW(), %s)", (filename, request.remote_addr))
    conn.commit()
    cur.close()
    conn.close()

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
