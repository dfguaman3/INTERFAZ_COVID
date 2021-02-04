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
        self.listacountry.itemClicked.connect(self.getCSV)
        self.scrollbar.tickInterval()
        self.df = pd.read_csv('./data/covid_data2.csv', parse_dates=['Country'], sep=',', na_values='')
        
        self.country_selected=''
        
    def interval(self):
        self.inter=15
        return self.inter
    def getCSV(self):
        cases,deaths,tipo=[],[],[]
        
        paises = self.df['Country']
        estados = self.df['State']
        
        self.list_date=None
        self.pais=self.df.iloc[:, 0]
        self.country=self.pais[0]
        aux2=0
        for a in range(2,100):
            
            for b in range(1,330):
                if self.country_selected==self.pais[b]:
                    aux2=b
                    

            self.primera=self.df.iloc[:, a].values[aux2] # indice del pais 
            self.list_date = self.df.columns.tolist()
            casos=self.primera.split(sep=" ")
            contagios=[casos[0]]
            muertes=[casos[2]]
            cases+=contagios
            deaths+=muertes
        segunda=self.df.iloc[:, 1] # Segunda columna
        ultima=self.df.iloc[:, -1] # Última columna
        #print(ultima.values[265])
        for i in paises:
            self.listacountry.addItem(str(i))
            self.extrac_country=self.listacountry.currentItem()
        for j in estados:
            self.listastate.addItem(str(j))
          
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
        self.MplWidget.canvas.axes.bar(self.list_date[2:100],tipo, width = 0.2, align='center')
        self.MplWidget.canvas.axes.legend((self.x, self.y), loc='upper right')
        self.MplWidget.canvas.axes.set_title(f'{self.x} - {self.y}')
        self.MplWidget.canvas.axes.set_xlabel('Fecha')
        self.MplWidget.canvas.axes.set_ylabel('Numero de casos')
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
