import csv
import pandas as pd
import import_main
import parameters as pm
from datetime import datetime

inputFilePath = "/home/pi/Desktop/SpecializationProject/datasets/"
outputFilePath = "/home/pi/Desktop/SpecializationProject/measurements/"

headers = ['time','irradiance', 'led_percent', 'SoCpacks', 'adc1.1', 'adc1.2', 'adc1.3', 'adc1.4', 'adc1.5', 'adc1.6', 'adc1.7', 'adc1.8', 'adc2.1', 'adc2.2', 'adc2.3', 'adc2.4', 'adc2.5', 'adc2.6', 'adc2.7', 'adc2.8']

class file_handler:
    def __init__(self):
        self.inputFile = inputFilePath + pm.season + '.tsv'

        currentDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        strCurrentDatetime = str(currentDatetime)

        self.outputFile = outputFilePath + pm.season + '_measurements_' + strCurrentDatetime + '.tsv'
        
        self.create_output_file()
        
    def create_output_file(self):
        file = open(self.outputFile, "w")
        file.close()
        self.append_to_file(headers)

    def append_to_file(self, list):
        with open(self.outputFile, "a") as file: # df.to_csv(self.outputFile, mode='a', index=False, header=False)
            csv.writer(file, delimiter='\t').writerow(list) 
            file.close()
    
    def read_from_file(self):
        return pd.read_csv(self.inputFile, sep='\t', usecols = [pm.column],  dtype = float, nrows = (pm.numberOfDays*60*24)) # header=0, index_col=False,