import csv
import pandas as pd
#import import_main #LIGHT OFF
import parameters as pm
import messages as msg
from datetime import datetime

inputFilePath = "/home/pi/Desktop/SpecializationProject/datasets/"
outputFilePath = "/home/pi/Desktop/SpecializationProject/measurements/"

#inputFilePath = "C:/Users/kriss/Desktop/NTNU/SpecializationProject/datasets/"
#outputFilePath = "C:/Users/kriss/Desktop/NTNU/SpecializationProject/measurements/"

#headers = ['time','irradiance', 'led_percent', 'SoCpacks', 'adc1.1', 'adc1.2', 'adc1.3', 'adc1.4', 'adc1.5', 'adc1.6', 'adc1.7', 'adc1.8', 'adc2.1', 'adc2.2', 'adc2.3', 'adc2.4', 'adc2.5', 'adc2.6', 'adc2.7', 'adc2.8']

class file:
    def __init__(self):
        self.inputFile = inputFilePath + pm.season + ".tsv"

        self.read_from_file()
        self.filter_NaN_values()

        currentDatetime = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        strCurrentDatetime = str(currentDatetime)

        self.outputFile = outputFilePath + pm.season + "_measurements_" + strCurrentDatetime + ".tsv"
        
        self.create_output_file()
        
    def create_output_file(self):
        #file = open(self.outputFile, "w")
        #file.close()
        #self.append_to_file(headers)
        df = pd.DataFrame({ key:pd.Series(value) for key, value in msg.messages.items() })
        df.to_csv(self.outputFile, index=False, sep="\t")

    def append_to_file(self):#, df: pd.DataFrame):
        #with open(self.outputFile, "a") as file:
        #    csv.writer(file, delimiter='\t').writerow(list) 
        #    file.close()
        df = pd.DataFrame({ key:pd.Series(value) for key, value in msg.messages.items() })
        df.to_csv(self.outputFile, mode='a', index=False, header=False, sep="\t")
    
    def read_from_file(self):
        self.brightnessDF= pd.read_csv(self.inputFile, sep='\t', usecols = [pm.column],  dtype = float, nrows = (pm.numberOfDays*60*24)) # header=0, index_col=False,
        return self.brightnessDF

    def single_value(self, index):
        return self.brightnessDF.loc[index, pm.column]

    def filter_NaN_values(self):
        NaNCounter = 0
        #self.read_from_file(self.inputFile)

        for key, irrvalue in self.brightnessDF.itertuples():   
            if pd.isna(irrvalue) and NaNCounter == 0:
                previousValue = self.single_value(key - 1)
                #Check if next values are NaN
                for nextValueIndex in range(1, len(self.brightnessDF) - key):
                        NaNCounter += 1
                        nextValue = self.single_value(key + nextValueIndex)
                        if pd.notna(nextValue):
                            break
            if NaNCounter > 0:
                self.brightnessDF.loc[key, pm.column] = (previousValue + nextValue)/2
                NaNCounter -= 1
                    
        return self.brightnessDF