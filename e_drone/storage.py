import time

from e_drone.protocol import *
from e_drone.system import *


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

        self.d[DataType.PING]               = Ping.parse
        self.d[DataType.ACK]                = Ack.parse
        self.d[DataType.ERROR]              = Error.parse
        self.d[DataType.MESSAGE]            = Message.parse
        self.d[DataType.ADDRESS]            = Address.parse
        self.d[DataType.INFORMATION]        = Information.parse
        self.d[DataType.UPDATE_LOCATION]    = UpdateLocation.parse
        self.d[DataType.SYSTEM_INFORMATION] = SystemInformation.parse
        self.d[DataType.REGISTRATION]       = RegistrationInformation.parse

        self.d[DataType.PAIRING]            = Pairing.parse
        self.d[DataType.RSSI]               = Rssi.parse

        self.d[DataType.RAW_MOTION]         = RawMotion.parse
        self.d[DataType.RAW_FLOW]           = RawFlow.parse

        self.d[DataType.STATE]              = State.parse
        self.d[DataType.ATTITUDE]           = Attitude.parse
        self.d[DataType.POSITION]           = Position.parse
        self.d[DataType.ALTITUDE]           = Altitude.parse
        self.d[DataType.MOTION]             = Motion.parse
        self.d[DataType.RANGE]              = Range.parse

        self.d[DataType.COUNT]              = Count.parse
        self.d[DataType.BIAS]               = Bias.parse
        self.d[DataType.TRIM]               = Trim.parse
        self.d[DataType.WEIGHT]             = Weight.parse

        self.d[DataType.BUTTON]             = Button.parse
        self.d[DataType.JOYSTICK]           = Joystick.parse

        self.d[DataType.CARD_CLASSIFY]       = CardClassify.parse
        self.d[DataType.CARD_RANGE]          = CardRange.parse
        self.d[DataType.CARD_RAW]            = CardRaw.parse
        self.d[DataType.CARD_COLOR]          = CardColor.parse
        self.d[DataType.CARD_LIST]           = CardList.parse
        self.d[DataType.CARD_FUNCTION_LIST]  = CardList.parse

        self.d[DataType.INFORMATION_ASSEMBLED_FOR_CONTROLLER]  = InformationAssembledForController.parse
        self.d[DataType.INFORMATION_ASSEMBLED_FOR_ENTRY]       = InformationAssembledForEntry.parse


