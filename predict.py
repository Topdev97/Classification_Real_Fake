import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image


def predict_image(img_path, image_type):
    # Load the model
    model_path = f'models/{image_type}_model.h5'
    model = tf.keras.models.load_model(model_path)

    # Preprocess the image
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale the image

    # Make a prediction
    prediction = model.predict(img_array)[0][0]
    if prediction > 0.5:
        return f"The image is classified as Real."
    else:
        return f"The image is classified as Fake."
