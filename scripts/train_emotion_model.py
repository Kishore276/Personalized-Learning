import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Create the model architecture
def create_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)),
        tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        tf.keras.layers.Dropout(0.25),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1024, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(7, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Create a simple training dataset with random data (replace with real data)
def create_dummy_dataset():
    X = np.random.random((100, 48, 48, 1))
    y = tf.keras.utils.to_categorical(np.random.randint(0, 7, 100), 7)
    return X, y

def train_model():
    model = create_model()
    
    # Create dummy dataset
    X_train, y_train = create_dummy_dataset()
    
    # Create data generator for data augmentation
    datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    # Train the model
    model.fit(
        datagen.flow(X_train, y_train, batch_size=32),
        epochs=10,
        steps_per_epoch=len(X_train) // 32
    )
    
    # Save the entire model instead of just weights
    model.save('emotion_model.h5')
    print("Model saved successfully!")

if __name__ == "__main__":
    train_model()
