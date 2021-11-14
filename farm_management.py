#!/usr/bin/python3
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import configparser
import os
import syslog
#import argparse
from threading import Timer

def read_configuration(config_file_path):
    config = configparser.ConfigParser()
    if os.path.exists(config_file_path) and os.path.isfile(config_file_path):
        try:
            config.read(config_file_path)
        except Exception:
            syslog.syslog(syslog.LOG_ERR, "Cannot open configuration file . Do nothing")
            return None
    else:
        syslog.syslog(syslog.LOG_ERR, "Configuration file " + config_file_path + " does not exist. Do nothing")
    for key in config.sections():
        syslog.syslog(syslog.LOG_INFO, key)
        #
        if not 'pin' in config[key]:
            syslog.syslog(syslog.LOG_ERR, "---> Device " + key + " did not provide pin number. Skipping.")
            config.remove_section(key)
            continue
        else:
            syslog.syslog(syslog.LOG_INFO, "|--> pin No. =  " + config[key]['pin'])
        #
        if not 'pins_numbering' in config[key]:
            config[key]['pins_numbering'] = 'BOARD'
        syslog.syslog(syslog.LOG_INFO, "|--> Pins' numbering is " + config[key]['pins_numbering'])
        #
        if not 'on_every' in config[key]:
            config[key]['on_every'] = '259200'
        syslog.syslog(syslog.LOG_INFO, "|--> Switch on every " + config[key]['on_every'] + " seconds")
        #
        if not 'duration' in config[key]:
            config[key]['duration'] = '1800'
        syslog.syslog(syslog.LOG_INFO, "---> Switch on for " + config[key]['duration'] + " seconds")
        if float(config[key]['on_every']) - float(config[key]['duration']) <= 0:
            syslog.syslog(syslog.LOG_ERR, "---> Duration may not be more than 'Switch on every' time. Skipping")
            config.remove_section(key)
            continue
    return config

#def read_args():
#    parser = argparse.ArgumentParser()
#    parser.add_argument("-v", "--verbose", help="increase output verbosity",
#                        action="store_true")
#    args = parser.parse_args()
#    if args.verbose:
#        print("verbosity turned on")

def set_on_off_pin(pin_number=3, on=True):
    if on:
        #print(str(pin_number) + " -> on")
        GPIO.output(pin_number, GPIO.HIGH)
    else:
        #print(str(pin_number) + " -> off")
        GPIO.output(pin_number, GPIO.LOW)

def switch_on_off_dev(config, dev_name, on=True):
    set_on_off_pin(
        int(config[dev_name]['pin']),
        on
    )
    if on:
        Timer(
            float(config[dev_name]['duration']),
            switch_on_off_dev,
            args=[config, dev_name, False]
        ).start()
    else:
        Timer(
            float(config[dev_name]['on_every']) - float(config[dev_name]['duration']),
            switch_on_off_dev, 
            args=[config, dev_name, True]
        ).start()


if __name__ == '__main__':
    syslog.openlog("FARM: ", logoption=0, facility=syslog.LOG_SYSLOG)
    config = read_configuration("./farm_config.ini")
    if config == None:
        syslog.syslog(syslog.LOG_ERR, "Config has not been built. Shutting down.")
        exit(1)
    # setting up pins
    for key in config.sections():
        if config[key]['pins_numbering'] == 'BOARD':
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(config[key]['pin']), GPIO.OUT)
        set_on_off_pin(int(config[key]['pin']), False)
    for key in config.sections():
        Timer(
            float(config[key]['on_every']),
            switch_on_off_dev, 
            args=[config, key, True]
        ).start()

    syslog.closelog()