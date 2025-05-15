# 该文件使用TensorFlow和TensorFlow Datasets对图像数据集进行预处理和增强。
# 定义了图像转换和增强函数，划分不同批次用于训练和验证。

import tensorflow as tf
import numpy as np
import tensorflow_datasets as tfds
import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
# %matplotlib inline

train_dataset=r'F:\study\project\face\myface\images\capture_tian'

def convert(image, label):
    image = tf.image.convert_image_dtype(image, tf.float32)
    return image, label


def augment(image, label):
    image, label = convert(image, label)
    # image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize_with_crop_or_pad(image, 34, 34)  # 四周各加3像素
    image = tf.image.random_crop(image, size=[28, 28, 1])  # 随机裁剪成28*28大小
    image = tf.image.random_brightness(image, max_delta=0.5)  # 随机增加亮度
    return image, label


batch_size = 64
num_examples = 2048  # 使用较少数据量，以展现出过拟合

augmented_train_batches = (train_dataset
                           .take(num_examples)
                           .cache()
                           .shuffle(num_train_examples // 4)
                           .map(augment, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                           .batch(batch_size)
                           .prefetch(tf.data.experimental.AUTOTUNE))

non_augmented_train_batches = (train_dataset
                               .take(num_examples)
                               .cache()
                               .shuffle(num_train_examples // 4)
                               .map(convert, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                               .batch(batch_size)
                               .prefetch(tf.data.experimental.AUTOTUNE))

validation_batches = (test_dataset
                      .map(convert, num_parallel_calls=tf.data.experimental.AUTOTUNE)
                      .batch(2 * batch_size))