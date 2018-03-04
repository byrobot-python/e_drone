import time

from petrone_v2.protocol import *
from petrone_v2.system import *


# EventHandler
class EventHandler:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))



# StorageHeader
class StorageHeader:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))



# Storage
class Storage:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))



# Storage Count
class StorageCount:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))
        
        for key in self.d:
            self.d[key] = 0



# Storage
class Parser:

    def __init__(self):
        self.d = dict.fromkeys(list(DataType))

        self.d[DataType.Ack]            = Ack.parse
        self.d[DataType.Error]          = Error.parse
        self.d[DataType.Message]        = Message.parse
        self.d[DataType.Information]    = Information.parse
        self.d[DataType.Address]        = Address.parse

        self.d[DataType.State]          = State.parse
        self.d[DataType.Attitude]       = Attitude.parse
        self.d[DataType.AccelBias]      = AccelBias.parse
        self.d[DataType.GyroBias]       = GyroBias.parse
        self.d[DataType.TrimFlight]     = TrimFlight.parse
        self.d[DataType.TrimDrive]      = TrimDrive.parse

        self.d[DataType.Imu]            = Imu.parse
        self.d[DataType.Pressure]       = Pressure.parse
        self.d[DataType.Battery]        = Battery.parse
        self.d[DataType.Range]          = Range.parse
        self.d[DataType.ImageFlow]      = ImageFlow.parse
        self.d[DataType.Button]         = Button.parse
        self.d[DataType.Joystick]       = Joystick.parse
        self.d[DataType.IrMessage]      = IrMessage.parse
        self.d[DataType.CountFlight]    = CountFlight.parse
        self.d[DataType.CountDrive]     = CountDrive.parse
        self.d[DataType.Pairing]        = Pairing.parse
        self.d[DataType.Rssi]           = Rssi.parse

        self.d[DataType.InformationAssembledForController]  = InformationAssembledForController.parse
        self.d[DataType.InformationAssembledForEntry]       = InformationAssembledForEntry.parse
        self.d[DataType.InformationAssembledForImuMonitor]  = InformationAssembledForImuMonitor.parse


