# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:08:08 2020

@author: Кирилл
"""
import pandas as pd
import os
from tkinter.filedialog import askopenfilename
folder =  askopenfilename() #папка с файлами
folder = os.path.dirname(folder) #Переход к директории выше чем выбранный файл
print(folder)
direct = os.path.dirname(folder)
print(direct)
files = os.listdir(folder) #формируем список путей к файлам
direct_files = os.listdir(direct) 
print(direct_files)
#print('files=',files,'/n folder=',folder )
inp=input("Нажмите Enter если хотите выполнить сложение с транспонированием и добавлением имён.\n Нажмите 1 если хотите выполнить сложение дней в один файл")
all_file_frames = [] #сюда будем добавлять прочитанную таблицу
ind=['gran_d' ,'hice', 'h', 'Fmax', 'Wmax',
       'kp', 'kw', 'Ap', 'A1', 'A2',
       'Asum', 'kp1', 'kp2', 'kp_sum',
       'k_a', 'D', 'E', 'r' ] 

for d in direct_files:
    #filename = direct.split('/')[-1]
    all_file_frames.append(pd.Series(d.split(' ')[0]))
    for f in files:
        # TODO   Разбить folder и добавить d
        print('Reading %s'%(direct + '/' + d + '/' + f))
        tab = pd.read_excel(direct + '/' + d + '/' + f, header=None)
        if inp != 1:
            try:
                tab.loc[0] = f.split('_')[0]
            except:
                tab.loc[0] = f[0:2]
        print(tab)
        all_file_frames.append(tab)
if inp != 1:
    ax = 1
else:
    ax = 0
all_frame = pd.concat(all_file_frames,axis=ax) #  axis=0 если нужно добавить таблицу снизу и axis=1 если нужно слева
if inp != 1:
    print(all_frame)
    all_frame = all_frame.T
   # all_frame = all_frame.shift(1, axis = 0)
  #  all_frame.loc[0,0] = filename.split(' ')[0]
filename = direct.split('/')[-1]
all_frame.to_excel(filename+'.xlsx' ,header = False, index = False) 
input()                  
 #index=True, index_label=['gran_d' ,'hice', 'h', 'Fmax', 'Wmax', 'kp', 'kw', 'Ap', 'A1', 'A2', 'Asum', 'kp1', 'kp2', 'kp_sum', 'k_a','0','8','87']
