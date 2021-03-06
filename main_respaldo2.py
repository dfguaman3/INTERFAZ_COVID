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
        cases,deaths,tipo=[],[],[]
        paises = self.df['Country']
        estados = self.df['State']
        self.list_date=None
        self.pais=self.df.iloc[:, 0]
        self.country=self.pais[0]
        aux2=0
        valor = self.scrollbar.value()
        contagios2=[]
        
        for a in range(2,valor):
            
            for b in range(1,330):
                if self.country_selected==self.pais[b]:
                    aux2=b
            self.primera=self.df.iloc[:, a].values[aux2] # indice del pais 
            self.list_date = self.df.columns.tolist()
            casos=self.primera.split(sep=" ")
            contagios=[casos[0]]
            contagios=map(int,contagios)
            muertes=[casos[2]]
            cases+=contagios
            deaths+=muertes
            contagios2=list(map(lambda x: x // 1000, cases))
        
        segunda=self.df.iloc[:, 1] # Segunda columna
        ultima=self.df.iloc[:, -1] # Última columna
        for i in paises:
            self.listacountry.addItem(str(i))
            self.extrac_country=self.listacountry.currentItem()
        for j in estados:
            self.listastate.addItem(str(j))
          
        x_name = 'Contagios '
        y_name = 'Muertes'
        self.x = x_name
        self.y = y_name
    
        
        self.MplWidget.canvas.axes.clear()
        if self.casos.isChecked():
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],cases, width = 0.3, align='center')
        elif self.muertes.isChecked():
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],deaths, width = 0.3, align='center')
        elif self.ambos.isChecked():
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],cases, width = 0.3, align='center')
            self.MplWidget.canvas.axes.bar(self.list_date[2:valor],deaths, width = 0.3, align='center')
        self.MplWidget.canvas.axes.legend((self.x, self.y), loc='upper right')
        self.MplWidget.canvas.axes.set_title(f'{self.x} - {self.y} en '+self.country_selected)
        self.MplWidget.canvas.axes.set_xlabel('Fecha')
        self.MplWidget.canvas.axes.set_ylabel('Numero de casos(mil)')
        self.MplWidget.canvas.axes.grid(True)
        self.MplWidget.canvas.draw()

    def aux(self,extrac_country):
        self.country_selected=str(extrac_country.text())
        
        #print(self.country_selected)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
