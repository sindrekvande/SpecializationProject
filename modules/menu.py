import csv
import pandas as pd

inputFilePath = "/home/pi/Desktop/SpecializationProject/datasets/"
outputFilePath = "/home/pi/Desktop/SpecializationProject/measurements/"

inputFileDefault = 'tng00001_2020-09'
outputFileDefault = 'tng00001_2020-09_measurments'

headers = ['time', 'led_percent', 'SoCpacks', 'adc1.1', 'adc1.2', 'adc1.3', 'adc1.4', 'adc1.5', 'adc1.6', 'adc1.7', 'adc1.8', 'adc2.1', 'adc2.2', 'adc2.3', 'adc2.4', 'adc2.5', 'adc2.6', 'adc2.7', 'adc2.8']

class menu:
    def __inti__(self, args):
        if len(args) >= 2:
            self.inputFile = inputFilePath + args[0] + '.tsv'
            self.outputFile = outputFilePath + args[1] + '.tsv'
        elif len(args) >= 1:
            self.inputFile = inputFilePath + args[0] + '.tsv'
            self.outputFile = outputFilePath + args[0] + '_measurments.tsv'
        else:
            self.inputFile = inputFilePath + inputFileDefault + '.tsv'
            self.outputFile = outputFilePath + outputFileDefault + '.tsv'
        
        create_output_file()
        
    def create_output_file(self):
        file = open(self.outputFile, w)
        file.close()
        self.append_to_file(headers)

    def append_to_file(self, list):
        with open(self.outputFile, a) as file:
            csv.writer(file, delimiter='\t').writerow(item)
            file.close()
    
    def read_from_file(self):
        return pd.read_csv(self.inputFile, sep='\t', usecols = ['Gg_pyr'],  dtype = float) # header=0, index_col=False,