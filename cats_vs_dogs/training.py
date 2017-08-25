import os
import numpy as np
import tensorflow as tf
import input_data
import model

N_CLASSES = 2 # 分两类
IMG_W = 208  # resize the image, if the input image is too large, training will be very slow.
IMG_H = 208
BATCH_SIZE = 16
CAPACITY = 2000
MAX_STEP = 15000 # with current parameters, it is suggested to use MAX_STEP>10k
learning_rate = 0.0001 # with current parameters, it is suggested to use learning rate<0.0001

def run_training():

    train_dir = './train/' # 加载数据训练
    logs_train_dir = './save_model/' # 储存训练好的位置

    train, train_label = input_data.get_files(train_dir)

    train_batch, train_label_batch = input_data.get_batch(train,
                                                          train_label,
                                                          IMG_W,
                                                          IMG_H,
                                                          BATCH_SIZE,
                                                          CAPACITY)
    train_logits = model.inference(train_batch, BATCH_SIZE, N_CLASSES) # forward pass
    train_loss = model.losses(train_logits, train_label_batch) # 设置损失函数
    train_op = model.trainning(train_loss, learning_rate) # training
    train__acc = model.evaluation(train_logits, train_label_batch) # 验证正确率

    summary_op = tf.summary.merge_all() # 定义合并变量操作，一次性生成所有摘要数据
    sess = tf.Session() # 初始化会话
    train_writer = tf.summary.FileWriter(logs_train_dir, sess.graph) # TensorBoard的记录
    saver = tf.train.Saver() # 储存模型

    sess.run(tf.global_variables_initializer()) # 所有变量初始化
    coord = tf.train.Coordinator() # 多线程
    threads = tf.train.start_queue_runners(sess=sess, coord=coord)

    try:
        for step in np.arange(MAX_STEP):
            if coord.should_stop():
                break
            _, tra_loss, tra_acc = sess.run([train_op, train_loss, train__acc])

            if step % 50 == 0:
                print('Step %d, train loss = %.2f, train accuracy = %.2f%%' %(step, tra_loss, tra_acc*100.0))
                summary_str = sess.run(summary_op)
                train_writer.add_summary(summary_str, step)

            if step % 2000 == 0 or (step + 1) == MAX_STEP:
                checkpoint_path = os.path.join(logs_train_dir, 'model.ckpt')
                saver.save(sess, checkpoint_path, global_step=step)

    except tf.errors.OutOfRangeError:
        print('Done training -- epoch limit reached')
    finally:
        coord.request_stop()

    coord.join(threads)
    sess.close()



run_training()
