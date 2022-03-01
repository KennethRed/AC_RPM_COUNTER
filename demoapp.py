"""
    Just some random demo App that submits data to a serial port in Assetto Corsa.
    Made by KennethRed (GitHub profile: https://github.com/KennethRed)

    Basis used from ac_dashboard for figuring out how the hell DLL's and _ctypes should be implemented... (GitHub:
    https://github.com/ev-agelos/ac_dashboard)

    Serial handling and DLL on [Assetto Corsa Arduino LC-Display Dashboard](https://github.com/datort/ac-dashboard)
    """

import os
import sys
import ac
import acsys
import platform

APP_NAME = "demoapp"
comport = "COM4"
SERIAL_PACKAGE_INTERVAL = 100  # in ms
SERIAL_PACKAGES_SENT = 0
SERIAL_BAUDRATE = 9600
APPLICATION_ACTIVE_IN_SECONDS = 0


def initializeSerialConnection():
    availableComPorts = serial.tools.list_ports.comports()

    for ListPortInfo in availableComPorts:
        if comport == ListPortInfo.name:
            ac.log(comport + "found")
            return serial.Serial(port=comport, baudrate=SERIAL_BAUDRATE, timeout=0)

    if serial is None:
        ac.log(comport + " not found...")

        for ListPortInfo in availableComPorts:
            ac.log("- but I did find :" + ListPortInfo.name)


try:
    import threading

    sys.path.insert(0, "apps/python/demoapp/DLLs")
    SYSDIR = "stdlib64" if platform.architecture()[0] == "64bit" else "stdlib"
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), SYSDIR))

    os.environ['PATH'] += ';.'
    import serial
    import serial.tools.list_ports
    from sim_info import info


except Exception as err:
    ac.log("DEMOAPP ERROR: " + str(err))

serialConnection = initializeSerialConnection()


def acMain(ac_version):

    global serialConnection
    """Main function that is invoked by Assetto Corsa, besides acMain you also have acUpdate(delta_t) """

    # Create a new window and set its size
    app_window = ac.newApp(APP_NAME)
    ac.setSize(app_window, 200, 200)

    # create a new label, and add it to the recently created app window. add a new label to it.

    if serialConnection:
        ComPortLabelText = "Device found... Ready. Submitting data to " + comport
    else:
        ComPortLabelText = "Device not found on desired comport:" \
                           + comport \
                           + "Is the device connected to this COM port?" \
                             "Documents -> Assetto Corsa -> logs _> py_log.txt " \
                             "file for currently active com ports."

    comPortLabel = ac.addLabel(app_window, ComPortLabelText)
    ac.setPosition(comPortLabel, 3, 30)

    # the Assetto Corsa acMain function should return the app name(string
    return APP_NAME


def acUpdate(delta_t):
    # Create a secondsCounter
    global APPLICATION_ACTIVE_IN_SECONDS, SERIAL_PACKAGES_SENT
    APPLICATION_ACTIVE_IN_SECONDS = APPLICATION_ACTIVE_IN_SECONDS + delta_t

    # if the time that has passed divided by the SERIAL_INTERVAL is larger than the amount of serial packages sent...
    # then send a new package to serial.
    if ((SERIAL_PACKAGE_INTERVAL * SERIAL_PACKAGES_SENT) / 100) < APPLICATION_ACTIVE_IN_SECONDS:
        ac.log('Should send package.')
        sendDataToArduino()


def acShutdown():
    serialConnection.close()


# ============================
# Ac Class getters
# ============================

def getMaxRpm():
    return info.static.maxRpm


def getCurrentBrakeBalance():
    return "55.6"


def getCoreTireTempLf():
    return "55"


def getCoreTireTempRf():
    return "56"


def getCoreTireTempLr():
    return "62"


def getCoreTireTempRr():
    return "63"


# ============================
# Dashboards
# ============================

"""
Dashboard A, returns current brake balance, LF-core-temp, RF-core-temp, LR-core-temp, RR-core-temp
"""


def dashboardTypeA():  # first dashboard type.

    dashboardData = arrayToCsvString([
        info.physics.brakeBias,
        info.physics.tyreCoreTemperature[0],
        info.physics.tyreCoreTemperature[1],
        info.physics.tyreCoreTemperature[2],
        info.physics.tyreCoreTemperature[3]
    ])
    string = "<1," + dashboardData + ">"

    return string


# ============================
# helpers/functions
# ============================

def arrayToCsvString(array):
    string = ""

    for item in array:
        string = string + "," + item

    ac.log(string[1:])
    # return the complete string without the first character.
    return string[1:]


# ============================
# Serial function
# ============================
def sendDataToArduino():
    global serialConnection, SERIAL_PACKAGES_SENT
    """
    currently one dashboard is supported.

    For type A submit:
        type:a,
        brakeBalance:12.3,
        tireTempLf:55,
        tireTempRf:56,
        tireTempLr:62,
        tireTempRr:63
        we end the line with a ;
        
        a,12.3,55,56,62,63;

    this way we only submit the data we want to submit and keep the data submitted via serial lean:
    dashboard A doesn't show the rpm, so we send that data over serial.
    """
    # ac.log('serialConnection.write dashboarDtypeA.encode')
    ac.log('sending package.')
    serialConnection.write(dashboardTypeA().encode())
    ac.log('package succesfully sent.')
    SERIAL_PACKAGES_SENT = SERIAL_PACKAGES_SENT + 1
