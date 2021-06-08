from io import BytesIO
from flask import Flask, render_template, request
from scipy.misc import imsave, imread, imresize
from playsound import playsound
import base64, json
import numpy as np
from PIL import Image
from datetime import datetime
from keras.models import load_model

app = Flask(__name__)
conv = load_model("./models/conv_95.5.h5")
conv._make_predict_function()
FRUITS = {0: "Apple", 1: "Banana", 2: "Grapes", 3: "Pineapple", 4:"Eye", 5:"Face", 6:"Star", 7:"Bowtie", 8:"House", 9:"Cloud",}


@app.route('/')
def index():

    return render_template('index.html')

# recognition digit
@app.route('/Recognition', methods=['GET', 'POST'])
def ExecPy():
    retJson = {"predict_fruit" :"Err"}
    if request.method == 'POST':
        # request.body
        postImg = BytesIO(base64.urlsafe_b64decode(request.form['img']))
        #Create a BytesIO object.
        #if you want to manipulate binary data, you need to use BytesIO
        #base64.urlsafe_b64decode() method, we are able to get the decoded string which can be in binary form by using this method.
        postImg = Image.open(postImg)
        postImg.save("./temp.png")
        x = imread('temp.png', mode='L')#L= 8-bit pixels, black and white
        x = imresize(x, (28, 28))

        model = conv
        x = np.expand_dims(x, axis=0)
        x = np.reshape(x, (28, 28, 1))
         # invert the colors because the original trained files are white on black
        x = np.invert(x)
         # brighten the image by 60%
        for i in range(len(x)):
             for j in range(len(x)):
                 if x[i][j] > 50:
                     x[i][j] = min(255, x[i][j] + x[i][j] * 0.60)

        # normalize the values between -1 and 1
        x = np.interp(x, [0, 255], [-1, 1])
        val = model.predict(np.array([x]))
        pred = FRUITS[np.argmax(val)]#pred variable has drawing name like 'apple'
        retJson["predict_fruit"]=pred#retjson is a python dictionary. It has value 'apple' on key 'predict_fruit'


        from gtts import gTTS
        import os
        import os.path
        from os import path
        if path.exists(pred+'.mp3'):
            playsound(pred+'.mp3')
        else:
            mytext='it is a'+pred
            language = 'en'
            myobj = gTTS(text=mytext,lang=language)
            myobj.save(pred+'.mp3')
            playsound(pred+'.mp3')


    return json.dumps(retJson)#python dictionary is converted into json string and send to script.js
    #JSON (JavaScript Object Notation) is a popular data format used for representing structured data.
    #It's common to transmit and receive data between a server and web application in JSON format


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
