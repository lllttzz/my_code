import tensorflow as tf
import numpy as np
import os

train_dir = './train/' # 数据存放位置

def get_files(file_dir):
    cats = []
    label_cats = []
    dogs = []
    label_dogs = []
    for file in os.listdir(file_dir): # 返回指定的文件夹包含的文件或文件夹的名字的列表
        name = file.split(sep='.') # 通过'.'来分割
        if name[0]=='cat':
            cats.append(file_dir + file)
            label_cats.append(0) # 猫的label为0
        else:
            dogs.append(file_dir + file)
            label_dogs.append(1) # 狗的label为1
    print('There are %d cats\nThere are %d dogs' %(len(cats), len(dogs))) # 输出猫和狗的个数

    image_list = np.hstack((cats, dogs)) # 把猫和狗的图片全部放在一个list里
    label_list = np.hstack((label_cats, label_dogs)) # 把猫和狗的label全部放在一个list里

    temp = np.array([image_list, label_list]) # 组成一个2维数组（2行n列）
    temp = temp.transpose()  # 转置=>（n行2列）
    np.random.shuffle(temp) # 随机打乱顺序

    image_list = list(temp[:, 0]) # 打乱后的图片
    label_list = list(temp[:, 1]) # 打乱后的label
    label_list = [int(i) for i in label_list] # 把label转换为int型


    return image_list, label_list


#%%

def get_batch(image, label, image_W, image_H, batch_size, capacity):
    '''
    Args:
        image: list type
        label: list type
        image_W: image width
        image_H: image height
        batch_size: batch size
        capacity: the maximum elements in queue
    Returns:
        image_batch: 4D tensor [batch_size, width, height, 3], dtype=tf.float32
        label_batch: 1D tensor [batch_size], dtype=tf.int32
    '''

    image = tf.cast(image, tf.string) #类型转换
    label = tf.cast(label, tf.int32)

    # 生成队列
    '''
    可以被用来每次产生一个切片。这样就会让样本在
    整个迭代中被打乱，所以在使用批处理的时候不需要再次打乱样本。所以我们不使用 shuffle_batch 函数，取而
    代之的是纯 tf.train.batch 函数。
    '''
    input_queue = tf.train.slice_input_producer([image, label])

    label = input_queue[1]
    image_contents = tf.read_file(input_queue[0]) # 读取并输出输入文件名的全部内容
    image = tf.image.decode_jpeg(image_contents, channels=3) # 解码

    ######################################
    # data argumentation should go to here
    ######################################

    image = tf.image.resize_image_with_crop_or_pad(image, image_W, image_H) #裁剪或填充

    # if you want to test the generated batches of images, you might want to comment the following line.
    # 如果想看到正常的图片，请注释掉111行（标准化）和124行（转成float）
    # 训练时不要注释掉！
# '''
#     标准化处理可以使得不同的特征具有相同的尺度（Scale）。这样，在使用梯度下降法学习参数的时候，不同特征对参数的影响程度就一样了。
#     tf.image.per_image_standardization(image)，此函数的运算过程是将整幅图片标准化（不是归一化），加速神经网络的训练。
#     主要有如下操作，(x - mean) / adjusted_stddev，其中x为图片的RGB三通道像素值，mean分别为三通道像素的均值，
#     adjusted_stddev = max(stddev, 1.0/sqrt(image.NumElements()))。
#     stddev为三通道像素的标准差，image.NumElements()计算的是三通道各自的像素个数。
# '''
    image = tf.image.per_image_standardization(image)

    image_batch, label_batch = tf.train.batch([image, label],
                                                batch_size= batch_size,
                                                num_threads= 64, # The number of threads enqueuing tensors
                                                capacity = capacity # The maximum number of elements in the queue
                                             )

    #you can also use shuffle_batch
#    image_batch, label_batch = tf.train.shuffle_batch([image,label],
#                                                      batch_size=BATCH_SIZE,
#                                                      num_threads=64,
#                                                      capacity=CAPACITY,
#                                                      min_after_dequeue=CAPACITY-1)

    label_batch = tf.reshape(label_batch, [batch_size]) # Reshapes a tensor
    image_batch = tf.cast(image_batch, tf.float32) # 转换为float32格式

    return image_batch, label_batch

#%% TEST
# To test the generated batches of images
# When training the model, DO comment the following codes

# import matplotlib.pyplot as plt
#
# BATCH_SIZE = 2
# CAPACITY = 256
# IMG_W = 208
# IMG_H = 208
#
# train_dir = './train/'
#
# image_list, label_list = get_files(train_dir)
# image_batch, label_batch = get_batch(image_list, label_list, IMG_W, IMG_H, BATCH_SIZE, CAPACITY)
#
# with tf.Session() as sess:
#    i = 0
#    coord = tf.train.Coordinator()
#    threads = tf.train.start_queue_runners(coord=coord)
#
#    try:
#        while not coord.should_stop() and i<1:
#
#            img, label = sess.run([image_batch, label_batch])
#
#            # just test one batch
#            for j in np.arange(BATCH_SIZE):
#                print('label: %d' %label[j])
#                plt.imshow(img[j,:,:,:])
#                plt.show()
#            i+=1
#
#    except tf.errors.OutOfRangeError:
#        print('done!')
#    finally:
#        coord.request_stop()
#    coord.join(threads)


#%%
