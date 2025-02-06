import tensorflow as tf
from tensorflow import keras
import os

def load_models():
    model_paths = {
        'mobilenet': 'models/mobilenet.h5',
        'densenet': 'models/densenet201.h5',
        'resnet50': 'models/resnet50v2.h5',
        'resnet152': 'models/resnet152v2.h5'
    }
    
    models = {}
    
    for name, path in model_paths.items():
        if os.path.exists(path):
            models[name] = keras.models.load_model(path)
        else:
            print(f"Error: El archivo del modelo '{name}' no se encuentra en la ruta: {path}")
    
    return models

models = load_models()

print('Load models success')
