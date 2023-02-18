#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
from datetime import datetime
from settings_handler import settings_exist, read_settings_file, generate_settings_file, write_settings_file
from state_handler import file_test, set_pin_state


def raspi_gpio_control(pin, state):
  settingsFileName = "/home/automation/settings/gpio_settings.ini"
  raspi_gpio_settings = {"stateFileName": "state_log", "stateFilePath": "", "logFileName": "usage_log.txt", "logFilePath": ""}
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
  raspi_gpio_control(int(sys.argv[1]), int(sys.argv[2]))
