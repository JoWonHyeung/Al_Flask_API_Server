import base64
from typing import io

from flask import Flask, request, render_template
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #response시, 한글 깨짐 이슈 해결
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

label = {0:'고추탄저병',
         1:'고추흰가루병',
         2:'무검은무늬병',
         3:'무노균병',
         4:'배추검은썩음병',
         5:'배추노균병',
         6:'정상_고추',
         7:'정상_무',
         8:'정상_배추',
         9:'정상_콩',
         10:'정상_파',
         11:'콩불마름병',
         12:'콩점무늬병',
         13:'파검은무늬병',
         14:'파노균병',
         15:'파녹병'}

@app.route('/')
@app.route("/test")
def index():
    return "server test"

# 데이터 예측 처리
@app.route('/prediction')
def local_predict_test():
     model = load_model("/home/ubuntu/Al_Flask_API_Server/model/xception_epoch10_pretrained.h5")

     image = Image.open("/home/ubuntu/Al_Flask_API_Server/image/test_img.jpg")
     processed_image = preprocess_image(image, target_size=(224, 224))

     prediction = model.predict(processed_image).tolist()

     response = {
             'result': {
                 'crop_name': label[np.argmax(prediction[0])],                                  
                 'percentage' : max(prediction[0])
             }
         }
     return flask.jsonify(response)

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = image / 255
    image = np.expand_dims(image, axis=0)
    return image

# @app.route("/predict", methods=["POST"])
# def predict():
#     message = request.get_json(force=True)
#     encoded = message['image']
#     decoded = base64.b64decode(encoded)
#     image = Image.open(io.BytesIO(decoded))
#     processed_image = preprocess_image(image, target_size=(224, 224))
#
#     prediction = model.predict(processed_image).tolist()
#
#     response = {
#         'prediction': {
#             'dog': prediction[0][0],
#             'cat': prediction[0][1]
#         }
#     }
#     return jsonify(response)

if __name__ == '__main__':

    # Flask 서비스 스타트
    app.run(host='0.0.0.0',port=5000)
