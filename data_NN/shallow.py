# encoding=utf-8
from layers import *


def main():
    datalayer1 = Data('train.npy', 1024)  # 用于训练，batch_size设置为1024
    datalayer2 = Data('validate.npy', 10000)  # 用于验证，所以设置batch_size为10000,一次性计算所有的样例
    inner_layers = []
    inner_layers.append(FullyConnect(17 * 17, 26))
    inner_layers.append(Sigmoid())
    #inner_layers = [FullyConnect(17 * 17, 26)，Sigmoid()]
    losslayer = QuadraticLoss() #损失函数
    accuracy = Accuracy()

    for layer in inner_layers:
        layer.lr = 1000.0  # 为所有中间层设置学习速率

    epochs = 20
    for i in range(epochs):
        print('epochs:', i)
        losssum = 0 #总误差
        iters = 0
        while True:
            data, pos = datalayer1.forward()  # 从数据层取出数据
            x, label = data #data = ret([一个batch_size中的所有数据，相当于一组batch_size数量的图片],[每一列数据的标签])
            for layer in inner_layers:  # 前向计算
                x = layer.forward(x) # 这一层前向计算的输出继续作为下一层前向计算的输入

            loss = losslayer.forward(x, label)  # 调用损失层forward函数计算损失函数值
            losssum += loss # 总的误差值 = 所有误差值相加
            iters += 1
            d = losslayer.backward()  # 调用损失层backward函数曾计算将要反向传播的梯度

            for layer in inner_layers[::-1]:  # 反向传播（ [::-1]倒序 ），所以先从Sigmoid开始计算
                d = layer.backward(d)

            if pos == 0:  # 一个epoch完成后进行准确率测试
                data, _ = datalayer2.forward()
                x, label = data
                for layer in inner_layers:
                    x = layer.forward(x)
                accu = accuracy.forward(x, label)  # 调用准确率层forward()函数求出准确率
                print('loss:', losssum / iters)
                print('accuracy:', accu)
                break


if __name__ == '__main__':
    main()
