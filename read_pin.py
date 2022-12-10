#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep
from os.path import exists
import pickle
import sys
import json

def settings_exist(settingsFileName):
  if exists(settingsFileName):
      return 1
  else:
      if exists("../" + settingsFileName):
        return 2
      else:
        return 0

def read_settings_file(settingsFileName, folder_level):
  if folder_level == 1:
    settings_file = open(settingsFileName, "rb")
  else:
    settings_file = open("../" + settingsFileName, "rb")
  settings_content = json.load(settings_file)
  settings_file.close()
  return settings_content

def generate_settings_file(settingsFileName, folder_level, settings_content):
  settings_json = json.dumps(settings_content)
  if folder_level == 1:
    settings_file = open(settingsFileName,"w")
  else:
    settings_file = open("../" + settingsFileName,"w")
  settings_file.write(settings_json)
  settings_file.close()

def write_settings_file(settingsFileName, folder_level, settingsContent):
  settings_json = json.dumps(settingsContent)
  if folder_level == 1:
    settings_file = open(settingsFileName,"w")
  else:
    settings_file = open("../" + settingsFileName,"w")
  settings_file.write(settings_json)
  settings_file.close()
  return 0

def raspi_gpio_read_pin(settingsFileName="settings.ini", raspi_gpio_settings={"stateFileName": "state_log", "stateFilePath": ""}, pin=1):
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

def raspi_gpio_print_pin(settingsFileName="settings.ini", raspi_gpio_settings={"stateFileName": "state_log", "stateFilePath": ""}, pin=1):
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
  raspi_gpio_print_pin(pin=int(sys.argv[1]))
