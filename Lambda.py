# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:03:12 2020

@author: Кирилл
"""
from matplotlib import pyplot as plt
import numpy as np 
import matplotlib.ticker as mtick
from GP_ice import onelayer_h
def F_array(X, k, p):
    return k*X**p
h = np.arange(start=0, stop=7, step=0.1)
"""
    12
20мм ЦП:
    0.3314, 1.761
20 мм 1 кан
    0.3524, 1.497
20 мм 2 кан
    1.549, 0.8266
 20 мм 3 кан
    0.9811, 1.001  
    
    8.5
10 мм ЦП:
    3.912, 1.378
10мм 1 кан:
    2.617, 1.199
10мм 2 кан:    
    3.027, 0.9463
10мм 3 кан:      
    4.485, 0.6963
    
    7
3мм ЦП
    2.035, 1.76
3мм 1 кан
    2.663, 1.39
3мм 2 кан
    2.21, 1.381
3 мм 3 кан
    0.9332, 1.922
"""
filename = "3 мм 3 кан"
F = F_array(h, 0.9332, 1.922)
h_ice = np.array(onelayer_h(h, 3))
F_end = F/(pow(h_ice,2))
Lam = 2.786/F_end
fig = plt.figure()

#Статистические параметры оценки регрессии из метода summary:

#Цвета графиков:
color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)
color3 = plt.cm.viridis(.9)

#Пределы осей:
#ax1.set_xlim(0)
#ax1.set_ylim(0, F_end[-1]+F_end[-1]*0.1)
ax1 = fig.add_subplot(2, 2, 1)
#Названия осей:
ax1.set_xlabel('Толщина проморозки $h_{пром}$, мм')
ax1.set_ylabel('Коэффицент разрушающей силы $F_{max}$/ $h_{льда}^2$')

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))

#Рисуем графики
ax1.plot(h, F_end)

ax2 = fig.add_subplot(2, 2, 2)
#Пределы осей:
#ax2.set_xlim(0)
ax2.set_ylim(0, 100)

#Названия осей:
ax2.set_xlabel('Толщина проморозки $h_{пром}$, мм')
ax2.set_ylabel('Геометрическй масштаб λ')

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))
ax2.plot(h, Lam)

ax3 = fig.add_subplot(2, 2, 3)
Hn = h_ice*Lam
#Пределы осей:
#ax2.set_xlim(0)
ax3.set_ylim(0, 500)

#Названия осей:
ax3.set_xlabel('Толщина проморозки $h_{пром}$, мм')
ax3.set_ylabel('Толщина натурного льда, мм')

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))

ax3.plot(h, Hn)
np.savetxt(filename +'.txt', np.column_stack((h, F_end, Lam, Hn)))
fig.savefig(filename+'.png')
plt.show()

