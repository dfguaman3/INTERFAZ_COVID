from numpy.lib.shape_base import split
import requests,json,urllib.request, datetime, sys
import pandas as pd
from PyQt5 import uic, QtWidgets
from mplwidget import MplWidget
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
qtCreatorFile = "interfaz.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):#Clase principal que contendra las funciones para los eventos que ocurriran en la interfaz
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.MplWidget = MplWidget(self.MplWidget)
        self.cargar.clicked.connect(self.getCSV)#evento para el boton de cargar datos usando la funcion getCSV
        self.casos.setChecked(True)#por defecto inicia marcado el check de casos
        self.listacountry.itemClicked.connect(self.aux)#evento del Slider para extraer el pais y usarlo en otro evento para graficar datos
        self.listacountry.itemClicked.connect(self.getCSV)
        self.scrollbar.setMinimum(5)#se define el valor minimo, maximo y los intervalos para el slider
        self.scrollbar.setMaximum(375)#375 corresponde al valor de la ultima columna del archivo csv
        self.scrollbar.setSingleStep(25)
        self.scrollbar.setTickInterval(25)
        self.df = pd.read_csv('./data/covid_data2.csv', parse_dates=['Country'], sep=',', na_values='')#lee el archivo csv y generar un dataframe
        self.country_selected=''
    def getCSV(self):
        cases,deaths,tipo=[],[],[]#creamos listas vacias para ir insertando los valores de casos y muertes
        paises = self.df['Country']#extraemos los paises de la columna Country
        estados = self.df['State']#extraemos los estados de la columna State
        self.list_date=None
        self.pais=self.df.iloc[:, 0]
        aux2=0
        valor = self.scrollbar.value()
        for a in range(2,valor):#ciclo for para seleccionar el rango de visualizacion usando la variable valor
            
            for b in range(1,330):#cicllo for para recorrer las filas las que corresponden a  los paises
                if self.country_selected==self.pais[b]:#compara si el pais seleccionado es igual al pais de la fila correspondiente
                    aux2=b
            self.primera=self.df.iloc[:, a].values[aux2] #luego de obtener el indice del pais seleccionado se extraen los valores de casos y muertes 
            self.list_date = self.df.columns.tolist()#convierte las columnas de las fechas a una lista para colocar en el eje x de la grafica
            casos=self.primera.split(sep=" ")#separa los valores contenidos en las celdas, los cuales estan separados por espacios
            contagios=[casos[0]]#luego de extraerlos a una lista se extrae el valor del indice 0 correspondiente a los casos
            contagios=map(int,contagios)#utilizamos la funcion map para convertir los valores a enteros y mostrar las cantidades en miles o millones
            muertes=[casos[-1]]#extrae el valor correspondiente al numero de muertes ubicado en el ultimo indice de la lista
            cases+=contagios#cada valor se va almacenando en la lista correspondiente
            deaths+=muertes#aplica el mismo procedimiento en la linea anterior pero con los valores de el numero de muertes
        for i in paises:#ciclo for para ir agregando los paises extraidos en la QlistWidget
            self.listacountry.addItem(str(i))#agrega los paises uno auno en la listwidget
            self.extrac_country=self.listacountry.currentItem()
        for j in estados:#agrega los estado en la otra listwidget
            self.listastate.addItem(str(j))
        self.x = 'Contagios '#variables para colocar leyendas en la grafica
        self.y = 'Muertes'
        self.MplWidget.canvas.axes.clear()#limpia la grafica antes de cargar los datos
        if self.casos.isChecked():#condicion if para comprobar si se marca el check de casos
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],cases, width = 0.3, align='center')#muestra los casos en la grafica correspondiente
        elif self.muertes.isChecked():
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],deaths, width = 0.3, align='center')#muestra las muertes en la grafica correspondiente
        elif self.ambos.isChecked():#condicion if si decide mostrar ambos casos de mcontagios y muertes
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],cases, width = 0.3, align='center')#genera una grafica tipo barra con los casos y demas parametros
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],deaths, width = 0.3, align='center')#genera una grafica tipo barra con las muertes y demas parametros
        self.MplWidget.canvas.axes.legend((self.x, self.y), loc='upper right')
        self.MplWidget.canvas.axes.set_title(f'{self.x} - {self.y} en '+self.country_selected)
        self.MplWidget.canvas.axes.set_xlabel('Fecha')
        self.MplWidget.canvas.axes.set_ylabel('Numero de casos')
        self.MplWidget.canvas.axes.grid(True)
        self.MplWidget.canvas.draw()
    def aux(self,extrac_country):#funcion para extraer el pais de la QListWidget 
        self.country_selected=str(extrac_country.text())
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())