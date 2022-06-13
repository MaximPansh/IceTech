# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:35:26 2020

@author: Кирилл
"""

import pandas as pd
import os
from tkinter.filedialog import askopenfilename
while True:
    inp=input("\nНажмите Enter если хотите выполнить сложение с транспонированием и добавлением имён.\n Нажмите 1 если хотите выполнить сложение дней в один файл\n Нажмите 2 чтобы выйти\n")
    try:
        inp = int(inp)
    except:
        pass
    if inp == 2:
        break
    folder =  askopenfilename() #папка с файлами
    folder = os.path.dirname(folder) #Переход к директории выше чем выбранный файл
    direct = os.path.dirname(folder)
    files = os.listdir(folder) #формируем список путей к файлам
    direct_files = os.listdir(direct) 
    
    #print('files=',files,'/n folder=',folder )
    
    all_file_frames = [] #сюда будем добавлять прочитанную таблицу
    ind=['gran_d' ,'hice', 'h', 'Fmax', 'Wmax',
           'kp', 'kw', 'Ap', 'A1', 'A2',
           'Asum', 'kp1', 'kp2', 'kp_sum',
           'k_a', 'D', 'E', 'r' ] 
    all_file_frames.append(pd.Series(folder.split('/')[-1].split(' ')[0]))
    for f in files:
        print('Reading %s'%(folder + '/' + f))
        tab = pd.read_excel(folder + '/' + f, header=None)
        if inp != 1:
            for i in f:
                if i == '_':
                    tab.loc[0] = f.split('_')[1]
                elif i == '.':
                    tab.loc[0] = f.split('.')[0]
                elif i == ' ':
                    tab.loc[0] = f.split(' ')[0]
                else:
                    tab.loc[0] = f[0:2]
        print(tab)
        all_file_frames.append(tab)
    if inp != 1:
        ax = 1
    else:
        ax = 0
    all_frame = pd.concat(all_file_frames,axis=ax) #  axis=0 если нужно добавить таблицу снизу и axis=1 если нужно слева
    if inp != 1:
        all_frame = all_frame.T
        print(all_frame)
       # all_frame = all_frame.shift(1, axis = 0)
      #  all_frame.loc[0,0] = filename.split(' ')[0]
    filename = folder.split('/')[-1]
    all_frame.to_excel(filename+'.xlsx' ,header = False, index = False) 
              