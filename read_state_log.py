#!/usr/bin/python3

import RPi.GPIO as GPIO
#from gpiozero import LED
from time import sleep
from os.path import exists
import pickle
import sys
from read_pin import settings_exist, read_settings_file, generate_settings_file, write_settings_file

#pin = int(sys.argv[1])
#state = int(sys.argv[2])

#stateFileName = "state_log"
#stateFilePath = ""
#stateFileFullPath = stateFilePath + stateFileName

def raspi_gio_read_state_log(settingsFileName="settings.ini", raspi_gpio_settings={"stateFileName": "state_log", "stateFilePath": ""}):
  settingsFileFolderLevel = settings_exist(settingsFileName)
  if settingsFileFolderLevel == 0:
    generate_settings_file(settingsFileName, 1, raspi_gpio_settings)
    settingsFileFolderLevel = 1
  
  readSettingsContent = read_settings_file(settingsFileName, settingsFileFolderLevel)

  #print(raspi_gpio_settings)

  for x in raspi_gpio_settings:
    if x not in readSettingsContent:
      readSettingsContent[x] = raspi_gpio_settings[x]
      write_settings_file(settingsFileName, settingsFileFolderLevel, readSettingsContent)
  
  raspi_gpio_settings = read_settings_file(settingsFileName, settingsFileFolderLevel)
  stateFileFullPath = raspi_gpio_settings["stateFilePath"] + raspi_gpio_settings["stateFileName"]
  #print("Printing file content:")
  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  #print(stateDict)
  stateFile.close()
  return stateDict

def raspi_gio_print_state_log(settingsFileName="settings.ini", raspi_gpio_settings={"stateFileName": "state_log", "stateFilePath": ""}):
  settingsFileFolderLevel = settings_exist(settingsFileName)
  if settingsFileFolderLevel == 0:
    generate_settings_file(settingsFileName, 1, raspi_gpio_settings)
    settingsFileFolderLevel = 1
  
  readSettingsContent = read_settings_file(settingsFileName, settingsFileFolderLevel)

  #print(raspi_gpio_settings)

  for x in raspi_gpio_settings:
    if x not in readSettingsContent:
      readSettingsContent[x] = raspi_gpio_settings[x]
      write_settings_file(settingsFileName, settingsFileFolderLevel, readSettingsContent)
  
  raspi_gpio_settings = read_settings_file(settingsFileName, settingsFileFolderLevel)
  stateFileFullPath = raspi_gpio_settings["stateFilePath"] + raspi_gpio_settings["stateFileName"]
  print("Printing file content:")
  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  print(stateDict)
  stateFile.close()

if __name__ == "__main__":
  #settingsFileName = "settings.ini"
  #raspi_gpio_settings = {"stateFileName": "state_log", "stateFilePath": ""}
  #print("Printing file content:")
  #stateFile = open(stateFileFullPath, "rb")
  #stateDict = pickle.load(stateFile)
  #print(stateDict)
  #stateFile.close()
  raspi_gio_print_state_log()
