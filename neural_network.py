# all neural network libraries
import tensorflow as tf
import tensorflow_datasets as tfds
from keras.layers import Dense, GlobalAveragePooling2D, Dropout

# photo size for the best grid performance
SIZE = 224

# Avoiding downloading additional software represented by CUDO
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def resize_image(img, label):
    """
    function to change the training sample to a resolution of 224 by 224
    (at these values this neural network shows the best accuracy), and
    the color gradations were normalized by dividing by 255 so that
    the neural network sees colors from 0 to 1 inclusive
    """

    img = tf.cast(img, tf.float32)
    img = tf.image.resize(img, (SIZE, SIZE))
    img = img / 255.0
    return img, label


def main():
    """
    convolutional neural network for classifying cats/dogs
    """

    # download dataset from Microsoft named cats_vs_dogs
    train, _ = tfds.load('cats_vs_dogs', split = ['train[:100%]'], with_info = True, as_supervised = True)

    train_resized = train[0].map(resize_image)

    # break the data into batches
    train_batches = train_resized.shuffle(1000).batch(16)

    base_layers = tf.keras.applications.MobileNetV2(input_shape = (SIZE, SIZE, 3), include_top = False)
    base_layers.trainable = False

    model = tf.keras.Sequential([
        base_layers,
        GlobalAveragePooling2D(),
        Dropout(0.2),
        Dense(1)
    ])

    model.compile(optimizer = 'adam',
                  loss = tf.keras.losses.BinaryCrossentropy(
                      from_logits = True), metrics = ['accuracy'])

    model.fit(train_batches, epochs = 3)

    model.save('model_load')


if __name__ == '__main__':
    main()
