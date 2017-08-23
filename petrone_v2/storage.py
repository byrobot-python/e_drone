import time

from petrone_v2.protocol import *
from petrone_v2.system import *


# Storage Drone
class StorageDrone:

    def __init__(self):
        self.ack                = Ack()
        self.message            = ""
        self.information        = Information()
        self.address            = Address()
        
        self.state              = State()
        self.attitude           = Attitude()
        self.accelBias          = Vector()
        self.gyroBias           = Attitude()
        self.trimFlight         = TrimFlight()
        self.trimDrive          = TrimDrive()

        self.imu                = Imu()
        self.pressure           = Pressure()
        self.battery            = Battery()
        self.range              = Range()
        self.imageFlow          = ImageFlow()

        self.button             = Button()

        self.irMessageFront     = IrMessage()
        self.irMessageRear      = IrMessage()

        self.countFlight        = CountFlight()
        self.countDrive         = CountDrive()

        self.pairing            = Pairing()
        self.rssi               = Rssi()



# Storage Drone Count
class StorageDroneCount:

    def __init__(self):
        self.ack                = 0
        self.message            = ""
        self.information        = 0
        self.address            = 0

        self.state              = 0
        self.attitude           = 0
        self.accelBias          = 0
        self.gyroBias           = 0
        self.trimFlight         = 0
        self.trimDrive          = 0

        self.imu                = 0
        self.pressure           = 0
        self.battery            = 0
        self.range              = 0
        self.imageFlow          = 0

        self.button             = 0

        self.irMessageFront     = 0
        self.irMessageRear      = 0

        self.countFlight        = 0
        self.countDrive         = 0

        self.pairing            = 0
        self.rssi               = 0



# Storage Controller
class StorageController:

    def __init__(self):
        self.ack                = Ack()
        self.message            = ""
        self.information        = Information()
        self.address            = Address()

        self.button             = Button()
        self.joystick           = Joystick()

        self.pairing            = Pairing()
        self.rssi               = Rssi()



# Storage Controller Count
class StorageControllerCount:

    def __init__(self):
        self.ack                = 0
        self.message            = ""
        self.information        = 0
        self.address            = 0

        self.button             = 0
        self.joystick           = 0

        self.pairing            = 0
        self.rssi               = 0


