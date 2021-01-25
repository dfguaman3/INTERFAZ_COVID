#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pandas as pd
import matplotlib.pyplot as plt

#Importar aquí las librerías a utilizar

from PyQt5 import uic, QtWidgets

qtCreatorFile = "interfaz.ui" #Aquí va el nombre de tu archivo

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        #Aquí van los botones
        self.lectura.clicked.connect(self.getCSV)
        self.graficar.clicked.connect(self.plot)
    #Aquí van las nuevas funciones
    #Esta función abre el archivo CSV    
    def getCSV(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './C:/Users/danny/Documents/GitHub/proyecto-final-b-KarolQuezada')
        if filePath != "":
            print ("Dirección",filePath) #Opcional imprimir la dirección del archivo
            self.df = pd.read_csv(str(filePath))
    def plot(self):
        x=self.df['1/22/20']
        y=self.df['1/23/20']
        plt.plot(x,y)
        plt.show()
        estad_st="Estadisticas 2:" +str(self.df['1/23/20'].describe())
        self.resultado.setText(estad_st)
    
    
  
if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()




