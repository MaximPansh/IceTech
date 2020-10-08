# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 13:08:08 2020

@author: Кирилл
"""
import pandas as pd
import os
folder = "D:/Python/Exel_sum/Files" #папка с файлами
files = os.listdir(folder) #формируем список путей к файлам
all_file_frames = [] #сюда будем добавлять прочитанную таблицу
ind=['gran_d' ,'hice', 'h', 'Fmax', 'Wmax',
       'kp', 'kw', 'Ap', 'A1', 'A2',
       'Asum', 'kp1', 'kp2', 'kp_sum',
       'k_a'] 
for f in files:
    print('Reading %s'%(folder+'/'+f))
    tab = pd.read_excel(folder+'/'+f, header=None)
    all_file_frames.append(tab)

all_frame = pd.concat(all_file_frames,axis=1) #  axis=0 если нужно добавить таблицу снизу и axis=1 если нужно слева
all_frame.to_excel('final_file.xlsx' ,header= False,index= False) 
                   #index=True, index_label=['gran_d' ,'hice', 'h', 'Fmax', 'Wmax', 'kp', 'kw', 'Ap', 'A1', 'A2', 'Asum', 'kp1', 'kp2', 'kp_sum', 'k_a','0','8','87']