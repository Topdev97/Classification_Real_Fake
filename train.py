import tensorflow as tf
from tensorflow.keras import layers, models
import os
import shutil


def load_data(image_type):
    base_dir = f'data/{image_type}'
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1.0/255,
        validation_split=0.2
    )

    train_generator = datagen.flow_from_directory(
        base_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='binary',
        subset='training'
    )

    validation_generator = datagen.flow_from_directory(
        base_dir,
        target_size=(150, 150),
        batch_size=32,
        class_mode='binary',
        subset='validation'
    )

    return train_generator, validation_generator


def train_model(image_type):
    train_generator, validation_generator = load_data(image_type)

    # Build a CNN model
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    # Train the model
    model.fit(
        train_generator,
        epochs=10,
        validation_data=validation_generator
    )

    # Save the trained model
    model.save(f'models/{image_type}_model.h5')
    print(f"{image_type} model trained and saved successfully!")


if __name__ == "__main__":
    image_type = input("Enter image type (cars/driver_license): ")
    train_model(image_type)
