#!/usr/bin/python3

import RPi.GPIO as GPIO
#from gpiozero import LED
from time import sleep
from os.path import exists
import pickle
import sys
import json

#pin = int(sys.argv[1])
#state = int(sys.argv[2])

#stateFileName = "state_log"
#stateFilePath = ""
#stateFileFullPath = stateFilePath + stateFileName
#settingsFileName = "settings.ini"

# Default settings
#raspi_gpio_settings = {"stateFileName": "state_log", "stateFilePath": ""}

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
  #for x in settings_content:
  #  print(x)
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

  #print(raspi_gpio_settings)

  for x in raspi_gpio_settings:
    if x not in readSettingsContent:
      readSettingsContent[x] = raspi_gpio_settings[x]
      write_settings_file(settingsFileName, settingsFileFolderLevel, readSettingsContent)
  
  raspi_gpio_settings = read_settings_file(settingsFileName, settingsFileFolderLevel)
  stateFileFullPath = raspi_gpio_settings["stateFilePath"] + raspi_gpio_settings["stateFileName"]

  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  #print(int(stateDict["Pin"+str(pin)]))
  stateFile.close()
  return int(stateDict["Pin"+str(pin)])

def raspi_gpio_print_pin(settingsFileName="settings.ini", raspi_gpio_settings={"stateFileName": "state_log", "stateFilePath": ""}, pin=1):
  #print(settingsFileName)
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

  stateFile = open(stateFileFullPath, "rb")
  stateDict = pickle.load(stateFile)
  print(int(stateDict["Pin"+str(pin)]))
  stateFile.close()

if __name__ == "__main__":
  #settingsFileName = "settings.ini"
  #raspi_gpio_settings = {"stateFileName": "state_log", "stateFilePath": ""}

  raspi_gpio_print_pin(pin=int(sys.argv[1]))
  #print("Printing file content:")
  #stateFile = open(stateFileFullPath, "rb")
  #stateDict = pickle.load(stateFile)
  #print(int(stateDict["Pin"+str(pin)]))
  #stateFile.close()
  
  #raspi_gpio_print_pin(int(sys.argv[1]))

  #print("these were the default settings:", raspi_gpio_settings)

  #settingsFileFolderLevel = settings_exist()

  #if settingsFileFolderLevel == 0:
  #  generate_settings_file(1, raspi_gpio_settings)
  #  settingsFileFolderLevel = 1
    #print("settings generated")
  #else:
  #  print("settings exist")
  
  #readSettingsContent = read_settings_file(settingsFileFolderLevel)

  #for x in raspi_gpio_settings:
  #  if x not in readSettingsContent:
      #print(x, "already present in settings file")
  #    readSettingsContent[x] = raspi_gpio_settings[x]
  #    write_settings_file(settingsFileFolderLevel, readSettingsContent)
    #else:
      #print("we need to add", x, "to the settings file")
      #print(readSettingsContent)
      #readSettingsContent[x] = raspi_gpio_settings[x]
      #print(readSettingsContent)
      #write_settings_file(settingsFileFolderLevel, readSettingsContent)
  
  #raspi_gpio_settings = read_settings_file(settingsFileFolderLevel)
  #print("these are the new settings:", readSettingsContent)

  #stateFileFullPath = raspi_gpio_settings["stateFilePath"] + raspi_gpio_settings["stateFileName"]

  #raspi_gpio_print_pin(int(sys.argv[1]))