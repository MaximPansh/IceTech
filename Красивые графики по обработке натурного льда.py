# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 09:41:14 2022

@author: Кирилл
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tkinter.filedialog import askopenfilename
import matplotlib.ticker as mtick

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
        
    except ValueError:
        file= open(path, encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
        data = pd.read_csv(file,sep='\s+' ,decimal="," ) #Читаю из тестового документа в качестве сепаратора: все пробелы
        data = np.array(data.values) 
        print(data)

        
    #у переменной data сейчас тип dataframe
    file.close()
    return data
def plot_aprx(Koef,data):
    global ax
    if Koef[-1] == 0:
        pass
    else:
        data = np.sort(data, axis = 0)
        h = np.arange(data[0,0], data[-1,0], 0.1)
        ax.plot(h, Koef[1]*h**Koef[-1], label = Koef[0] + '= %.3f$h^{%.3f}$'%(Koef[1],Koef[-1]), linewidth = 2)
        plt.legend(loc=2, prop={'size': 16})
label_dic = {'1': 'Максимальная сила, Н', '2':'Прогиб при максимальной силе, мм' , '3':'Максимальный прогиб, мм',
             '4':'Работа критической части диаграммы, Дж', '5': 'Работа закритической части диаграммы, Дж',
             '6': 'Общая работа разрушения, Дж', '7': ' Коэффициент формы критической части диаграммы',
             '8': 'Коэффициент формы закритической части диаграммы', '9': 'Коэффициент формы диаграммы разрушения',
             '10': 'Отношение критической работы разрушения к общей работе', '11': 'Прогиб льда в закритической части' }

dic_DV = {"1":['$F_{max}$' , 0.2786, 2],
           '2':['$W_{max}$' ,6.3248  , 0.406],
           '3':['$W_{end}$' ,14.707  , 0.217],
           "4":['$A_{1}$' , 7.218, 2.5],
           '5':['$A_{2}$',5.898 , 2.06 ],#
           '6':['$A_{sum}$',15 , 2.35],#
           '7':['$K_{A1}$',0 , 0],
           '8':['$K_{A2}$',0 ,0 ],
           '9':['$K_{Asum}$',0 , 0],
           '10':['$A_{1}$/$A_{sum}$',0 , 0],
           '11':['$W_{A2}$' ,8.3251 ,-0.075 ]
           }

dic_KN = {"1":['$F_{max}$' , 2.73, 2],
           '2':['$W_{max}$' ,9.247  , 0.2],
           '3':['$W_{end}$' ,0  , 0],
           "4":['$A_{1}$' , 0.0042, 2.5],
           '5':['$A_{2}$',0.0168 , 2.5 ],#
           '6':['$A_{sum}$',0.0384 , 2.35],#
           '7':['$K_{A1}$',0 , 0],
           '8':['$K_{A2}$',0 ,0 ],
           '9':['$K_{Asum}$',0 , 0],
           '10':['$A_{1}$/$A_{sum}$',0 , 0],
           '11':['$W_{A2}$' ,0 ,0 ]
           }
SIZE= 20
X = 2
DIC = dic_KN




filename=askopenfilename()# Вызов окна открытия файла
data=open_datafile(filename) #Открыть файл
fig, ax = plt.subplots(1,1) # создаем объект figure и axes
ax.tick_params(labelsize=SIZE - 2)

ax.set_xlabel('Толщина проморозки, мм', size = SIZE)
ax.set_ylabel(label_dic[filename.split('/')[-1].split('.')[0]], size = SIZE)
ax.set_xlim(0, round(data[np.argmax(data[:,0]), 0]*1.05, 0)+1)
ax.set_ylim(0, round(data[np.argmax(data[:,1]), 1]*1.1, 1))
#ax.set_ylim(0, 0.5)
plt.grid()
ax.xaxis.set_major_locator(mtick.MultipleLocator(X))# цена деления


ax.scatter(data[:,0], data[:,1], s = 70, c = 'm')
plot_aprx(DIC[filename.split('/')[-1].split('.')[0]], data)
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()

fig.savefig(filename[0:-4]+'.png')
plt.show()