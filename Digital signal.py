# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 13:23:59 2021

@author: Кирилл
"""
import matplotlib.pyplot as plt
import numpy as np

V = np.array([0,0,5,5,5,5,0,0,0,0,5,5,5,0,0,0,5,5]) 
T = np.array([0,1,1,2,3,4,4,5,6,7,7,8,9,9,10,11,11,12])
if V[-1] != 0:
    V = np.append(V,0)
    T = np.append(T,T[-1])
def Velosity(T, V, time_set = 0.1):
    
    RISE = [] # список точек "подъема" цифрового сигнала
    FALL = [] # список точек "падения" цифрового сигнала
    VEL = [] # список скоростей
    VEL1 = [] # список скоростей
    TIME = [] #список времени

    for i in np.where(V > 0)[0]: #цикл по всем точкам где напряжение больше 0
        if V[i-1] < 5: 
            RISE.append(i) # добавляем точку начала цифрового сигнала
        if V[i+1] > 5:
            FALL.append(i) # добавляем точку конца цифрового сигнала
    for i in range(len(RISE)): 
        if i!=len(RISE)-1:
            VEL.append(1/(T[RISE[i+1]]-T[RISE[i]])) #1/dT где dТ время между двумя началами цифрового сигнала
            VEL1.append(1/(T[FALL[i+1]]-T[FALL[i]])) 
            TIME.append((T[RISE[i+1]]+T[RISE[i]])/2)# среднее время между двумя точками
            
    return np.column_stack((np.array(VEL),np.array(VEL1, np.array(TIME))))


print(Velosity(T,V))
fig, ax = plt.subplots()
ax.plot(T, V)
plt.grid()
plt.show()


input()
