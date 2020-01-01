# This file allows us to transform an image and make a prediction



# Import the environments
from PIL import Image
import numpy as np



# Create the class
class prediction():
    
    
    # This function imports a 420 x 420 px image and returns an array of
    # a 28 x 28 px image after centering and resizing it.
    def transform_image(self, filename):
        img = Image.open('tmp/' + filename)
        bbox = Image.eval(img, lambda px: 255-px).getbbox()
        if bbox == None:
            return None
        widthlen = bbox[2] - bbox[0]
        heightlen = bbox[3] - bbox[1]
        if heightlen > widthlen:
            widthlen = int(20.0 * widthlen/heightlen)
            heightlen = 20
        else:
            heightlen = int(20.0 * widthlen/heightlen)
            widthlen = 20
        hstart = int((28 - heightlen) / 2)
        wstart = int((28 - widthlen) / 2)
        img_temp = img.crop(bbox).resize((widthlen, heightlen), Image.NEAREST)
        new_img = Image.new('L', (28,28), 255)
        new_img.paste(img_temp, (wstart, hstart))
        imgdata = list(new_img.getdata())
        self.im = np.array([(255.0 - x) / 255.0 for x in imgdata])
        return self.im

    
    # This function transforms the type of the element of the previous array
    # and reshape it in order to be used by the prediction model.
    def transform(self):
        self.im = self.im.astype('float32')
        self.im = self.im.reshape(1, 1, 28, 28)


    # This function takes a model and a graph as inputs. It will use them to 
    # the prediction of the previous array
    def prediction(self, model, graph):
        with graph.as_default():
            out = model.predict(self.im)
        p = np.argmax(out)
        return p
        
    
    # This is the final function that calls all of the previous one.
    # If the image is empty, we don't make a prediction and return a different message.
    def final_function(self, filename, model, graph):
        t = self.transform_image(filename)
        if t is None:
            return {'result': "You didn't draw anything!  :)"}
        else:
            self.transform()
            pred = self.prediction(model, graph)
            return {'result': str(pred)}
    
    