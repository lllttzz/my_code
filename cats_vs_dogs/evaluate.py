from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import input_data
import model

def get_one_image(train):
   '''Randomly pick one image from training data
   Return: ndarray
   '''
   n = len(train)
   ind = np.random.randint(0, n)
   img_dir = train[ind]

   image = Image.open(img_dir)
   plt.imshow(image)
   plt.show()
   image = image.resize([208, 208])
   image = np.array(image)
   return image




def evaluate_one_image():
   '''Test one image against the saved models and parameters
   '''

   train_dir = './train/'
   train, train_label = input_data.get_files(train_dir)
#   train = input_data.get_test_file(train_dir)
   image_array = get_one_image(train) # 获取随机一张图片的array

   with tf.Graph().as_default():
       BATCH_SIZE = 1
       N_CLASSES = 2
       image = tf.cast(image_array, tf.float32) # 图片的array转化为tf.float32
       image = tf.image.per_image_standardization(image) # 标准化处理
       image = tf.reshape(image, [1, 208, 208, 3])
       logit = model.inference(image, BATCH_SIZE, N_CLASSES,train=False) # 图片输入model测试，返回猫和狗的"概率"(1.4,2)

       logit = tf.nn.softmax(logit) # 经过softmax转化为概率

    #    x = tf.placeholder(tf.float32, shape=[208, 208, 3])

       logs_train_dir = './save_model/'

       saver = tf.train.Saver()

       with tf.Session() as sess:

           print("Reading checkpoints...")
           ckpt = tf.train.get_checkpoint_state(logs_train_dir)
           if ckpt and ckpt.model_checkpoint_path:
               # ckpt.model_checkpoint_path:表示模型存储的位置
               global_step = ckpt.model_checkpoint_path.split('/')[-1].split('-')[-1] # .../model.ckpt-14999
               saver.restore(sess, ckpt.model_checkpoint_path)
               print('Loading success, global_step is %s' % global_step)
           else:
               print('No checkpoint file found')

           prediction = sess.run(logit)
           max_index = np.argmax(prediction)
           if max_index==0:
               print('This is a cat with possibility %.6f' %prediction[:, 0])
           else:
               print('This is a dog with possibility %.6f' %prediction[:, 1])

evaluate_one_image()
