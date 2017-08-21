import serial
import binascii
import random
import queue
import threading
from threading import Thread
from time import sleep
from struct import *

from petrone_v2.protocol import *
from petrone_v2.storage import *
from petrone_v2.receiver import *
from petrone_v2.system import *
from petrone_v2.crc import *




class Drone:


    def __init__(self):
        
        self.serialport      = None
        self.bufferReceive   = []
        self.bufferHandler   = []
        self.index           = 0

        self.threadLock      = threading.Lock()
        self.flagThreadRun   = False

        self.receiver        = Receiver()
        self.storage         = Storage()


    def _receiving(self):
        while self.flagThreadRun:
            
            self.threadLock.acquire()        # Get lock to synchronize threads
            self.bufferReceive.extend(self.serialport.read())
            self.threadLock.release()        # Free lock to release next thread

            sleep(0.001)


    def open(self, portname):
        self.serialport = serial.Serial(
            port        = portname,
            baudrate    = 115200,
            parity      = serial.PARITY_NONE,
            stopbits    = serial.STOPBITS_ONE,
            bytesize    = serial.EIGHTBITS,
            timeout     = 0)

        if( self.serialport.isOpen() ):
            self.flagThreadRun = True
            Thread(target=self._receiving, args=()).start()


    def close(self):
        self.flagThreadRun = False
        sleep(0.002)
        while (self.serialport.isOpen() == True):
            self.serialport.close()
            sleep(0.002)


    def makeTransferDataArray(self, header, data):
        if (header == None) or (data == None):
            return None

        if (not isinstance(header, Header)) or (not isinstance(data, ISerializable)):
            return None

        crc16 = CRC16.calc(header.toArray(), 0)
        crc16 = CRC16.calc(data.toArray(), crc16)

        dataArray = []
        dataArray.extend((0x0A, 0x55))
        dataArray.extend(header.toArray())
        dataArray.extend(data.toArray())
        dataArray.extend(pack('H', crc16))

        #print("{0} / {1}".format(len(dataArray), dataArray))

        return dataArray


    def transfer(self, header, data):
        if (self.serialport == None) or (self.serialport.isOpen() == False):
            return

        dataArray = self.makeTransferDataArray(header, data)

        self.serialport.write(dataArray)

        return dataArray


    def check(self):
        if len(self.bufferReceive) > 0:
            self.threadLock.acquire()           # Get lock to synchronize threads
            self.bufferHandler.extend(self.bufferReceive)
            self.bufferReceive.clear()
            self.threadLock.release()            # Free lock to release next thread

            while len(self.bufferHandler) > 0:
                self.receiver.call(self.bufferHandler[0])
                del(self.bufferHandler[0])
                
                if self.receiver.state == StateLoading.Loaded:
                    self.handler(self.receiver.header, self.receiver.dataBuffer)
                    self.receiver.checked()
                    return self.receiver.header.dataType

        return DataType.None_



    def handler(self, header, dataArray):
        if header.dataType == DataType.Ack:
            self.storage.countAck += 1



# Light Start


    def sendLightManual(self, target, flags, brightness):
        
        if  (((target != DeviceType.Drone) and (target != DeviceType.Controller)) or
            (not isinstance(flags, int)) or
            (not isinstance(brightness, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightManual
        header.length   = LightManual.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = target

        data = LightManual()

        data.flags      = flags
        data.brightness = brightness

        return self.transfer(header, data)
    



    def sendLightModeColor(self, lightMode, interval, r, g, b):
        
        if  (((not isinstance(lightMode, LightModeDrone)) and (not isinstance(lightMode, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightModeColor
        header.length   = LightModeColor.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightMode, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightMode, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightModeColor()

        data.mode.mode      = lightMode.value
        data.mode.interval  = interval

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)



    def sendLightModeColorCommand(self, lightMode, interval, r, g, b, commandType, option):
        
        if  (((not isinstance(lightMode, LightModeDrone)) and (not isinstance(lightMode, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int)) or
            (not isinstance(commandType, CommandType)) or
            (not isinstance(option, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightModeColorCommand
        header.length   = LightModeColorCommand.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightMode, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightMode, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightModeColorCommand()

        data.mode.mode      = lightMode.value
        data.mode.interval  = interval

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        data.command.commandType    = commandType
        data.command.option         = option

        return self.transfer(header, data)



    def sendLightModeColorCommandIr(self, lightMode, interval, r, g, b, commandType, option, irData):
        
        if  (((not isinstance(lightMode, LightModeDrone)) and (not isinstance(lightMode, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int)) or
            (not isinstance(commandType, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(irData, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightModeColorCommandIr
        header.length   = LightModeColorCommandIr.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightMode, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightMode, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightModeColorCommandIr()

        data.mode.mode      = lightMode.value
        data.mode.interval  = interval

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        data.command.commandType    = commandType
        data.command.option         = option

        data.irData         = irData

        return self.transfer(header, data)



    def sendLightModeColors(self, lightMode, interval, colors):
        
        if  (((not isinstance(lightMode, LightModeDrone)) and (not isinstance(lightMode, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.dataType = DataType.LightModeColors
        header.length   = LightModeColors.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightMode, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightMode, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightModeColors()

        data.mode.mode      = lightMode.value
        data.mode.interval  = interval

        data.colors         = colors

        return self.transfer(header, data)



    def sendLightModeColorsCommand(self, lightMode, interval, colors, command, option):
        
        if  (((not isinstance(lightMode, LightModeDrone)) and (not isinstance(lightMode, LightModeController))) or
            (not isinstance(interval, int))  or
            (not isinstance(colors, Colors)) or
            (not isinstance(command, CommandType)) or
            (not isinstance(option, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightModeColorsCommand
        header.length   = LightModeColorsCommand.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightMode, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightMode, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightModeColorsCommand()

        data.mode.mode      = lightMode.value
        data.mode.interval  = interval

        data.colors         = colors

        data.command.commandType    = command
        data.command.option         = option

        return self.transfer(header, data)



    def sendLightModeColorsCommandIr(self, lightMode, interval, colors, command, option, irData):
        
        if  (((not isinstance(lightMode, LightModeDrone)) and (not isinstance(lightMode, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(colors, Colors)) or
            (not isinstance(command, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(irData, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightModeColorsCommandIr
        header.length   = LightModeColorsCommandIr.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightMode, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightMode, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightModeColorsCommandIr()

        data.mode.mode      = lightMode.value
        data.mode.interval  = interval

        data.colors         = colors

        data.command.commandType    = command
        data.command.option         = option

        data.irData      = irData

        return self.transfer(header, data)
    


    def sendLightEventColor(self, lightEvent, interval, repeat, r, g, b):
        
        if  (((not isinstance(lightEvent, LightModeDrone)) and (not isinstance(lightEvent, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEventColor
        header.length   = LightEventColor.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightEvent, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightEvent, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightEventColor()

        data.event.event    = lightEvent.value
        data.event.interval = interval
        data.event.repeat   = repeat

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)



    def sendLightEventColorCommand(self, lightEvent, interval, repeat, r, g, b, commandType, option):
        
        if  (((not isinstance(lightEvent, LightModeDrone)) and (not isinstance(lightEvent, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int)) or
            (not isinstance(commandType, CommandType)) or
            (not isinstance(option, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEventColorCommand
        header.length   = LightEventColorCommand.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightEvent, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightEvent, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightEventColorCommand()

        data.event.event    = lightEvent.value
        data.event.interval = interval
        data.event.repeat   = repeat

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        data.command.commandType    = commandType
        data.command.option         = option

        return self.transfer(header, data)



    def sendLightEventColorCommandIr(self, lightEvent, interval, repeat, r, g, b, commandType, option, irData):
        
        if  (((not isinstance(lightEvent, LightModeDrone)) and (not isinstance(lightEvent, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int)) or
            (not isinstance(commandType, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(irData, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEventColorCommandIr
        header.length   = LightEventColorCommandIr.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightEvent, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightEvent, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightEventColorCommandIr()

        data.event.event    = lightEvent.value
        data.event.interval = interval
        data.event.repeat   = repeat

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        data.command.commandType    = commandType
        data.command.option         = option

        data.irData      = irData

        return self.transfer(header, data)



    def sendLightEventColors(self, lightEvent, interval, repeat, colors):
        
        if  (((not isinstance(lightEvent, LightModeDrone)) and (not isinstance(lightEvent, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEventColors
        header.length   = LightEventColors.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightEvent, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightEvent, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightEventColors()

        data.event.event    = lightEvent.value
        data.event.interval = interval
        data.event.repeat   = repeat

        data.colors         = colors

        return self.transfer(header, data)



    def sendLightEventColorsCommand(self, lightEvent, interval, repeat, colors, command, option):
        
        if  (((not isinstance(lightEvent, LightModeDrone)) and (not isinstance(lightEvent, LightModeController))) or
            (not isinstance(interval, int))  or
            (not isinstance(repeat, int)) or
            (not isinstance(colors, Colors)) or
            (not isinstance(command, CommandType)) or
            (not isinstance(option, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEventColorsCommand
        header.length   = LightEventColorsCommand.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightEvent, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightEvent, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightEventColorsCommand()

        data.event.event    = lightEvent.value
        data.event.interval = interval
        data.event.repeat   = repeat

        data.colors         = colors

        data.command.commandType    = command
        data.command.option         = option

        return self.transfer(header, data)



    def sendLightEventColorsCommandIr(self, lightEvent, interval, repeat, colors, command, option, irData):
        
        if  (((not isinstance(lightEvent, LightModeDrone)) and (not isinstance(lightEvent, LightModeController))) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(colors, Colors)) or
            (not isinstance(command, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(irData, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEventColorsCommandIr
        header.length   = LightEventColorsCommandIr.getSize()
        header.from_    = DeviceType.Tester

        if      isinstance(lightEvent, LightModeDrone):
            header.to_  = DeviceType.Drone
        elif    isinstance(lightEvent, LightModeController):
            header.to_  = DeviceType.Controller
        else:
            return None

        data = LightEventColorsCommandIr()

        data.event.event    = lightEvent.value
        data.event.interval = interval
        data.event.repeat   = repeat

        data.colors         = colors

        data.command.commandType    = command
        data.command.option         = option

        data.irData      = irData

        return self.transfer(header, data)
    




# Light End



# Display Start


    def sendDisplayClearAll(self, pixel):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayClear
        header.length   = DisplayClearAll.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayClearAll()

        data.pixel      = pixel

        return self.transfer(header, data)
    


    def sendDisplayClear(self, x, y, width, height, pixel):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayClear
        header.length   = DisplayClear.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayClear()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height
        data.pixel      = pixel

        return self.transfer(header, data)



    def sendDisplayInvert(self, x, y, width, height):
        
        header = Header()
        
        header.dataType = DataType.DisplayInvert
        header.length   = DisplayInvert.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayInvert()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height

        return self.transfer(header, data)



    def sendDisplayDrawPoint(self, x, y, pixel):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawPoint
        header.length   = DisplayDrawPoint.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawPoint()

        data.x          = x
        data.y          = y
        data.pixel      = pixel

        return self.transfer(header, data)



    def sendDisplayDrawRect(self, x, y, width, height, pixel, flagFill):
        
        if ( (not isinstance(pixel, DisplayPixel)) or (not isinstance(flagFill, bool)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawRect
        header.length   = DisplayDrawRect.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawRect()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height
        data.pixel      = pixel
        data.flagFill   = flagFill

        return self.transfer(header, data)



    def sendDisplayDrawCircle(self, x, y, radius, pixel, flagFill):
        
        if ( (not isinstance(pixel, DisplayPixel)) or (not isinstance(flagFill, bool)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawCircle
        header.length   = DisplayDrawCircle.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawCircle()

        data.x          = x
        data.y          = y
        data.radius     = radius
        data.pixel      = pixel
        data.flagFill   = flagFill

        return self.transfer(header, data)



    def sendDisplayDrawString(self, x, y, font, pixel, message):
        
        if ( (not isinstance(font, DisplayFont)) or (not isinstance(pixel, DisplayPixel)) or (not isinstance(message, str)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawString
        header.length   = DisplayDrawString.getSize() + len(message)
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawString()

        data.x          = x
        data.y          = y
        data.font       = font
        data.pixel      = pixel
        data.message    = message

        return self.transfer(header, data)



    def sendDisplayDrawStringAlign(self, x_start, x_end, y, align, font, pixel, message):
        
        if ( (not isinstance(align, DisplayAlign)) or (not isinstance(font, DisplayFont)) or (not isinstance(pixel, DisplayPixel)) or (not isinstance(message, str)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawStringAlign
        header.length   = DisplayDrawStringAlign.getSize() + len(message)
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawStringAlign()

        data.x_start    = x_start
        data.x_end      = x_end
        data.y          = y
        data.align      = align
        data.font       = font
        data.pixel      = pixel
        data.message    = message

        return self.transfer(header, data)


# Display End

