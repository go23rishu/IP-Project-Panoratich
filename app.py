from flask import Flask, render_template, flash, request, redirect
from werkzeug.utils import secure_filename
import os
#import magic
import urllib.request
# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os
app = Flask(__name__)
 
UPLOAD_FOLDER = "/home/rishu/Desktop/IP Project/gg/dist/static/styles"
 
app.secret_key = "Cairocoders-Ednalan"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
 return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/')
def upload_form():
 return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
    files = request.files.getlist('files[]')
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    flash('File(s) successfully uploaded')
    print("[INFO] loading images...")
    images=[]
    for imagePath in files:
        print(type(imagePath))
        print(imagePath)
    for imagePath in files:
        image= cv2.imread(imagePath)
        cv2.imshow("Image", image)
        # image=cv2.resize(image, (64,64))
        images.append(image)
    print("[INFO] stitching images...")
    stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
    (status, stitched) = stitcher.stitch(images)
    if status == 0:
        # cv2.imwrite(args["output"], stitched)
        cv2.imshow("Stitched", stitched)
        cv2.waitKey(0)
    else:
        print("[INFO] image stitching failed ({})".format(status))
    return redirect('/')
   
if __name__ == '__main__':
 app.run(debug=True)