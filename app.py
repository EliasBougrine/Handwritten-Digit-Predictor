# Main file defining the different routes



# Import the environments
from flask import Flask, render_template, request
import uuid
import base64
import json
import os
from New_Prediction import prediction
from load import init
import tensorflow.compat.v1 as tf



# Create the application
app = Flask(__name__)



# Load the graph and model
global model, graph
model, graph = init()
tf.disable_v2_behavior()



# Define the routes

# Home
@app.route("/")
def home():
	return render_template('home.html', title='Home')

# Drawing Predictor
@app.route("/DrawingPredictor")
def drawing_predictor():
    return render_template('drawing_predictor.html', title='Drawing Predictor')

# Project Description
@app.route("/ProjectDescription")
def project_description():
    return render_template('project_description.html', title='Project Description')

# About Me
@app.route("/AboutMe")
def about_me():
    return render_template('about_me.html', title='About Me')

# Hidden function running to make the prediction
@app.route("/hidden", methods=["GET", "POST"])
def hidden():
    if request.method == 'POST':
        # Get the encoded image and decode it
        image_b64 = request.values['imageBase64']
        image_encoded = image_b64.split(',')[1]
        image = base64.decodebytes(image_encoded.encode('utf-8'))
        # Create a file name
        filename = 'digit' +  '__' + str(uuid.uuid1()) + '.png'
        # Save the image in a temporary file
        with open('tmp/' + filename, 'wb') as f:
            f.write(image)
        # Make the prediction
        pred = prediction().final_function(filename, model, graph)
        # Delete the image
        os.remove('tmp/' + filename)
    return json.dumps(pred)



# Run the app
if __name__ == '__main__':
	app.run(debug=False)