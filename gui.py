import numpy as np
import sys
from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QVBoxLayout,QHBoxLayout,QMainWindow,QPushButton,QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import pyqtgraph as pg
import csv
from datetime import datetime

class spectometerGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spectrometer Testing")
        self.resize (1000,700)
        self.setStyleSheet("background-color: #2b2b2b;")

        #Create the initial layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        mainLayout = QHBoxLayout(central_widget)
        
        
        #Left vertical layout
        leftLayout = QVBoxLayout()
        mainLayout.addLayout(leftLayout, 2)
        mainLayout.addSpacing(30)
    

        #Right hand vertical layout
        rightLayout = QVBoxLayout()
        rightLayout.setContentsMargins(0,0,50,0)
        mainLayout.addLayout(rightLayout,1)
        
        #Test Panel row - Top left
        testLayout = QHBoxLayout()
        label = QLabel("Test Name:")  
        font = QFont("Cambria", 20)    
        label.setFont(font)
        label.setStyleSheet("color: white")
        self.testName = QLineEdit()
        self.testName.setStyleSheet("background-color: white")
        self.testName.setMinimumWidth(300)
        testLayout.setContentsMargins (25,40,0,0)
        testLayout.addWidget(label)
        testLayout.addWidget(self.testName)
        testLayout.addStretch()
        leftLayout.addLayout(testLayout)
       

        #Graph 1
        self.plotGraph1 = pg.PlotWidget()
        self.wavelength = [0,10,20,30]
        self.absorption = [0,10,5,30]
        self.targetAbsoprtion = [0,20,40,60]
        pen1 = pg.mkPen(color=(255, 0, 0), width=2) 
        pen2 = pg.mkPen(color=(0, 0, 255), width=2) 
        self.plotGraph1.addLegend()
        self.plotGraph1.plot(self.wavelength, self.absorption,pen=pen1, symbol ="o", symbolSize=7, symbolBrush ="w", name="wavelength")
        self.plotGraph1.plot(self.wavelength, self.targetAbsoprtion,pen=pen2, symbol ="o", symbolSize=7, symbolBrush ="w", name="Target wavelength")
        self.plotGraph1.setTitle("Spectral Profile", color ="w", size="20pt")
        styles = {"color": "white", "font-size": "18px"}
        self.plotGraph1.setLabel("left", "Absorbance",**styles)
        self.plotGraph1.setLabel("bottom", "Wavelength (nm)",**styles)
        self.plotGraph1.showGrid(x=True,y=True)
    

        leftLayout.addWidget(self.plotGraph1)       


        #Start button
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet("background-color: white")
        buttonFont = QFont("Arial Black", 20)
        self.startButton.setFont(buttonFont)
        self.startButton.setMinimumSize(200,50)
        rightLayout.addSpacing(25)
        rightLayout.addWidget(self.startButton)
        rightLayout.addStretch()
        

        #Target - wavelength
        waveLayout = QVBoxLayout()  
        wavelengthLabel = QLabel("Target wavelength")
        wavelengthLabel.setStyleSheet("color: white")
        font = QFont("Cambria", 20) 
        wavelengthLabel.setFont(font)
        self.target = QLineEdit()
        self.target.setStyleSheet("background-color: white")
        self.target.setFixedSize(200,50)
        waveLayout.addWidget(wavelengthLabel)
        waveLayout.addWidget(self.target)
        rightLayout.addSpacing(200)
        rightLayout.addLayout(waveLayout)
        rightLayout.addStretch()
       

        #File dialog
        self.saveButton = QPushButton("Save")
        self.saveButton.setStyleSheet("background-color: white")
        self.saveButton.setFont(buttonFont)
        self.saveButton.setMinimumSize(200,50)
        self.saveButton.clicked.connect(self.saveFile)
        rightLayout.addWidget(self.saveButton)

        rightLayout.addStretch()

    
    def saveFile(self): #CSV save
        name = self.testName.text()
        date = datetime.now().strftime("%Y-%m-%d")
        defaultName = f"{name}.{date}.csv"

        filePath, _ = QFileDialog.getSaveFileName(self,"Save Test",defaultName,"CSV file (*.csv)")
        if not filePath:
            return

        with open(filePath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Frequency", "Absorbance"])
            for x, y in zip(self.wavelength, self.absorption):
                writer.writerow([x, y])
       





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = spectometerGui()
    window.show()
    app.exec()