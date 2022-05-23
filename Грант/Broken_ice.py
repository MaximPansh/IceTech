# -*- coding: utf-8 -*-
"""
Created on Mon May  9 13:46:19 2022

@author: Кирилл
"""
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick


Geom = np.array([0.466, 0.477, 3.46, 0.96,
                          5.28, 1.52, 0.072, 0.744,
                          0.068, 0.241, 0.006, 0.023])


def R_1 (h, B, v, Geom, g = 9.81, f = 0.15, po_l = 0.92, po = 1, Ci = None):
    """
    Функция расчета импульсного сопротивления судна при движении в битых льдах.
    При вводе параметров в виде массивов данных, необходимо размеры входных массивов 
    привести к одному порядку.
    Parameters
    ----------
    h : TYPE - NP.Array, INT, FLOAT
        DESCRIPTION.Толщина ледяного покрова, м
                
    B : TYPE -  INT, FLOAT
        DESCRIPTION. Ширина судна, м
                
    v : TYPE - NP.Array, INT, FLOAT
        DESCRIPTION. Скорость движения судна, м\с
        
    Geom : TYPE - NP.Array
        DESCRIPTION.Одномерный массив геометрических характеристик корпуса судна
                
    g : TYPE, optional FLOAT
        DESCRIPTION. Ускорение свободного падения м\с2 Стандартное значение 9.81.
        
    f : TYPE, optional FLOAT
        DESCRIPTION. Коэффициент трения льда о корпус судна. Стандартное значение 0.24.
        
    po_l : TYPE, optional FLOAT
        DESCRIPTION. Плотность ледяного покрова т\м3. Стандартное значение 0.92.
        
    po : TYPE, optional FLOAT
        DESCRIPTION. Плотность воды т\м3. Стандартное значение 1.
        
    Ci : TYPE, optional FLOAT, INT
        DESCRIPTION.Коэффициент учитывающий присоединенные массы воды.
        Стандартное значение None, при не изменении стандартного значения 
        расчитывается по формуле внутри функции

    Returns
    -------
    TYPE FLOAT, NP.ARRAY
        DESCRIPTION. Функция возращает число равное импульсному сопротивлению судна кН.
        При вводе в функцию  одномерного массива с размером N возравщается массив размера N

    """
    if Ci == None:
        puas = 0.35 # коэффициент Пуассона
        E = 5.8 * 10**6 #модуль упругости пресного льда
        D = E * h**3 / (12 * (1 - puas**2))
        alf = (po * g / D)**0.25
        b = 0.312 / alf
        Ci = 1 + (0.218 * b / h) * (po / po_l)
    return Ci * po_l * h * (B/2) * (v**2) * (Geom[8] + f * Geom[9])
    

def R_2 ( h, B, v, Geom, f = 0.15, po = 1, Cg = 2):
    """
    Функция расчитывающие сопротивление судна обусловленное рассеиванием энергии движущегося
    состающее из двух слагаемых: диссипативной составляющиией вследствии сопротивления воды
    раздвиганию льдин и диссипативной составляющией обусловленной трением льдин друг об друга.
    При вводе параметров в виде массивов данных, необходимо размеры входных массивов 
    привести к одному порядку.

    Parameters
   h : TYPE - NP.Array, INT, FLOAT
        DESCRIPTION.Толщина ледяного покрова, м
                
    B : TYPE -  INT, FLOAT
        DESCRIPTION. Ширина судна, м
                
    v : TYPE - NP.Array, INT, FLOAT
        DESCRIPTION. Скорость движения судна, м\с
     Geom : TYPE - NP.Array
        DESCRIPTION.Одномерный массив геометрических характеристик корпуса судна
    f : TYPE, optional FLOAT
        DESCRIPTION. Коэффициент трения льда о корпус судна. Стандартное значение 0.24.

    po : TYPE, optional FLOAT
        DESCRIPTION. Плотность воды т\м3. Стандартное значение 1.
        
    Cg : TYPE, optional FLOAT, INT
        DESCRIPTION.Коэффициент учитывающий гидродинамическое сопротивление 
        при раздвигании льдин.
        Стандартное значение 2
   Returns
    -------
    TYPE FLOAT, NP.ARRAY
        DESCRIPTION. Функция возращает число или массив числе равное сопротивлению
        воды раздвиганию льдин и трения льдин друг об друга , кН.
        При вводе в функцию  одномерного массива с размером N возравщается массив размера N


    """
    return Cg * po * (v**2) * h * (B/2) * (Geom[10] + f * Geom[11])


def R_3 (h, B, Geom, g = 9.81, f = 0.15, po_l = 0.92, po = 1):
    """
    Функция расчета сопротивления судна обсуловленного притаплиыванием
    и поворачиванием льдин.    
    При вводе параметров в виде массивов данных, необходимо размеры входных массивов 
    привести к одному порядку.

    Parameters
    ----------
     h : TYPE - NP.Array, INT, FLOAT
        DESCRIPTION.Толщина ледяного покрова, м
                
    B : TYPE -  INT, FLOAT
        DESCRIPTION. Ширина судна, м
     Geom : TYPE - NP.Array
        DESCRIPTION.Одномерный массив геометрических характеристик корпуса судна
                
    g : TYPE, optional FLOAT
        DESCRIPTION. Ускорение свободного падения м\с2 Стандартное значение 9.81.
        
    f : TYPE, optional FLOAT
        DESCRIPTION. Коэффициент трения льда о корпус судна. Стандартное значение 0.24.
        
    po_l : TYPE, optional FLOAT
        DESCRIPTION. Плотность ледяного покрова т\м3. Стандартное значение 0.92.
        
    po : TYPE, optional FLOAT
        DESCRIPTION. Плотность воды т\м3. Стандартное значение 1.
        

    Returns
    -------
    TYPE FLOAT, NP.ARRAY
        DESCRIPTION. Возрвращает число или массив чисел от притапливания и 
        поворачивания льдин, кН
        При вводе в функцию  одномерного массива с размером N возравщается массив размера N
        

    """
    
    puas = 0.35 # коэффициент Пуассона
    E = 5.8 * 10**6 #Модуль упругости пресного льда
    D = E * h**3 / (12 * (1 - puas**2)) #Цилиндрическая жесткость
    alf = (po * g / D)**0.25 #Коэффициент упругого основания пластины
    b = 0.312 / alf # ширина льдины
    return (po_l + po) * g * h * b * B * (Geom[6] + f * Geom[7])


def R_Zuev(h, B, v, po_l = 0.92, g = 9.82, S = 0.9):
    """
    

    Parameters
    ----------
    h : TYPE
        DESCRIPTION.
    B : TYPE
        DESCRIPTION.
    po_l : TYPE, optional
        DESCRIPTION. The default is 0.92.
    g : TYPE, optional
        DESCRIPTION. The default is 9.82.
    S : TYPE, optional
        DESCRIPTION. The default is 10.

    Returns
    -------
    None.

    """
    Fr_h = v/(g * h)**0.5

    return (po_l * g * B * h**2) * ((0.13 * B / h) + (1.3 * Fr_h) + (0.5*Fr_h**2)) * (2 - S) * S**2


def Thrust_line (P_w, v, v0, a2 = 0.6):
    a1 = 1 - a2
    return (P_w * (1 - a1 * (v/v0) -  a2 * (v/v0)**2))
    
P_w = 140
v0 = 6.11   
v = np.arange(0, 7, 1)
B = 11.2
h = np.arange(0.1, 0.8, 0.1)
fig = plt.figure()
ax = fig.add_subplot()
col = np.array([0.1, 1, 1])

for i in h:
       col[0] += 0.1
       col[1] -= 0.1
       col[2] -= 0.1
       ax.plot(v, R_1(i, B, v, Geom) + R_2(i, B, v, Geom) + R_3(i, B, Geom), label = "Толщина льда " + str(round(i,2)) + " м", color = tuple(col))
       ax.plot(v, R_Zuev(i, B, v), linestyle = 'dashed', color = tuple(col), linewidth = 2)
       
                            
ax.plot(v, Thrust_line(P_w, v, v0), color = 'black')      
ax.set_xlabel('Скорость, м/c')
ax.set_ylabel('Сопротвление\nТяга, кН')
ax.set_xlim(0, 6)
ax.xaxis.set_major_locator(mtick.MultipleLocator(0.5))
#ax.yaxis.set_major_locator(mtick.MultipleLocator(20))
plt.grid()
ax.legend()
plt.show()