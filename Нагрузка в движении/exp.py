# -*- coding: utf-8 -*-
"""
Created on Wed May  5 12:18:29 2021

@author: Кирилл
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tkinter.filedialog import askopenfilename
import tkinter as tk 
import matplotlib.ticker as mtick
from scipy.optimize import curve_fit

def open_datafile(path):
    """
    Открыть файл с экспериментальными данными
    Запрашивает: путь к файлу(строковый тип), левая граница промежутка, правая граница промежутка 
    Возвращает массив из 3-х столбцов: время, сила, прогиб
    """
    
    try:
        file= open(path, encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
        data=pd.read_csv(file,sep='\s+' ,decimal="." ,header = None)
        print(data)
        data=np.array(data.values)    #перевод значений в массив Numpy
        float(data[-5,0])
        float(data[-10,0])
        
    except:
        file= open(path,encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
        data=pd.read_csv(file,sep='\s+' ,decimal=",", header = None ) #Читаю из тестового документа в качестве сепаратора: все пробелы
        data=np.array(data.values) 
        #data = np.flip(data, axis = 1)#перевод значений в массив Numpy
        
    #у переменной data сейчас тип dataframe
    file.close()
    return data

KG5 = open_datafile(askopenfilename())
KG10 = open_datafile(askopenfilename())
KG15 = open_datafile(askopenfilename())
KG21 = open_datafile(askopenfilename())

def func(x,k,b):
    return k*2.718**(b*x)


root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
fig = plt.figure(figsize=(width/100., height/100.))
plt.rcParams.update({'font.size': 20})
plt.gca().xaxis.set_major_locator(mtick.MultipleLocator(0.1))
plt.gca().yaxis.set_major_locator(mtick.MultipleLocator(0.1))


plt.xlim(0, KG21[np.argmax(KG21[:,0]),0]*1.1)
plt.ylim(0, KG21[np.argmax(KG21[:,0]),1]*1.1)

color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.4)
color3 = plt.cm.viridis(0.7)
color4 = plt.cm.viridis(.9)
popt,pcov = curve_fit(func,KG5[:,0],KG5[:,1], maxfev=10**6)
k,b = popt
kg = "кг"
Stat = "Cтатический прогиб"
zero = 0.055
print(k,'/n',b)
plt.scatter(KG5[:,0],KG5[:,1], c = color1, label = "11,32 "+kg)

plt.plot(KG5[:,0],func(KG5[:,0],*popt), c = color1, label = '$w_{max}$=%.3f$e^{%.3f v}$'%(k,b))

popt,pcov = curve_fit(func,KG10[:,0],KG10[:,1], maxfev=10**6)
k,b = popt
print(k,'/n',b)
plt.scatter(KG10[:,0],KG10[:,1], c = color2, label = "16,32 "+kg)

plt.plot(KG10[:,0],func(KG10[:,0],*popt), c = color2, label = '$w_{max}$=%.3f$e^{%.3f v}$'%(k,b))

popt,pcov = curve_fit(func,KG15[:,0],KG15[:,1], maxfev=10**6)
k,b = popt
print(k,'/n',b)
plt.scatter(KG15[:,0],KG15[:,1], c = color3, label = "21,32 "+kg)

plt.plot(KG15[:,0],func(KG15[:,0],*popt), c = color3, label = '$w_{max}$=%.3f$e^{%.3f v}$'%(k,b))

popt,pcov = curve_fit(func,KG21[:,0],KG21[:,1], maxfev=10**6)
k,b = popt
print(k,'/n',b)
plt.scatter(KG21[:,0],KG21[:,1], c = color4, label = "27,32 "+kg)

plt.plot(KG21[:,0],func(KG21[:,0],*popt), c = color4, label = '$w_{max}$=%.3f$e^{%.3f v}$'%(k,b))
plt.scatter(zero,0.3902, c = color1, s = 95, marker = 'X')
plt.scatter(zero,0.563, c = color2, s = 95, marker = 'X')
plt.scatter(zero,0.734, c = color3, s = 95, marker = 'X')
plt.scatter(zero,0.942, c = color4, s = 95, marker = 'X')
"""
plt.xlabel("Load travel velocity $\it{v}$, m/s")
plt.ylabel("Maximum deflection of the ice cover $w_{max}$, mm")
"""
plt.xlabel("Скорость движения нагрузки $\it{v}$, м/c")
plt.ylabel("Максимальный прогиб ледяного покрова $w_{max}$, мм")

plt.grid()
plt.legend(prop={'size':16})
plt.show()

