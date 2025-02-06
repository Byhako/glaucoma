import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image

from PIL import Image
import io
import numpy as np

def predict(image, model):
    # Cargar y procesar la imagen
    image = image.resize((224, 224))
    image_array = np.array(image)

    # Asegurarse de que la imagen tenga 3 canales (RGB)
    if image_array.ndim == 2:  # Imagen en escala de grises
        image_array = np.stack((image_array,) * 3, axis=-1)
    elif image_array.shape[2] == 1:  # Imagen con un solo canal
        image_array = np.concatenate([image_array] * 3, axis=-1)

    # Asegurarse de que la imagen tenga la forma correcta (1, 224, 224, 3)
    assert image_array.shape == (224, 224, 3)
    image_array = np.expand_dims(image_array, axis=0)

    image_array = image_array / 255.0 # Normalizar la imagen

    # Realizar la predicción
    prediction = model.predict(image_array)
    predicted_class = np.argmax(prediction, axis=1)

    # Mapear las clases predichas
    class_names = ['No', 'Si']
    predicted_label = class_names[predicted_class[0]]
    value_confidence = prediction[0][predicted_class[0]]

    return [predicted_label, value_confidence]
