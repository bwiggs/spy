#!/usr/bin/python
import optparse
import os
import subprocess
import time

VERSION = "0.1"
COPYRIGHT = "Copyright 2011 Brian Wigginton.\n"

def main():

    parser = optparse.OptionParser(usage="%prog [OPTIONS] [TARGET]", version="%prog " + VERSION + '\n\n' + COPYRIGHT)

    # add options
    parser.add_option("-c", "--clear", action="store_true", default=False, dest="clear_screen", help="clear the screen after each execution")
    parser.add_option("-e", "--exec", dest="command", help="path to the program to execute")
    parser.add_option("-i", "--interval", type="int", default="1", dest="interval", help="(in seconds) set the time interval to check for file modifications")

    # parse options
    (options, args) = parser.parse_args()

    # safety checks
    if len(args) != 1:
        parser.print_help()
        exit(-1)
        #parser.error("incorrect number of arguments")

    # Get's the last modified time of the file to watch
    def getModificationTime():
        return os.stat(args[0]).st_mtime

    # Executes the desired command
    def runCommand():
        if options.clear_screen: subprocess.call(["clear"])
        return subprocess.call(options.command if options.command else args[0])

    # main loop
    def loop():

        runCommand()

        global data
        data = getModificationTime()
        run = True

        while run:
            try:
                time.sleep(options.interval)
                newData = getModificationTime()
                if data != newData:
                  data = newData
                  runCommand()
            except KeyboardInterrupt:
                run = False

    loop()

if __name__ == '__main__':
    main()
