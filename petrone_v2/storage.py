import time

from petrone_v2.protocol import *
from petrone_v2.system import *


# Event
class Event:

    def __init__(self):
        self.ack                = None
        self.message            = None
        self.information        = None
        self.address            = None
        
        self.state              = None
        self.attitude           = None
        self.accelBias          = None
        self.gyroBias           = None
        self.trimFlight         = None
        self.trimDrive          = None
        
        self.imu                = None
        self.pressure           = None
        self.battery            = None
        self.range              = None
        self.imageFlow          = None
        
        self.button             = None
        
        self.irMessage          = None
        
        self.countFlight        = None
        self.countDrive         = None
        
        self.pairing            = None
        self.rssi               = None



# Storage
class Storage:

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

        self.irMessage          = IrMessage()

        self.countFlight        = CountFlight()
        self.countDrive         = CountDrive()

        self.pairing            = Pairing()
        self.rssi               = Rssi()



# Storage Count
class StorageCount:

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

        self.irMessage          = 0

        self.countFlight        = 0
        self.countDrive         = 0

        self.pairing            = 0
        self.rssi               = 0



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

        self.irMessage          = IrMessage()

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

        self.irMessage          = 0

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


