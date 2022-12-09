#!/usr/bin/python3

import RPi.GPIO as GPIO
#from gpiozero import LED
from time import sleep
from os.path import exists
import pickle
import sys

#pin = int(sys.argv[1])
#state = int(sys.argv[2])

stateFileName = "state_log"
stateFilePath = ""
stateFileFullPath = stateFilePath + stateFileName

def raspi_gpio_read_pin(pin):
  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  #print(int(stateDict["Pin"+str(pin)]))
  stateFile.close()
  return int(stateDict["Pin"+str(pin)])

def raspi_gpio_print_pin(pin):
  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  print(int(stateDict["Pin"+str(pin)]))
  stateFile.close()

if __name__ == "__main__":
  #print("Printing file content:")
  #stateFile = open(stateFileFullPath, "rb")
  #stateDict = pickle.load(stateFile)
  #print(int(stateDict["Pin"+str(pin)]))
  #stateFile.close()
  raspi_gpio_print_pin(int(sys.argv[1]))
