#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
from os.path import exists
import pickle
import sys
from datetime import datetime
from read_pin import settings_exist, read_settings_file, generate_settings_file, write_settings_file


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

def raspi_gpio_control(settingsFileName="settings.ini", raspi_gpio_settings={"stateFileName": "state_log", "stateFilePath": "", "logFileName": "usage_log.txt", "logFilePath": ""}, pin=1, state=0):
  settingsFileFolderLevel = settings_exist(settingsFileName)
  if settingsFileFolderLevel == 0:
    generate_settings_file(settingsFileName, 1, raspi_gpio_settings)
    settingsFileFolderLevel = 1
  
  readSettingsContent = read_settings_file(settingsFileName, settingsFileFolderLevel)

  for x in raspi_gpio_settings:
    if x not in readSettingsContent:
      readSettingsContent[x] = raspi_gpio_settings[x]
      write_settings_file(settingsFileName, settingsFileFolderLevel, readSettingsContent)
  
  raspi_gpio_settings = read_settings_file(settingsFileName, settingsFileFolderLevel)
  stateFileFullPath = raspi_gpio_settings["stateFilePath"] + raspi_gpio_settings["stateFileName"]
  logFileFullPath = raspi_gpio_settings["logFilePath"] + raspi_gpio_settings["logFileName"]

  stateDict = file_test(stateFileFullPath, pin)
  GPIO.setwarnings(False)
  set_pin_state(stateFileFullPath, stateDict, pin, state)
  logFile = open(logFileFullPath, "a")
  dt = datetime.now()
  str_date_time = dt.strftime("%d-%m-%Y, %H:%M:%S")
  logFile.write(str_date_time + " " + "Pin: " + str(pin) + " State: " + str(state) + "\n")
  logFile.close()


if __name__ == "__main__":
  raspi_gpio_control(pin=int(sys.argv[1]), state=int(sys.argv[2]))
