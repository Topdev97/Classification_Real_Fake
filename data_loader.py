import os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def preprocess_data(data_dir, img_height, img_width):
    """
    Load and preprocess data from the specified directory structure.
    """
    categories = ["car", "driver_license"]
    labels = {"real": 0, "fake": 1}
    
    image_paths = []
    image_labels = []

    # Iterate through categories and real/fake folders
    for category in categories:
        category_path = os.path.join(data_dir, category)
        for label in labels.keys():
            label_path = os.path.join(category_path, label)
            for img_name in os.listdir(label_path):
                img_path = os.path.join(label_path, img_name)
                if img_path.endswith((".jpg", ".png", ".jpeg")):  # Ensure it's an image file
                    image_paths.append(img_path)
                    image_labels.append(labels[label])
    
    images = []
    for img_path in image_paths:
        # Load and resize image
        img = load_img(img_path, target_size=(img_height, img_width))
        img_array = img_to_array(img)
        images.append(img_array)
    
    # Normalize images
    images = np.array(images) / 255.0
    labels = np.array(image_labels)

    return images, labels
