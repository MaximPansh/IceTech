# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 21:45:08 2021

@author: Кирилл
"""
import math
import numpy as np
from scipy.integrate import quad
from matplotlib import pyplot as plt
def calc(v, h):
    """
    !!!TO DO!!!
   r, f_fur, yj - вопросы
    """
    E = 6*10**9  #  модуль упругости
   # h = 2.5  #  толщина льда
    u = 0.33 # к-т Пуассона
    po= 1025 # плотность воды
    po_l = 920 # плотность льда
    H = 1000 #глубина бассейна
    g = 9.81 # ускорение свободного падения
    D =  (E*h**3)/(12*(1-u**2)) #цилиндрическая жесткость
    m = po_l*h
    x = 0
    y = 0
    p = 100 # давление, Па
    yj= 0.126 # декремент затухания колебаний
    D1 = D/(po*g) 
    X1 = po_l *h/(po*g) 
    X0 = 0 # снег
    X = (po_l*h)/po
    n = 0.14
    n1 = n /(po*g)
    a = -h*po_l/po #глубина погружения льдины при статическом равновесии
    
    ## НЕ ПРАВИЛЬНО ПОСЧИТАНО ВОЛНОВОЕ ЧИСЛО
    
    r = (g*H)**(0.5)*(m/D)**(0.5)
    R = (x**2 + y**2)**0.5
    M = r*g*((1+X1*r*g*math.tanh(r)*H)**(-1))*math.tanh(r)*H
    l = (D1*r**4)+1
    tay =( l * M )**0.5
    

    #f0 = r*f_fur*M
    
    
    
    def interate_J (R, O, v, tay):
        global yj
        G = (r*(g*(a+H))**0.5)/(1+X1*r**(2)*g*(a+H))
        yj = (n1*(r**4)*g*math.tanh(r)*H)/(8*G*(1+(X+X0)*r*math.tanh(r)*H))
        d1 = r*v*math.cos(O) + -1*tay                     
        d2 = r*v*math.cos(O) + pow(-1,2)*tay
        return 2/(d1*d2)*2.7182**(1j*r*R*math.cos(O-yj))
    
    
    
    J = quad(interate_J, -math.pi/2, 3*math.pi/2 , args=(R, v, tay))
    
    
    def integrate_W(r,H):
        global yj
        G = (r*(g*(a+H))**0.5)/(1+X1*r**(2)*g*(a+H)) #частота волнения для мелкой воды
        yj = (n1*(r**4)*g*math.tanh(r)*H)/(8*G*(1+(X+X0)*r*math.tanh(r)*H))
        
        f_fur = (2*3.14)**0.5*yj    # фурье образ функции декардовых координат ОЧЕНЬ СПОРНЫЙ ВОПРОС
        f_fur = 1
        M = r*g*((1+X1*r*g*math.tanh(r)*H)**(-1))*math.tanh(r)*H
        # print('\n\n\n')
        # print(G)
        # print(f_fur)
        # print(M)
        # print('\n\n\n')
        return r*f_fur*M
    
    
    W = quad(integrate_W, 0, np.inf, args = (H) )
    a = p/(po*g)
    
    # print("Численное решение интеграла по эпсилон\n", J)
    J = round(J[0],3)
    # print(a)
    # print(J)
    # print(W[0])
    print(yj)
    print("Численное решение интеграла по r\n", W)
    # print("Значение прогиба, мм \n",(a*J*W[0])/(8*(3.1415**2)),"\n\n")
    return (a*J*W[0])/(8*(3.1415**2))

v = np.arange(0, 21, 0.5)
w_t = []
w_ex = []
h = [1.5, 2, 2.5, 3]
fig = plt.figure()
ax1 = fig.add_subplot()
for j in h:
    for i in v:
        w_t.append(calc(i, j))
        w_ex.append(0.140 * math.exp(0.1*i))
    ax1.plot(v,w_t, label = j)
    w_t = []


#ax1.plot(v,w_ex, label = "Экспериментальная кривая")
plt.legend()
plt.show()
