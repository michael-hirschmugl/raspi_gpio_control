#!/usr/bin/python

from os.path import exists
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

if __name__ == "__main__":
  print("This file is not intended to be called as main. sorry...")