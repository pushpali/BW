# Program to Upload Color Image and convert into Black & White image
import os
from flask import  Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2#converting uploaded images in static folder to array and then changing the value so that it becomes black and white
import numpy as np

app = Flask(__name__)

# Open and redirect to default upload webpage
@app.route('/')#to run the function in home page
def load_form():
    return render_template('upload.html')# to show the output in html page


# Function to upload image and redirect to new webpage
@app.route('/gray', methods=['POST'])
def upload_image():
    file = request.files['file']
    filename = secure_filename(file.filename)

    file_data = make_grayscale(file.read())#passing image file to make_grayscale() where the image is converted into black and white and then stored in file_data
    #to store BW image we need to open the place where the coloured image is stored and then put file_data variable over there
    with open(os.path.join('static/', filename),
              'wb') as f:#wb-write binary
        f.write(file_data)

    display_message = 'Image successfully uploaded and displayed below'
    return render_template('upload.html', filename=filename, message = display_message)#only upload image and show msg



def make_grayscale(input_image):

    image_array = np.fromstring(input_image, dtype='uint8')#to convert coloured image into pixel single-line array whose datatype is uint8
    print('Image Array:',image_array)

    # decode the array into an image
    decode_array_to_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)#converts single array into matrix format  i.e proper RGB format array with 3 columns
    print('Decode values of Image:', decode_array_to_img)

    # Make grayscale
    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)#converts image to BW
    status, output_image = cv2.imencode('.PNG', converted_gray_img)#converts image to original format
    print('Status:',status)

    return output_image#returned to file_data variable


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename))#upload image from static folder to the same page



if __name__ == "__main__":
    app.run()


