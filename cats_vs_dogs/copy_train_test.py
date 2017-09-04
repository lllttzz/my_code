import tensorflow as tf
import numpy as np
import input_data
import model
import os
import csv

train_dir = './test1/' # 加载数据训练
logs_train_dir = './save_model/'
N_CLASSES = 2 # 分两类
IMG_W = 208  # resize the image, if the input image is too large, training will be very slow.
IMG_H = 208
BATCH_SIZE = 1
CAPACITY = 2000

def get_files(file_dir):
    bianhao = []
    picture = []
    a = os.listdir(file_dir)
    a.sort(key= lambda x:int(x[:-4]))

    for file in a:
        name = file.split(sep='.')
        bianhao.append(name[0])
        picture.append(file_dir+file)
        print(file)

    picture_list = np.array([picture,bianhao])
    picture_list = picture_list.transpose()
    image_list = list(picture_list[:,0])
    bianhao_list = list(picture_list[:,1])
    bianhao_list = [int(i) for i in bianhao]

    return image_list,bianhao_list

def get_all_picture_evaluate():

    label_out=[]

    train, test_step = get_files(train_dir)
    train_batch, train_label_batch = input_data.get_batch(train,
                                                        test_step,
                                                        IMG_W,
                                                        IMG_H,
                                                        BATCH_SIZE,
                                                        CAPACITY)
    logit = model.inference(train_batch, BATCH_SIZE, N_CLASSES)
    logit = tf.nn.softmax(logit)
    sess = tf.Session()
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)
    csvfile = open('csv.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['name','label'])

    try:
        ckpt = tf.train.get_checkpoint_state(logs_train_dir)
        saver.restore(sess, ckpt.model_checkpoint_path)

        for step in test_step:
            if coord.should_stop():
                break
            prediction = sess.run(logit)
            max_index = np.argmax(prediction)
            label_out.append(max_index)
            if step%1000 == 0:
                print(step)
        for (i,j) in zip(test_step,label_out):
            writer.writerow([i,j])

    except tf.errors.OutOfRangeError:
        print('Done training -- epoch limit reached')
    finally:
        coord.request_stop()

    coord.join(threads)
    csvfile.close()
    sess.close()

get_all_picture_evaluate()
