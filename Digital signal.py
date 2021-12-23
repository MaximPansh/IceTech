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


def butter_lowpass(normal_cutoff, order=5):
    """
    Настройка фильтра Баттерворта
    """
    return sp.signal.butter(order, normal_cutoff, btype='low', analog=False)


def butter_lowpass_filtfilt(data, normal_cutoff, order=5):
    """
    Низкочастотный фильтр Баттерворта. Вызывает функцию настройки фильтра Баттерворта.
    Запрашивает: 1-мерный массив данных, нормальную отсечку, порядок
    Возвращает: 1-мерный отфильтрованный массив
    """
    b, a = butter_lowpass(normal_cutoff, order=order)
    return sp.signal.filtfilt(b, a, data)

def tar_w(V, k, null_point=0):
    """
    Преобразование показаний датчика перемещений (Вольты в миллиметры)
    Тарировочное уравнение вида w(V)=kV+b
    Запрашивает: показания датчика перемещений (Вольты), k, номер начальной точки (стандартное значение 0)
    Возвращает w(массив)

    """
    b=-k*V[null_point]  
    return np.array(k*V+b) #Тарировочное уравнение

"""
Переменные
"""
d = 246 # диаметр
Volt_ch = 2 # граница напряжения относительно которой сравниваем
med = 5 #размер ядра фильтрации медианного фильтра
bat = 0.02

filename = askopenfilename()# Вызов окна открытия файла
data = open_datafile(filename) #Открыть файл с данными 


fig, ax = plt.subplots(1,3) # создаем объект figure и axes
T = data[:,0]
V = data[:,2]
#plt.plot(T,V)
#V = sp.signal.medfilt(V, med)

V[0], V[-1] = 0, 0

# поиск точек подъема и падения
n = np.array(np.where(V > Volt_ch))[0,: ] # массив координат где V > 2
n = np.vstack((n[np.where(V[n - 1] < Volt_ch)], n[np.where(V[n + 1] < Volt_ch)]))# двумерный массив с точками подъема и падения
# первый столбец ищет точки на одну итерацию меньше где происходит изменение напряжения,
# второй столбец аналогично но итерация вперед



v = 1/(((T[n[0, 1:]] + T[n[1, 1:]]) / 2) - ((T[n[0, :-1]] + T[n[1, :-1]]) / 2)) 
v = (math.pi* d /360) * np.hstack([ v, np.array(1 / (((T[n[0, -1]] + T[n[1, -1]]) / 2) - ((T[n[0, -2]] + T[n[1, -2]])/2)))])
t = (((T[n[0, 1:]] + T[n[1, 1:]]) / 2) + ((T[n[0, :-1]] + T[n[1, :-1]]) / 2))/2
t = np.hstack([ t, np.array((((T[n[0, -1]] + T[n[1, -1]]) / 2) + ((T[n[0, -2]] + T[n[1, -2]])/2)) / 2)])



ax[0].set_xlabel('Время, сек')
ax[0].set_ylabel('Напряжение, В \n Скорость, мм/сек')
ax[0].plot(t,v, label = "Не фильтованый")
v = sp.signal.medfilt(v, med)
v = butter_lowpass_filtfilt(v, bat)
ax[0].plot(t,v, label = "Медианый + Батерворта")# скорость от времени построение графика
ax[1].plot(t,tar_w(data[:,1], k = 1.6084))
ax[2].plot(t,tar_w(data[:,3], k = -1.5389))
ax[3].plot(t,tar_w(data[:,4], k = 1.5763))


plt.legend()
plt.grid()
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()