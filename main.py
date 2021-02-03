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
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.MplWidget = MplWidget(self.MplWidget)
        self.cargar.clicked.connect(self.getCSV)
        self.casos.setChecked(True)
        self.listacountry.itemClicked.connect(self.aux)
        self.df = pd.read_csv('./data/covid_data2.csv', parse_dates=['Country'], sep=',', na_values='')
        self.country_selected=''
           
    def getCSV(self):
        cases=[]
        deaths=[]
        tipo=[]
        paises = self.df['Country']
        estados = self.df['State']
        dias=self.df.columns.tolist()
        self.fechas = self.df.loc['1/22/2020':'2/5/2020']
        self.fechas2 = self.fechas.columns.tolist()
        print(self.fechas.values[0][0])
        print(len(self.fechas))
        for i in paises:
            self.listacountry.addItem(str(i))
            self.extrac_country=self.listacountry.currentItem()
            self.index_country=self.listacountry.currentRow()
            
        for j in estados:
            self.listastate.addItem(str(j))
        '''
        for l in range(2,len(self.fechas)):
            if str(self.country_selected)==str(self.fechas.values[0][0]):
                valores=self.fechas.values[l]
                for k in range(2,15):
                    casos=valores[k].split(sep=" ")
                    contagios=[casos[0]]
                    muertes=[casos[2]]
                    pais=valores[0]
                    cases+=contagios
                    deaths+=muertes
            
        '''
        for k in range(2,15):
            valores=self.fechas.values[10]#Australia
            casos=valores[k].split(sep=" ")
            contagios=[casos[0]]
            muertes=[casos[2]]
            pais=valores[0]
            cases+=contagios
            deaths+=muertes
            
        print(cases)
        print(deaths)
        
        self.lon = range(1,len(dias)+1)
        
        x_name = 'Daily Number of Cases and Deaths in '
        y_name = 'Date'
        z_name = 'Tiempo'
        self.x = x_name
        self.y = y_name
        
        if self.casos.isChecked():
            tipo=cases
        elif self.muertes.isChecked():
            tipo=deaths
            
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.bar(list(self.fechas2[2:15]),tipo, width = 0.2, align='center')
        self.MplWidget.canvas.axes.legend((self.x, self.y), loc='upper right')
        self.MplWidget.canvas.axes.set_title(f'{self.x} - {self.y}')
        self.MplWidget.canvas.axes.set_xlabel('Fecha')
        self.MplWidget.canvas.axes.set_ylabel('Numero de casos')
        self.MplWidget.canvas.axes.grid(True)
        self.MplWidget.canvas.draw()

    def aux(self,extrac_country):
        self.country_selected=str(extrac_country.text())
        
        print(self.country_selected)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
