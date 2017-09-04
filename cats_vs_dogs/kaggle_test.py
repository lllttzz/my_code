import os
import gui_evaluate
import csv


train_dir = './test2/' # 数据存放位置
name = []
label = []
def get_files(file_dir):
    for file in os.listdir(file_dir):
        n = file.split(sep='.')
        label.append(gui_evaluate.get_a_picture_evaluate(train_dir+file))
        name.append(n[0])
        label1 = [str(k) for k in label]


    csvfile = open('csv.csv', 'w', newline='')
    writer = csv.writer(csvfile)
    writer.writerow(['name','label'])
    for (i,j) in zip(name,label1):
        writer.writerow([i,j])
    csvfile.close()

    
get_files('./test2/')
