# Load the trained model's structure and weights from json and h5 file



# Import the environments 
from keras.models import model_from_json
import tensorflow as tf


# We will run this function when the website is loading
def init():
    # open the structure
    json_file = open('modelStructure.json','r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # open the weights
    model.load_weights("modelWeights.h5")
    # compile and evaluate loaded model
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    model._make_predict_function()
    graph = tf.compat.v1.get_default_graph()


    return model,graph
