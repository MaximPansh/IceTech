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
h = np.arange(start=0, stop=8.5, step=0.1)
F = F_array(h, 3.912, 1.378)
h_ice = np.array(onelayer_h(h, 10))
print(type(h_ice))
F_end = F/(h_ice**2)
Lam = 2.786/F_end
fig = plt.figure()
ax1 = fig.add_subplot(2, 2, 1)
#Статистические параметры оценки регрессии из метода summary:

#Цвета графиков:
color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)
color3 = plt.cm.viridis(.9)

#Пределы осей:
#ax1.set_xlim(0)
#ax1.set_ylim(0, F_end[-1]+F_end[-1]*0.1)

#Названия осей:
ax1.set_xlabel('Толщина проморозки $h_{пром}$, мм')
ax1.set_ylabel('Коэффицент разрушающей силы $F_{max}$/ $h_{льда}^2$')

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))

#Рисуем графики
ax1.plot(h, h_ice)

ax2 = fig.add_subplot(2, 2, 2)
#Пределы осей:
#ax2.set_xlim(0)
ax2.set_ylim(0, Lam[1]+Lam[1]*0.05)

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
ax3.set_ylim(0, Hn[1]+Hn[1]*0.05)

#Названия осей:
ax3.set_xlabel('Толщина проморозки $h_{пром}$, мм')
ax3.set_ylabel('Толщина натурного льда, мм')

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))

ax3.plot(h, Hn)

plt.show()

