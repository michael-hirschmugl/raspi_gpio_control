#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
from os.path import exists
import pickle
import sys
import json
from settings_handler import settings_exist, read_settings_file, generate_settings_file, write_settings_file


def raspi_gpio_read_pin(pin):
  settingsFileName = "settings.ini"
  raspi_gpio_settings = {"stateFileName": "state_log", "stateFilePath": ""}
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

  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  stateFile.close()
  return int(stateDict["Pin"+str(pin)])

def raspi_gpio_print_pin(pin):
  settingsFileName = "settings.ini"
  raspi_gpio_settings = {"stateFileName": "state_log", "stateFilePath": ""}
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

  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  print(int(stateDict["Pin"+str(pin)]))
  stateFile.close()

if __name__ == "__main__":
  raspi_gpio_print_pin(int(sys.argv[1]))
