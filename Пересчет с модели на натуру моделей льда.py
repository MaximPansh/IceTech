# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 11:03:12 2020

@author: Кирилл
"""
from matplotlib import pyplot as plt
import numpy as np 
import matplotlib.ticker as mtick
from GP_ice import multylayer
from GP_ice import onelayer_h
import tkinter as tk # use tkinter for python 3
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#Словарь разрушающих нагрузок композитного льда, коэффициенты степенной функции
"""
dic = {'F':{20:{'ЦП':[3.134, 1.462], '1кан':[1.202*10**-31, 27.97], '2кан':[9.958*10**-12, 10.45], '3кан':[2.193*10**-20,-18.04]},
       10:{'ЦП':[1.638*10**-6, 8.508], '1кан':[5.208*10**-6, 7.626], '2кан':[3.967*10**-5, 6.473], '3кан':[0.0003909, 5.285]},
       3:{'ЦП':[5.263*10**-33, 29.35], '1кан':[1.31, 1.736], '2кан':[1.962, 1.429], '3кан':[0.8261, 1.954]}
           },
       'A1':{20:{'ЦП':[6.731*10**-48, 40.66], '1кан':[1.73*10**-35, 29.36], '2кан':[9.885*10**-20, 15.54], '3кан':[3.373*10**-20, 15.95]},
       10:{'ЦП':[5.445*10**-10, 10.17], '1кан':[2.099*10**-11, 11.37], '2кан':[7.696*10**-9, 8.155], '3кан':[4.797*10**-6, 5.034]},
       3:{'ЦП':[0.01674, 1.842], '1кан':[0.005819, 2.008], '2кан':[0.0059, 1.947], '3кан':[0.0008587, 3.119]}
           }
       }
"""

dic = {"1":{'F':{20:{'ЦП':[0.3314, 1.761], '1кан':[0.3524, 1.497], '2кан':[1.549, 0.8266], '3кан':[0.9811, 1.001]},
       10:{'ЦП':[3.912, 1.378], '1кан':[2.617, 1.199], '2кан':[3.027, 0.9463], '3кан':[4.485, 0.6963]},
       3:{'ЦП':[2.374, 1.736], '1кан':[2.052, 1.603], '2кан':[1.71, 1.61], '3кан':[0.9332, 1.922]}
           },
       'A1':{20:{'ЦП':[0.001135, 2.28], '1кан':[0.001524,1.714], '2кан':[0.006139, 1.131], '3кан':[0.006643, 1.085]},
       10:{'ЦП':[0.0218, 1.688], '1кан':[0.008373, 1.685], '2кан':[0.00832, 1.393], '3кан':[0.01913, 0.9639]},
       3:{'ЦП':[0.01458, 1.949], '1кан':[0.01079, 1.822], '2кан':[0.01157, 1.675], '3кан':[0.001156, 3.019]}
           }
       },
       "2":{'F':{
       10:{'ЦП':[3.395, 1.072], '1кан':[1.073, 1.418], '2кан':[0.1701, 2.227], '3кан':[2.808, 0.986]},
       3:{'ЦП':[0.09707, 3.38], '1кан':[0.6035, 1.963], '2кан':[0.1613, 2.587], '3кан':[]}
           },
       'A1':{
       10:{'ЦП':[0.0212, 1.347], '1кан':[0.0428, 0.8302], '2кан':[0.002732, 1.946], '3кан':[0.01489, 1.216]},
       3:{'ЦП':[0.01458, 1.949], '1кан':[0.0001051, 6.019], '2кан':[0.01157, 1.675], '3кан':[]}
           }
       },
       "3":{'F':{
       3:{'ЦП':[34.87, 0.5321], '1кан':[0.6495, 1.923], '2кан':[0.9545, 1.713], '3кан':[9.564, 0.752]}
           },
       'A1':{
       3:{'ЦП':[0.01046, 1.074], '1кан':[0.0982 * 10** -5, 3.605], '2кан':[0.001852, 2.313], '3кан':[0.0002064, 3.314]}
           }
       }
       }

"""
СЛОВАРИК С НОВОЙ ОБРАБОТКОЙ 20 ММ
"""
dic = {"1":{'F':{20:{'ЦП':[1.059, 1.1975], '1кан':[0.5975, 1.2964], '2кан':[0.9775, 1.0146], '3кан':[1.1818, 0.8848]},
       10:{'ЦП':[3.912, 1.378], '1кан':[2.617, 1.199], '2кан':[3.027, 0.9463], '3кан':[4.485, 0.6963]},
       3:{'ЦП':[2.374, 1.736], '1кан':[2.052, 1.603], '2кан':[1.71, 1.61], '3кан':[0.9332, 1.922]}
           },
       'A1':{20:{'ЦП':[0.0036, 1.3616], '1кан':[0.003,1.3695], '2кан':[0.004, 1.2511], '3кан':[0.0033, 1.3312]},
       10:{'ЦП':[0.0218, 1.688], '1кан':[0.008373, 1.685], '2кан':[0.00832, 1.393], '3кан':[0.01913, 0.9639]},
       3:{'ЦП':[0.01458, 1.949], '1кан':[0.01079, 1.822], '2кан':[0.01157, 1.675], '3кан':[0.001156, 3.019]}
           }
       },
       "2":{'F':{
       10:{'ЦП':[3.395, 1.072], '1кан':[1.073, 1.418], '2кан':[0.1701, 2.227], '3кан':[2.808, 0.986]},
       3:{'ЦП':[0.09707, 3.38], '1кан':[0.6035, 1.963], '2кан':[0.1613, 2.587], '3кан':[]}
           },
       'A1':{
       10:{'ЦП':[0.0212, 1.347], '1кан':[0.0428, 0.8302], '2кан':[0.002732, 1.946], '3кан':[0.01489, 1.216]},
       3:{'ЦП':[0.01458, 1.949], '1кан':[0.0001051, 6.019], '2кан':[0.01157, 1.675], '3кан':[]}
           }
       },
       "3":{'F':{
       3:{'ЦП':[34.87, 0.5321], '1кан':[0.6495, 1.923], '2кан':[0.9545, 1.713], '3кан':[9.564, 0.752]}
           },
       'A1':{
       3:{'ЦП':[0.01046, 1.074], '1кан':[0.0982 * 10** -5, 3.605], '2кан':[0.001852, 2.313], '3кан':[0.0002064, 3.314]}
           }
       }
       }


#Словарь разрушающих нагрузок натурного льда, коэффициенты степенной функции
dic_Nat = {"A1":{'ЦП':[0.02352, 2.5], '1кан':[0.001825, 2.778], '2кан':[0.001284, 2.807], '3кан':[0.8853, 2.894]},
           "F":{'ЦП':[2.786, 2], '1кан':[0.4731, 2.208], '2кан':[0.3475, 2.248], '3кан':[210.2, 1.082]}}


Gran = 20 # диаметр гранул
layer = "1"
left = 0
#словарь для 1 слоя:
#h_dic = {20:12, 10:8.5, 3:7} #Словарик максимальных толщин проморозки в серии опытов
h_dic = {20:12}
h_len = h_dic[Gran]
Type_array = ["ЦП", "1кан", "2кан", "3кан"]
A_switch_array = [True, False] # если False то считаем силу, если True - работу1

def F_array(X, k, p): 
   
    return k*X**p
    
def calculation(Type, Gran, A_switch, dic, line_width, line_style):
    global m
    global key_nat
    # выбор коэффициента m в зависимости от вида графиков
    
    if A_switch == True:
        m = 4
        key_nat = 'A1'
        print('1')
    else:
        m = 3 
        key_nat = 'F'
        print('2')
        
    h = np.arange(start=0, stop=h_len, step=0.1) #Задаю массив толщин проморозки льда

    h_model =[]
    h_new = []
    for i in h:
        #h_i = multylayer(i, Gran, 2) # переход от толщины проморозки к приведенной толщине
        h_i =onelayer_h(i,Gran)

        if h_i != None:
            h_new.append(i)
            h_model.append(h_i) # Массив приведенных толщин

    h_model = np.array(h_model)
    h = np.array(h_new) 
   # print(h_model)
   #print(h)
    
    Fm = F_array(h, dic[layer][key_nat][Gran][Type][0], dic[layer][key_nat][Gran][Type][1] ) # F модельная
    km = Fm/(pow(h_model, dic_Nat[key_nat][Type][1])) # коэффицент Fм
    Lam = (dic_Nat[key_nat][Type][0]/km) ** (1/(m-dic_Nat[key_nat][Type][1]))#коэффициент геометрического подобия
   # print(Lam)
    Hn = h_model*Lam #толщина натурного льда в пересчете с модельного
    # ax2.plot(h, Lam, label = key_nat + ' ' + str(Gran) + "мм " + Type, linewidth = line_width, c = "black", linestyle = line_style)
    # ax3.plot(h, Hn, label = key_nat + ' ' + str(Gran) + "мм " + Type, linewidth = line_width, c = "black", linestyle = line_style)
    ax2.plot(h, Lam, label = key_nat + ' ' + str(Gran) + "мм " + Type)
    ax3.plot(h, Hn, label = key_nat + ' ' + str(Gran) + "мм " + Type)
    ax2.plot([left, left],[0, 200], c = 'black', linewidth = 3)
    ax3.plot([left, left],[0, 2000], c = 'black', linewidth = 3)

fig = plt.figure(figsize=(width/100., height/100.)) 
fig.subplots_adjust(left=0.09,right=0.95, top= 0.97, bottom=0.2)
#Цвета графиков:
color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)
color3 = plt.cm.viridis(.9)

ax2 = fig.add_subplot(1, 2, 1)
plt.grid()
ax3 = fig.add_subplot(1, 2, 2)



#Названия осей:
ax2.set_xlabel('Толщина проморозки $h_{пром}$, мм', size = 20)
ax2.set_ylabel('Геометричесий масштаб λ', size = 20)

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))

ax2.xaxis.set_major_locator(mtick.MultipleLocator(1))
ax3.xaxis.set_major_locator(mtick.MultipleLocator(1))
ax3.tick_params(labelsize = 18)# размер текста толщина льда
ax2.tick_params(labelsize = 18)# размер текста лямбда
ax2.yaxis.set_major_locator(mtick.MultipleLocator(10))# цена деления лямбда
ax3.yaxis.set_major_locator(mtick.MultipleLocator(100))# цена деления толщины льда
#Пределы осей:
ax2.set_xlim(left, h_len)
ax3.set_xlim(left, h_len)
ax2.set_ylim(0, 200)#Лямбда
ax3.set_ylim(0, 1800)#толщина льда

#Названия осей:
ax3.set_xlabel('Толщина проморозки $h_{пром}$, мм', size = 20)
ax3.set_ylabel('Толщина натурного льда, мм', size = 20)

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))

l_w = 1.8
l_s = 0
lines = ['dashed', 'dashdot','solid', 'solid']

for i in A_switch_array:
    A_switch = i
    if i == False:
        l_s = 0
        l_w = 3.1
    for j in Type_array:
        Type = j
        calculation(Type, Gran, A_switch,dic, l_w, lines[l_s])
        l_s+=1
    
plt.grid()
ax3.legend(loc = 'lower center',
            mode = 'expand',
            borderaxespad = 18,
            prop={'size':16},
            bbox_to_anchor=(-1.9,-0.82,3.4,2),
            ncol = 22
            )
#np.savetxt(key_nat + ' ' + str(Gran) + "мм " + Type  +'.txt', np.column_stack((h, Lam, Hn)))
#figManager = plt.get_current_fig_manager()
#figManager.window.showMaximized()
#fig.savefig(key_nat + ' ' + str(Gran) + "мм " + Type +'.png', dpi = 300)
plt.rcParams.update({'font.size': 14})
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
plt.show()