import numpy as np
import sys
from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QVBoxLayout,QHBoxLayout,QMainWindow,QPushButton,QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import pyqtgraph as pg
import csv
from datetime import datetime
import spectrometer

class spectrometerGui(QMainWindow):
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
    

        #Right vertical layout
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
        self.wavelength = []
        self.brightness = []
        pen1 = pg.mkPen(color=(255, 0, 0), width=2) 
        pen2 = pg.mkPen(color=(0, 0, 255), width=2) 
        self.plotGraph1.addLegend()
        self.plotGraph1.setTitle("Spectral Profile", color ="w", size="20pt")
        styles = {"color": "white", "font-size": "18px"}
        self.plotGraph1.setLabel("left", "Brightness",**styles)
        self.plotGraph1.setLabel("bottom", "Wavelength (nm)",**styles)
        self.plotGraph1.showGrid(x=True,y=True)
        leftLayout.addWidget(self.plotGraph1)       

        #Plotting live graph
        self.line = self.plotGraph1.plot(
            self.wavelength,
            self.brightness,
            name = "Spectrometer data",
            pen = pen1,
            )



        #Start button
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet("background-color: white")
        buttonFont = QFont("Arial Black", 20)
        self.startButton.setFont(buttonFont)
        self.startButton.setMinimumSize(200,50)
        self.startButton.clicked.connect(self.startData)
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
       

        #File dialog - save button
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
            for x, y in zip(self.wavelength, self.brightness):
                writer.writerow([x, y])
    
    def startData(self):
        print("Clicked!")
        try:
            spectrometer.start()
            spectrum = spectrometer.read_spectrum()
        
            print(spectrum.shape)                 # should be 1440
            peak = np.argmax(spectrum)            # brightest column 
            peak_nm = 0.234 * peak + 400.0        # column to wavelength in nm 

            #Save the data so other methods (likesaveFile) can use it
            self.brightness = spectrometer.read_spectrum()  #y-axis
            self.wavelength = 0.234 * np.arange(1440) + 400.0 #creates range up to 1440  #x-axis
            print(f"peak: {peak_nm:.1f} nm (column {peak})")

            self.line.setData(self.wavelength,self.brightness) #Plots data to the graph

        except Exception as e: #The app keep running even after the error
            print("Spectrometer error:", e)
        finally:
            spectrometer.stop()   # always runs even after an error

    
    
        
#graph brightness and wavelength.

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = spectrometerGui()
    window.show()
    app.exec()