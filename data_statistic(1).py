# -*- coding: utf-8 -*-

"""
Статистическая обработка результатов экспериментов по разрушению льда
"""

from matplotlib import pyplot as plt
import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd
import numpy as np  # noqa:F401
import tkinter as tk # use tkinter for python 3
from GP_ice import multylayer
import matplotlib.ticker as mtick
import math
from tkinter.filedialog import askopenfilename
root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

filename = askopenfilename()

def open_datafile(path):
    """
    Открыть файл с данными диаграммы разрушения
    Запрашивает: путь к файлу(строковый тип)
    Возвращает массив из 2-х столбцов: {x;y}
    """
    file= open(path,encoding= 'ansi')#перекодировка из utf-8 в ansi из за странной ошибки в спайдере
    data=pd.read_csv(file,sep='\s+', decimal=",")    #Читаю из тестового документа в качестве сепаратора: все пробелы
    #у переменной data сейчас тип dataframe
    file.close()
    return data

data=open_datafile(filename)  #открываем файл с данными
#filename ='A1 ' + filename.split(' ')[1] + ' ' + filename.split(' ')[-1].split('.')[0]

#data.h*=10
#data.F*=1000

"""

УБРАТЬ ЕСЛИ НЕ 3 ММ


"""
from math import pi
ro_b=0.919
ro_w=1
R=3/2 #Радиус шарика
S=pow(3,0.5)*pow(R,2)   #Площадь элементарного треугольника разбивки поля льда
V_b=(4/3)*pi*pow(R,3)    #Объём шарика
V_upseg=V_b*(1-ro_b/ro_w)   #Объём шарового сегмента, торчащего над поверхностью воды
   #Расчёт высоты, на которую шарик торчит из воды:
A=pow(((2*ro_b+2j*pow(ro_b*(ro_w-ro_b),0.5))/ro_w)-1,1/3)
h_upseg=((2-1j*pow(3,0.5)*(A-pow(A,-1))-(A+pow(A,-1)))/2).real*R
"""
УБРАТЬ ЕСЛИ НЕ 3 ММ

"""
datah = np.array(data.h)
print(datah)
data_h_new = []
for i in datah:
    data_h_new.append(i- h_upseg)
data.h_p = pd.Series(data_h_new)
print(data_h_new)
data.F = data.A1
h_max=data.h_p.loc[data.h_p.idxmax()]   #максимальная толщина льда в датафрейме

data_line=pd.DataFrame({'ln_h':np.log(data.h_p), 'ln_y':np.log(data.F)}) #Линеаризация даных, ложащихся на степенную зависимость

print('\nНачинаем поиск грубых промахов')
index = True
i = 0
del_index=np.array([])
while index:
    i+=1
    print('\nПриближение № %g\n\nВнешние стьюдентизированные остатки:' % i)
    model=smf.ols(formula="ln_y~ln_h",data=data_line) #задаём модель
    results=model.fit() #получаем результаты регрессионной модели
    influence=results.get_influence() #Оценка на грубые промахи
    r_stud=sm.regression.linear_model.OLSResults.outlier_test(results) #Внешние стьюдентизированные остатки
    print(r_stud)
    index=r_stud.index[r_stud.student_resid.abs()>3].tolist() #Ищем остатки, большие 2 по модулю
    data_line.drop(index, inplace=True) #Удаляем точки из расчёта, если внешний стьюдентизированный остаток больше 2
    print('Удаляем строки:', index)
    del_index=np.append(del_index, index)

fig = plt.figure(figsize=(width/90., height/90.))
ax1 = fig.add_subplot()

if del_index.size==0:
    print("Грубые промахи отсутствуют")
    fig.text(0.40, 0.10, 'Грубые промахи отсутствуют', fontproperties = 'monospace', size = 8)
else:
    print('\nГрубые промахи:\n', data.iloc[del_index])
    fig.text(0.40, 0.10, 'Грубые промахи:\n'+str(data.iloc[del_index]), fontproperties = 'monospace', size = 8)

print(results.summary())
print(results.params)

x=np.arange(start=0,stop=h_max+0.025*h_max,step=0.001).reshape((-1,1)) #задаём массив для построения регрессионной зависимости
x=np.log(x)
x=(np.column_stack((np.ones(np.size(x)),x))) #добавляем колонку единиц, т.к. уравнение регрессии со свободным членом
y=model.predict(exog=x,params=results.params)

#Статистические параметры оценки регрессии из метода summary:
fig.subplots_adjust(left=0.08,right=0.95, top= 0.97, bottom=0.4)
fig.text(0.05, 0.032, str(results.summary()), fontproperties = 'monospace', size = 8)

#Цвета графиков:
color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)
color3 = plt.cm.viridis(.9)

#Пределы осей:
ax1.set_xlim(0, data.h_p.max()*1.1)
ax1.set_ylim(0, data.F.max()*1.1)

#Названия осей:
ax1.set_xlabel('Толщина льда $h_{л}$, мм')
ax1.set_ylabel('Критическая работа разрушения $A_{1}$, Дж')
#ax1.set_ylabel('Максимальная сила $F_{max}$, Н')

#Добавляем промежуточные деления осей
plt.gca().xaxis.set_minor_locator(mtick.MultipleLocator(50))
plt.gca().yaxis.set_minor_locator(mtick.MultipleLocator(25))

#Формат чисел осей
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('$%.4g$'))
plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('$%.3g$'))


#Рисуем графики
points=ax1.scatter(data.h_p, data.F, color=color1, marker='o')
regres=ax1.plot(np.exp(x[:,1]),np.exp(y))

#Легенда:
ax1.legend((points, regres), labels=(r'$A_{1} = %.4g \cdot h_{л}^{%.4g}$, $R^2=%.3g$' % (math.exp(results.params.Intercept), results.params.ln_h, results.rsquared), 'Экспериментальные точки'), loc='upper left')
#открываем график в полный экран
figManager = plt.get_current_fig_manager()
figManager.window.showMaximized()
fig.savefig(filename.split(".")[0]+".png", dpi = 300)
#data.to_csv(filename + ' ' + '.txt', sep=' ', decimal=",")

plt.show()
input()