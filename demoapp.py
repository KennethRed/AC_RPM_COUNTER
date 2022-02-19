"""
    Just some random demo App that shows the MaxRPM in window for Assetto Corsa.
    Made by KennethRed (Github profile: https://github.com/KennethRed)

    Basis used from ac_dashboard for figuring out how the hell DLL's and _ctypes should be implemented... (github: https://github.com/ev-agelos/ac_dashboard)
"""
import ac

try:
    import os
    import sys
    import platform
    import threading

    sys.path.insert(0, "apps/python/ac_dashboard/DLLs")
    SYSDIR = "stdlib64" if platform.architecture()[0] == "64bit" else "stdlib"
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), SYSDIR))
    os.environ['PATH'] += ';.'

    from sim_info import info

except Exception as err:
    ac.log("ac_dashboard: " + str(err))

import acsys

APP_NAME = "demoapp"


def acMain(ac_version):
    """Main function that is invoked by Assetto Corsa, besides acMain you also have acUpdate(deltaT) """

    # Create a new window and set its size
    app_window = ac.newApp(APP_NAME)
    ac.setSize(app_window, 200, 200)

    # create a new label, and add it to the recently created app window. add a new label to it.
    rpm_label = ac.addLabel(app_window, "RPM: " + str(getMaxRpm()))

    # then we set the position of the label
    ac.setPosition(rpm_label, 3, 30)

    # the Assetto Corsa acMain function should return the app name(string
    return APP_NAME


def getMaxRpm():
    return info.static.maxRpm
