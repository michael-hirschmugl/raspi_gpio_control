#!/usr/bin/python

import RPi.GPIO as GPIO
from os.path import exists
import pickle


def file_test(stateFileFullPath, pin):
  if exists(stateFileFullPath):
    stateFile = open(stateFileFullPath, "rb")
    stateDict = pickle.load(stateFile)
    if pin_number_to_name(pin) not in stateDict:
      stateDict[pin_number_to_name(pin)] = 0
      stateFile.close()
      stateFile = open(stateFileFullPath, "wb")
      pickle.dump(stateDict, stateFile)
  else:
    stateFile = open(stateFileFullPath, "wb")
    stateDict = {pin_number_to_name(pin): 0}
    pickle.dump(stateDict, stateFile)
  stateFile.close()
  return stateDict

def check_toggle(stateDict, pin, newState):
  if stateDict[pin_number_to_name(pin)] == newState:
    return 0
  if stateDict[pin_number_to_name(pin)] != newState:
    return 1

def set_pin_state(stateFileFullPath, stateDict, pin, state):
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
  return stateDict

def pin_name_to_number(pinName):
  return int(pinName[3:4])

def pin_number_to_name(pin):
  return "Pin"+str(pin)

if __name__ == "__main__":
  print("This file is not intended to be called as main. sorry...")