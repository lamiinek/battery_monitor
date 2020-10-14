#!/usr/bin/python3
import time
import pathlib
import subprocess
from gi.repository import Notify

class BatteryWatcher():

    def __init__(self):
        super(BatteryWatcher, self).__init__()
        self.chargeCmd = "acpi"
        self.modeCmd = "acpi -V | grep 'Adapter 0:'"

        self.notified = False
        self.change = False
        self.current_mode = self.getPowerMethod()

        while True:
            self.checkStatusChange()
            self.batteryCare()
            time.sleep(30)

    # check if the charger is plugged in or not
    def checkStatusChange(self):
        if self.getPowerMethod() != self.current_mode:
            # print("status changed")
            self.notified = False
            self.current_mode = self.getPowerMethod()



    def getBatteryCharge(self):
        cmdOut = subprocess.getoutput(self.chargeCmd)
        batPercent = cmdOut.split(',')[1]
        batPercent = batPercent.replace(' ', '')
        batPercent = batPercent.replace('%', '')
        return batPercent

    def getPowerMethod(self):
        cmdOut = subprocess.getoutput(self.modeCmd)
        mode = cmdOut.split(":")[1]
        mode = mode.replace(" ", "")
        return mode

    def batteryCare(self):
        #keep the battery between 20 and 80% charge
        if int(self.getBatteryCharge()) >= 80 and self.notified == False:
            self.notif("Unplug charger to help extend battery life", "full")
            self.notified = True
        elif int(self.getBatteryCharge()) < 21 and self.notified == False:
            self.notif("Plug charger to help extend battery life", "low")
            self.notified = True

        if self.getPowerMethod() == "off-line":
            if int(self.getBatteryCharge()) == 40 and self.notified == False:
                self.notif("Battery at 40%, plug it in if possible", "topoff")
                self.notified = True

    def notif(self, msg, status):
        title = "Lamine Battery Care"
        icon_path = str(pathlib.Path(__file__).parent.absolute())
        bat_full_icon = icon_path+"/battery_full.png"
        bat_topoff_icon = icon_path+"/battery_topff.png"
        bat_low_icon = icon_path+"/battery_low.png"
        Notify.init(title)
        if status == "full":
            notification = Notify.Notification.new(title, msg, bat_full_icon).show()
        elif status == "low":
            notification = Notify.Notification.new(title, msg, bat_low_icon).show()
        elif status == "topoff":
            notification = Notify.Notification.new(title, msg, bat_topoff_icon).show()

        return notification


if __name__ == '__main__':
    BatteryWatcher()
