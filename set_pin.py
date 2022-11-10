#!/usr/bin/python3

import RPi.GPIO as GPIO
#from gpiozero import LED
from time import sleep
from os.path import exists
import pickle
import sys
from datetime import datetime

pin = int(sys.argv[1])
state = int(sys.argv[2])

stateFileName = "state_log"
stateFilePath = ""
stateFileFullPath = stateFilePath + stateFileName
logFileName = "usage_log.txt"
logFileFullPath = stateFilePath + logFileName

def file_test(pin):
  if exists(stateFilePath + stateFileName):
    #print("file exists")
    stateFile = open(stateFileFullPath, "rb")
    stateDict = pickle.load(stateFile)
    if pin_number_to_name(pin) not in stateDict:
      #print("pin already exists in dictionary")
    #else:
      stateDict[pin_number_to_name(pin)] = 0
      stateFile.close()
      stateFile = open(stateFileFullPath, "wb")
      pickle.dump(stateDict, stateFile)
      #print("pin did not exist but was written to file")
  else:
    #print("file doesn't exist")
    stateFile = open(stateFileFullPath, "wb")
    stateDict = {pin_number_to_name(pin): 0}
    pickle.dump(stateDict, stateFile)
  stateFile.close()
  return stateDict

def check_toggle(stateDict, pin, newState):
  if stateDict[pin_number_to_name(pin)] == newState:
    #print("no toggle")
    return 0
  if stateDict[pin_number_to_name(pin)] != newState:
    #print("will toggle!")
    return 1

def set_pin_state(stateDict, pin, state):
  #print("hello there")
  if check_toggle(stateDict, pin, state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    if state:
      GPIO.output(pin, True)
    else:
      GPIO.output(pin, False)
    stateDict[pin_number_to_name(pin)] = state
    stateFile = open(stateFileFullPath, "wb")
    pickle.dump(stateDict, stateFile)
    stateFile.close()
    #print("new state was set")
  #else:
    #print("no new state set")
  return stateDict

def pin_name_to_number(pinName):
  return int(pinName[3:4])

def pin_number_to_name(pin):
  return "Pin"+str(pin)

if __name__ == "__main__":
  #print("hello there")
  stateDict = file_test(pin)
  #print("The dictionary is:")
  #print(stateDict)
  #print("argument 1", pin)
  #print("argument 2", state)
  #print("Pin", pin_number_to_name(pin), "is now", stateDict[pin_number_to_name(pin)])

  GPIO.setwarnings(False)

  set_pin_state(stateDict, pin, state)
  #sleep(2)
  #set_pin_state(stateDict, pin, 0)

  logFile = open(logFileFullPath, "a")
  dt = datetime.now()
  str_date_time = dt.strftime("%d-%m-%Y, %H:%M:%S")
  logFile.write(str_date_time + " " + "Pin: " + str(pin) + " State: " + str(state) + "\n")
  logFile.close()

