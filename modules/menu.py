import csv
import pandas as pd
from tests import import_path
import parameters as pm

inputFilePath = "/home/pi/Desktop/SpecializationProject/datasets/"
outputFilePath = "/home/pi/Desktop/SpecializationProject/measurements/"

headers = ['time','irradiance', 'led_percent', 'SoCpacks', 'adc1.1', 'adc1.2', 'adc1.3', 'adc1.4', 'adc1.5', 'adc1.6', 'adc1.7', 'adc1.8', 'adc2.1', 'adc2.2', 'adc2.3', 'adc2.4', 'adc2.5', 'adc2.6', 'adc2.7', 'adc2.8']

class menu:
    def __init__(self):
        self.inputFile = inputFilePath + pm.season + '.tsv'
        self.outputFile = outputFilePath + pm.season + '_measurements' + '.tsv'
        
        self.create_output_file()
        
    def create_output_file(self):
        file = open(self.outputFile, w)
        file.close()
        self.append_to_file(headers)

    def append_to_file(self, list):
        with open(self.outputFile, a) as file: # df.to_csv(self.outputFile, mode='a', index=False, header=False)
            csv.writer(file, delimiter='\t').writerow(item) 
            file.close()
    
    def read_from_file(self):
        return pd.read_csv(self.inputFile, sep='\t', usecols = [pm.column],  dtype = float, nrows = (pm.numberOfDays*60*24)) # header=0, index_col=False,