#!/usr/bin/python3

import RPi.GPIO as GPIO
#from gpiozero import LED
from time import sleep
from os.path import exists
import pickle
import sys

pin = int(sys.argv[1])
#state = int(sys.argv[2])

stateFileName = "state_log"
stateFilePath = ""
stateFileFullPath = stateFilePath + stateFileName

if __name__ == "__main__":
  #print("Printing file content:")
  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  print(int(stateDict["Pin"+str(pin)]))
  stateFile.close()
