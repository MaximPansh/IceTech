# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 13:23:59 2021

@author: Кирилл
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.signal
import pandas as pd
import math
from tkinter.filedialog import askopenfilename
def open_datafile(path,a=1,b=20000000):
    """
    Открыть файл с экспериментальными данными
    Запрашивает: путь к файлу(строковый тип), левая граница промежутка, правая граница промежутка 
    Возвращает массив из 3-х столбцов: время, сила, прогиб
    """
    
    try:
        file= open(path,encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
        data=pd.read_csv(file,sep='\s+' ,decimal="." )
        data=np.array(data.values)    #перевод значений в массив Numpy
        float(data[-5,0])
        float(data[-10,0])
        
    except ValueError:
        file= open(path,encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
        data=pd.read_csv(file,sep='\s+' ,decimal="," ) #Читаю из тестового документа в качестве сепаратора: все пробелы
        data=np.array(data.values) 
        data = np.flip(data, axis = 1)#перевод значений в массив Numpy
        
    #у переменной data сейчас тип dataframe
    file.close()
    return data[a:(b+1)]

"""
Переменные
"""
d = 3 # диаметр
Volt_ch = 2 # граница напряжения относительно которой сравниваем
med = 101 #размер ядра фильтрации медианного фильтра

filename=askopenfilename()# Вызов окна открытия файла
data=open_datafile(filename) #Открыть файл с данными 
fig, ax = plt.subplots() # создаем объект figure и axes
T = data[:,0]
V = data[:,1]

V = sp.signal.medfilt(V, med)

V[0], V[-1] = 0, 0

# поиск точек подъема и падения
n = np.array(np.where(V > Volt_ch))[0,: ] # массив координат где V > 2
n = np.vstack((n[np.where(V[n - 1] < Volt_ch)], n[np.where(V[n + 1] < Volt_ch)]))# двумерный массив с точками подъема и падения
# первый столбец ищет точки на одну итерацию меньше где происходит изменение напряжения,
# второй столбец аналогично но итерация вперед

# Построение точек и графика напряжения от времени
ax.plot(T, V)
plt.scatter(T[n[0]], V[n[0]])#n[0] - индексы точек подъёма
plt.scatter(T[n[1]], V[n[1]])#n[1] - индексы точек падения
ax.set_xlabel('Время, сек')
ax.set_ylabel('Напряжение, В \n Скорость, мм/сек')

v = 1/(((T[n[0, 1:]] + T[n[1, 1:]]) / 2) - ((T[n[0, :-1]] + T[n[1, :-1]]) / 2)) 
v = (math.pi* d /360) * np.hstack([ v, np.array(1 / (((T[n[0, -1]] + T[n[1, -1]]) / 2) - ((T[n[0, -2]] + T[n[1, -2]])/2)))])
t = (((T[n[0, 1:]] + T[n[1, 1:]]) / 2) + ((T[n[0, :-1]] + T[n[1, :-1]]) / 2))/2
t = np.hstack([ t, np.array((((T[n[0, -1]] + T[n[1, -1]]) / 2) + ((T[n[0, -2]] + T[n[1, -2]])/2)) / 2)])


plt.plot(t,v)# скорость от времени построение графика
plt.grid()
plt.show()