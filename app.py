from flask import Flask, request, render_template, make_response
import cv2
import numpy as np
import mysql.connector

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
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    if cv2.__version__.startswith('3'):
        _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    elif cv2.__version__.startswith('4'):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    else:
        raise RuntimeError("Unsupported OpenCV version")

    img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    _, img_encoded = cv2.imencode('.jpg', img)
    response = make_response(img_encoded.tobytes())
    response.headers.set('Content-Type', 'image/jpeg')

    # Add information about the file, date, and user's IP address to the database
    conn = mysql.connector.connect(host='172.16.1.50', user='hehe', passwd='hehe', db='baza')
    cur = conn.cursor()
    cur.execute("INSERT INTO images (name, date, ip_address) VALUES (%s, NOW(), %s)", (filename, request.remote_addr))
    conn.commit()
    cur.close()
    conn.close()

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')

