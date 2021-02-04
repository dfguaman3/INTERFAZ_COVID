from numpy.lib.shape_base import split
import requests,json,urllib.request, datetime, sys
import pandas as pd
from PyQt5 import uic, QtWidgets
#from PyQt5.QtGui import QListWidget, QListWidgetItem, QApplication
from mplwidget import MplWidget
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
url='https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.json'
qtCreatorFile = "interfaz.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.MplWidget = MplWidget(self.MplWidget)
        self.cargar.clicked.connect(self.getCSV)
        #self.graficar.clicked.connect(self.aux)
        self.listacountry.itemClicked.connect(self.aux)
        self.df = pd.read_csv('./data/covid_data2.csv', parse_dates=['Country'], sep=',', na_values='')
        #self.df2 = pd.read_csv('./frankfurt_weather.csv', parse_dates=['time'], index_col='time', sep=',', na_values='')
        #print(self.df['1/26/2020'].values['Australia'])
        datos=pd.DataFrame(self.df, columns= ['Country','1/22/2020'])
            
    def getCSV(self):
        
        paises = self.df['Country']
        estados = self.df['State']
        dias=self.df.columns.tolist()
        self.fechas = self.df.loc['1/22/2020':'2/5/2020']
        self.fechas2 = self.fechas.columns.tolist()
        '''
        valores=self.fechas.values[6]#indice para el pais
        casos=valores[7].split(sep=" ")#indice para la fecha
        contagios=casos[0]
        muertes=casos[2]
        pais=valores[0]
        cases=[]
        cases+=contagios
        deaths=[]
        deaths+=muertes
        print("contagios en "+ str(pais)+": "+str(contagios))
        print("Muertes en "+ str(pais)+": "+str(muertes))
        
        '''
        
        for i in paises:
            self.listacountry.addItem(str(i))
            extrac_country=self.listacountry.currentItem()
            
        for j in estados:
            self.listastate.addItem(str(j))
        cases=[]
        deaths=[]
        
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

        for k in range(2,20):
            valores=self.fechas.values[6]
            casos=valores[k].split(sep=" ")
            contagios=[casos[0]]
            muertes=[casos[2]]
            pais=valores[0]
            
            cases+=contagios
            
            deaths+=muertes
            #print("contagios en "+ str(pais)+": "+str(contagios))
            #print("Muertes en "+ str(pais)+": "+str(muertes))
        print(cases)
        print(deaths)    
        #print(len(casos))377 columnas
        self.lon = range(1,len(dias)+1)
        
        #separado = dataset["Hora Creacion"].str.split(" ", n=1, expand=True)

        
        #fechas.groupby('Country')[col_names[2]].sum().plot(kin='bar',legend='Reverse')
        
           
        x_name = 'Daily Number of Cases and Deaths in '
        y_name = 'Date'
        z_name = 'Tiempo'
        self.x = x_name
        self.y = y_name
        self.z = z_name
        
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.bar(list(self.fechas2[2:20]),cases, width = 1, align='center')
        self.MplWidget.canvas.axes.legend((self.x, self.y), loc='upper right')
        self.MplWidget.canvas.axes.set_title(f'{self.x} - {self.y}')
        self.MplWidget.canvas.axes.set_xlabel('Fecha')
        self.MplWidget.canvas.axes.set_ylabel('Numero de casos')
        self.MplWidget.canvas.axes.grid(True)
        self.MplWidget.canvas.draw()
    def aux(self,extrac_country):
        print(extrac_country, str(extrac_country.text()))
    '''def presentarTabla(self):
        
        try:
            x_name = 'Daily Number of Cases and Deaths in Place'
            y_name = 'Date'
            z_name = 'Tiempo'
            self.x = x_name
            self.y = y_name
            self.z = z_name
            lista_mag = []
            lista_place =[]
            lista_time = []
            response = urllib.request.urlopen(url).read().decode()
            data = json.loads(response)
            long = len(data['data'])
            for i in range(long): 
                mag = data['data'][i]['date']['mag']#float
                place = data['data'][i]['total_cases']['place']#string
                lista_mag += [mag]
                lista_place += [place]
            
            self.lon = range(1,len(lista_mag)+1)
            self.MplWidget.canvas.axes.clear()
            self.MplWidget.canvas.axes.bar(list(self.lon),lista_mag, width = 0.4, align='center')
            self.MplWidget.canvas.axes.legend((self.x, self.y), loc='upper right')
            self.MplWidget.canvas.axes.set_title(f'{self.x} - {self.y}')
            self.MplWidget.canvas.axes.set_xlabel('Numero de sismos')
            self.MplWidget.canvas.axes.set_ylabel('Magnitud (Ritcher Scale)')
            self.MplWidget.canvas.axes.grid(True)
            self.MplWidget.canvas.draw()
        except Exception as e:
            print(e)     '''
            

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
