import base64
import io
import time
import datetime
from PIL import Image
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import keras
import tensorflow
from datetime import timedelta
import numpy as np



def infer(b64_image_data):
    # load model for use
    try:
        print("Loading model")
        model = keras.models.load_model('AI_model/biio.keras')
        print("Model Loaded")
    except Exception as e:
        print(f"Error loading model: {e}")
    clas_name = ["HDPE", "PE", "PET", "PP", "Paper", "Metal", "Non-Recyclable", "Tissue"]
    file_data = base64.b64decode(b64_image_data)
    file_io = io.BytesIO(file_data)
    image = Image.open(file_io)
    image = image.resize((224, 224))

    img_arr = keras.utils.array_to_img(image)
    img_bat = tensorflow.expand_dims(img_arr,0)



    start_time = time.perf_counter()  # High-precision timer
    predict = model.predict(img_bat)
    end_time = time.perf_counter()

    processing_time = timedelta(seconds= (end_time - start_time))
    score = tensorflow.nn.softmax(predict)
    # print('image is {} with acc of {:0.2f}'.format(clas_name[np.argmax(score)],np.max(score)*100))

    # print(predict)
    detected_type = clas_name[np.argmax(score)]
    # is accuracy the same as confidence?
    confidence = np.max(score)*100
    return {
        'detected_type': detected_type,
        'confidence': confidence,
        'processing_time': processing_time
        }
