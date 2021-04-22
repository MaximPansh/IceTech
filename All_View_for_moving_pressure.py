# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 16:05:12 2021

@author: Кирилл
"""

from matplotlib import pyplot as plt
import numpy as np 
import matplotlib.ticker as mtick
import pandas as pd
import tkinter as tk # use tkinter for python 3
import os
from tkinter.filedialog import askopenfilename
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
folder =  askopenfilename() #папка с файлами
folder = os.path.dirname(folder) #Переход к директории выше чем выбранный файл
direct = os.path.dirname(folder)
files = os.listdir(folder) #формируем список путей к файлам
direct_files = os.listdir(direct) 
def open_datafile(path,a=1,b=20000000):
    """
    Открыть файл с экспериментальными данными
    Запрашивает: путь к файлу(строковый тип), левая граница промежутка, правая граница промежутка 
    Возвращает массив из 3-х столбцов: время, сила, прогиб
    """
    
    try:
        file= open(path, encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
        data=pd.read_csv(file,sep='\s+' ,decimal="." )
        data=np.array(data.values)    #перевод значений в массив Numpy
        float(data[-5,0])
        float(data[-10,0])
        
    except:
        file= open(path,encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
        data=pd.read_csv(file,sep='\s+' ,decimal="," ) #Читаю из тестового документа в качестве сепаратора: все пробелы
        data=np.array(data.values) 
        #data = np.flip(data, axis = 1)#перевод значений в массив Numpy
        
    #у переменной data сейчас тип dataframe
    file.close()
    return data[a:(b+1)]

fig = plt.figure(figsize=(width/100., height/100.))       
ax4 = fig.add_subplot()
for f in files:
    data_S = open_datafile(folder + '/' + f) 
    print("Читаю ", f)
   # data_save = np.copy(data_S)
    sensor_len = 6 
    index = (np.abs(data_S[:,1]-np.argmin(data_S[:,1]))).argmax()
    ax4.set_xlabel('Метры ледяного поля, м')
    ax4.set_ylabel('Прогиб, мм')
    data_S[:,0]= data_S[:,0]-data_S[index,0]
    data_S[:,1] = data_S[:,1] - data_S[int(np.argwhere(data_S[:, 0] == data_S[0, 0])[-1]),1]
  #  print("%.4f" %float(data_S[int(np.argmin(data_S[:,1])), 1]))
    data_S = data_S[int(np.argwhere(data_S[:, 0] == data_S[0, 0])[-1]):
                    int(np.argwhere(data_S[:, 0] == data_S[-1, 0])[0])]
  #  print('min=',np.abs(np.abs(data_S[0:np.argmin(data_S[:,1]),1])-0.004) )
    
    try:
        left_indx = np.argmin(np.abs(np.abs(data_S[0:np.argmax(data_S[0:np.argmin(data_S[:, 1]), 1]), 1])))
    except:
        left_array = 0
        #left_array = np.abs(data_S[np.argmin(data_S[0:np.argmax(data_S[0:np.argmin(data_S[:,1]), 1]), 1])
#                                   :np.argmax(data_S[0:np.argmin(data_S[:,1]), 1])])
        #left_indx = left_array[np.argmin(left_array[:, 1]), 0]
       # left_indx = np.abs(data_S[:,0] - left_indx*(-1)).argmin()
        
    mid_array = np.abs(data_S[np.argmax(data_S[0:np.argmin(data_S[:, 1]), 1]):
                              np.argmin(data_S[:, 1])])
    mid_indx = mid_array[np.argmin(mid_array[:, 1]), 0]
    mid_indx = np.abs(data_S[:,0] - mid_indx*(-1)).argmin()
    if data_S[-1, 1] < 0:
        data_S = np.vstack([data_S,[(((0 - data_S[-1, 1]) / (data_S[-5000, 1] - data_S[-1, 1])) * (data_S[-5000, 0] - data_S[-1, 0]) + data_S[-1, 0]),0]])
    if data_S[-1,1] > 0:
        right_array = np.abs(data_S[np.argmin(data_S[:, 1]):-1])
        right_indx = right_array[np.argmin(right_array[:, 1]), 0]
        right_indx = np.abs(data_S[:,0] - right_indx).argmin()
       # right_indx = np.abs(data_S[-1:np.argmin(data_S[:,1]):-1,1]).argmin()
    else:
        right_indx = -1
    ax4.plot(data_S[:, 0],
             data_S[:, 1], 
             label = "Скорость: " + f.split('_')[-2]+" м/c \n" + "Прогиб: "+ str("%.3f" %float(f.split(' ')[0])) + " мм")
             #label = f.split('(')[-1].split("_")[0].split(')')[0])
    ax4.scatter(data_S[left_indx,0],data_S[left_indx,1],color='orange', s=50, marker='o')
    ax4.scatter(data_S[mid_indx,0],data_S[mid_indx,1],color='red', s=50, marker='o')
    ax4.scatter(data_S[right_indx,0],data_S[right_indx,1],color='blue', s=50, marker='o')
    
   
    #ax4.scatter(data_S[np.argmax(data_S[0:np.argmin(data_S[:, 1]), 1]),0],data_S[np.argmax(data_S[0:np.argmin(data_S[:, 1]), 1]),1],color='blue', s=50, marker='o')
    
    
    
    #np.savetxt( str("%.4f" %float(np.abs(data_S[int(np.argmin(data_S[:,1])), 1]))) + f[0:-4] + '.txt', data_save)
    
ax4.xaxis.set_major_locator(mtick.MultipleLocator(1))
ax4.yaxis.set_major_locator(mtick.MultipleLocator(0.1))

plt.grid()
ax4.legend()
plt.show()