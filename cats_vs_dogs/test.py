import tensorflow as tf
import numpy as np
from PIL import Image
import model
import os
file_dir = './test2/'
logs_train_dir = './save_model'

def get_a_picture_evaluate():
    with tf.Graph().as_default() as g:
        x = tf.placeholder(tf.float32,shape=[208,208,3])
        name = []
        label = []
        for file in os.listdir(file_dir):
            # n = file.split(sep='.')
            image_array= Image.open(file_dir+file)
            image_array = image_array.resize([208,208])
            image_array = np.array(image_array)

            image = tf.cast(image_array, tf.float32)
            image = tf.image.per_image_standardization(image) # 标准化处理
            image = tf.reshape(image, [1, 208, 208, 3])

            logit = model.inference(image, 1, 2)
            logit = tf.nn.softmax(logit)

        saver = tf.train.Saver()

    with tf.Session(graph=g) as sess:

        ckpt = tf.train.get_checkpoint_state(logs_train_dir)
        saver.restore(sess, ckpt.model_checkpoint_path)
        logit = model.inference(image, 1, 2)

        logit = tf.nn.softmax(logit)
        prediction = sess.run(logit, feed_dict={x: image_array})
        max_index = np.argmax(prediction)

        label.append(max_index)
        name.append(n[0])
        label1 = [str(k) for k in label]
get_a_picture_evaluate()
