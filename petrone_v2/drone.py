import serial
import binascii
import random
import queue
import threading
from threading import Thread
from time import sleep
from struct import *
import time

from petrone_v2.protocol import *
from petrone_v2.storage import *
from petrone_v2.receiver import *
from petrone_v2.system import *
from petrone_v2.crc import *




class Drone:

# BaseFunctions Start

    def __init__(self):
        
        self.serialport                 = None
        self.bufferReceive              = []
        self.bufferHandler              = []
        self.index                      = 0

        self.threadLock                 = threading.Lock()
        self.flagThreadRun              = False

        self.receiver                   = Receiver()

        self.storage                    = Storage()
        self.storageCount               = StorageCount()
        self.storageDrone               = StorageDrone()
        self.storageDroneCount          = StorageDroneCount()
        self.storageController          = StorageController()
        self.storageControllerCount     = StorageControllerCount()



    def _receiving(self):
        while self.flagThreadRun:
            
            self.threadLock.acquire()        # Get lock to synchronize threads

            self.bufferReceive.extend(self.serialport.read())

            length = len(self.bufferReceive)
            if length > 16384:
                del self.bufferReceive[0:(length - 16384)]    # bufferReceive에 저장된 데이터가 16384 바이트를 초과하면 이전에 받은 데이터를 제거함
            
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
                    self.handler(self.receiver.header, self.receiver.data)
                    self.receiver.checked()
                    return self.receiver.header.dataType

        return DataType.None_



    def checkDetail(self):
        if len(self.bufferReceive) > 0:
            self.threadLock.acquire()           # Get lock to synchronize threads
            self.bufferHandler.extend(self.bufferReceive)
            self.bufferReceive.clear()
            self.threadLock.release()            # Free lock to release next thread

            while len(self.bufferHandler) > 0:
                self.receiver.call(self.bufferHandler[0])
                del(self.bufferHandler[0])
                
                if self.receiver.state == StateLoading.Loaded:
                    self.handler(self.receiver.header, self.receiver.data)
                    self.receiver.checked()
                    return self.receiver.header, self.receiver.data

        return None, None



    def handler(self, header, dataArray):

        # 들어오는 데이터를 구분없이 저장
        self._handler(header, dataArray)

        # 들어오는 데이터를 구분하여 저장
        if      header.from_ == DeviceType.Drone:
            self._handlerDrone(header, dataArray)
        elif    header.from_ == DeviceType.Controller:
            self._handlerController(header, dataArray)

        return header.dataType



    def _handler(self, header, dataArray):
        if      header.dataType == DataType.Ack:
            self.storage.ack       = Ack.parse(dataArray);
            self.storageCount.ack  += 1

        elif    header.dataType == DataType.Message:
            self.storage.message       = dataArray.decode()
            self.storageCount.message  += 1

        elif    header.dataType == DataType.Information:
            self.storage.information       = Information.parse(dataArray)
            self.storageCount.information  += 1

        elif    header.dataType == DataType.Address:
            self.storage.address       = Address.parse(dataArray)
            self.storageCount.address  += 1


        elif    header.dataType == DataType.State:
            self.storage.state         = State.parse(dataArray)
            self.storageCount.state    += 1

        elif    header.dataType == DataType.Attitude:
            self.storage.attitude          = Attitude.parse(dataArray)
            self.storageCount.attitude     += 1

        elif    header.dataType == DataType.AccelBias:
            self.storage.accelBias         = Vector.parse(dataArray)
            self.storageCount.accelBias    += 1

        elif    header.dataType == DataType.GyroBias:
            self.storage.gyroBias          = Attitude.parse(dataArray)
            self.storageCount.gyroBias     += 1

        elif    header.dataType == DataType.TrimFlight:
            self.storage.trimFlight        = TrimFlight.parse(dataArray)
            self.storageCount.trimFlight   += 1

        elif    header.dataType == DataType.TrimDrive:
            self.storage.trimDrive         = TrimDrive.parse(dataArray)
            self.storageCount.trimDrive    += 1


        elif    header.dataType == DataType.Imu:
            self.storage.imu       = Imu.parse(dataArray)
            self.storageCount.imu  += 1

        elif    header.dataType == DataType.Pressure:
            self.storage.pressure      = Pressure.parse(dataArray)
            self.storageCount.pressure += 1

        elif    header.dataType == DataType.Battery:
            self.storage.battery       = Battery.parse(dataArray)
            self.storageCount.battery  += 1

        elif    header.dataType == DataType.Range:
            self.storage.range         = Range.parse(dataArray)
            self.storageCount.range    += 1

        elif    header.dataType == DataType.ImageFlow:
            self.storage.imageFlow = ImageFlow.parse(dataArray)
            self.storageCount.imageFlow    += 1


        elif    header.dataType == DataType.Button:
            self.storage.button        = Button.parse(dataArray)
            self.storageCount.button   += 1


        elif    header.dataType == DataType.IrMessage:
            irMessage = IrMessage.parse(dataArray)

            if  irMessage.direction == Direction.Front:
                self.storage.irMessageFront        = irMessage
                self.storageCount.irMessageFront   += 1
            else:
                self.storage.irMessageRear         = irMessage
                self.storageCount.irMessageRear    += 1


        elif    header.dataType == DataType.CountFlight:
            self.storage.countFlight       = CountFlight.parse(dataArray)
            self.storageCount.countFlight  += 1

        elif    header.dataType == DataType.CountDrive:
            self.storage.countDrive        = CountDrive.parse(dataArray)
            self.storageCount.countDrive   += 1


        elif    header.dataType == DataType.Pairing:
            self.storage.pairing       = Pairing.parse(dataArray)
            self.storageCount.pairing  += 1

        elif    header.dataType == DataType.Rssi:
            self.storage.rssi          = Rssi.parse(dataArray)
            self.storageCount.rssi     += 1




    def _handlerDrone(self, header, dataArray):
        if      header.dataType == DataType.Ack:
            self.storageDrone.ack       = Ack.parse(dataArray);
            self.storageDroneCount.ack  += 1

        elif    header.dataType == DataType.Message:
            self.storageDrone.message       = dataArray.decode()
            self.storageDroneCount.message  += 1

        elif    header.dataType == DataType.Information:
            self.storageDrone.information       = Information.parse(dataArray)
            self.storageDroneCount.information  += 1

        elif    header.dataType == DataType.Address:
            self.storageDrone.address       = Address.parse(dataArray)
            self.storageDroneCount.address  += 1


        elif    header.dataType == DataType.State:
            self.storageDrone.state         = State.parse(dataArray)
            self.storageDroneCount.state    += 1

        elif    header.dataType == DataType.Attitude:
            self.storageDrone.attitude          = Attitude.parse(dataArray)
            self.storageDroneCount.attitude     += 1

        elif    header.dataType == DataType.AccelBias:
            self.storageDrone.accelBias         = Vector.parse(dataArray)
            self.storageDroneCount.accelBias    += 1

        elif    header.dataType == DataType.GyroBias:
            self.storageDrone.gyroBias          = Attitude.parse(dataArray)
            self.storageDroneCount.gyroBias     += 1

        elif    header.dataType == DataType.TrimFlight:
            self.storageDrone.trimFlight        = TrimFlight.parse(dataArray)
            self.storageDroneCount.trimFlight   += 1

        elif    header.dataType == DataType.TrimDrive:
            self.storageDrone.trimDrive         = TrimDrive.parse(dataArray)
            self.storageDroneCount.trimDrive    += 1


        elif    header.dataType == DataType.Imu:
            self.storageDrone.imu       = Imu.parse(dataArray)
            self.storageDroneCount.imu  += 1

        elif    header.dataType == DataType.Pressure:
            self.storageDrone.pressure      = Pressure.parse(dataArray)
            self.storageDroneCount.pressure += 1

        elif    header.dataType == DataType.Battery:
            self.storageDrone.battery       = Battery.parse(dataArray)
            self.storageDroneCount.battery  += 1

        elif    header.dataType == DataType.Range:
            self.storageDrone.range         = Range.parse(dataArray)
            self.storageDroneCount.range    += 1

        elif    header.dataType == DataType.ImageFlow:
            self.storageDrone.imageFlow = ImageFlow.parse(dataArray)
            self.storageDroneCount.imageFlow    += 1


        elif    header.dataType == DataType.Button:
            self.storageDrone.button        = Button.parse(dataArray)
            self.storageDroneCount.button   += 1


        elif    header.dataType == DataType.IrMessage:
            irMessage = IrMessage.parse(dataArray)

            if  irMessage.direction == Direction.Front:
                self.storageDrone.irMessageFront        = irMessage
                self.storageDroneCount.irMessageFront   += 1
            else:
                self.storageDrone.irMessageRear         = irMessage
                self.storageDroneCount.irMessageRear    += 1


        elif    header.dataType == DataType.CountFlight:
            self.storageDrone.countFlight       = CountFlight.parse(dataArray)
            self.storageDroneCount.countFlight  += 1

        elif    header.dataType == DataType.CountDrive:
            self.storageDrone.countDrive        = CountDrive.parse(dataArray)
            self.storageDroneCount.countDrive   += 1


        elif    header.dataType == DataType.Pairing:
            self.storageDrone.pairing       = Pairing.parse(dataArray)
            self.storageDroneCount.pairing  += 1

        elif    header.dataType == DataType.Rssi:
            self.storageDrone.rssi          = Rssi.parse(dataArray)
            self.storageDroneCount.rssi     += 1



    def _handlerController(self, header, dataArray):
        if      header.dataType == DataType.Ack:
            self.storageController.ack          = Ack.parse(dataArray);
            self.storageControllerCount.ack     += 1

        elif    header.dataType == DataType.Message:
            self.storageController.message          = dataArray.decode()
            self.storageControllerCount.message     += 1

        elif    header.dataType == DataType.Information:
            self.storageController.information      = Information.parse(dataArray)
            self.storageControllerCount.information += 1

        elif    header.dataType == DataType.Address:
            self.storageController.address          = Address.parse(dataArray)
            self.storageControllerCount.address     += 1


        elif    header.dataType == DataType.Button:
            self.storageController.button           = Button.parse(dataArray)
            self.storageControllerCount.button      += 1

        elif    header.dataType == DataType.Joystick:
            self.storageController.joystick         = Joystick.parse(dataArray)
            self.storageControllerCount.joystick    += 1


        elif    header.dataType == DataType.Pairing:
            self.storageController.pairing      = Pairing.parse(dataArray)
            self.storageControllerCount.pairing += 1

        elif    header.dataType == DataType.Rssi:
            self.storageController.rssi         = Rssi.parse(dataArray)
            self.storageControllerCount.rssi    += 1


# BaseFunctions End



# Common Start


    def sendPing(self, deviceType):
        
        if  ( not isinstance(deviceType, DeviceType) ):
            return None

        header = Header()
        
        header.dataType = DataType.Ping
        header.length   = Ping.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = deviceType

        data = Ping()

        data.systemTime = 0

        return self.transfer(header, data)



    def sendRequest(self, deviceType, dataType):
    
        if  ( (not isinstance(deviceType, DeviceType)) or (not isinstance(dataType, DataType)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Request
        header.length   = Request.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = deviceType

        data = Request()

        data.dataType   = dataType

        return self.transfer(header, data)



    def sendPairing(self, deviceType, addressLocal, addressRemote, channel):
    
        if  ( (not isinstance(deviceType, DeviceType)) or
            (not isinstance(addressLocal, int)) or
            (not isinstance(addressRemote, int)) or
            (not isinstance(channel, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Pairing
        header.length   = Pairing.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = deviceType

        data = Pairing()

        data.addressLocal   = addressLocal
        data.addressRemote  = addressRemote
        data.channel        = channel

        return self.transfer(header, data)


# Common Start



# Control Start


    def sendTakeOff(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.FlightEvent
        data.option         = FlightEvent.TakeOff.value

        return self.transfer(header, data)



    def sendLanding(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.FlightEvent
        data.option         = FlightEvent.Landing.value

        return self.transfer(header, data)



    def sendStop(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.Stop
        data.option         = 0

        return self.transfer(header, data)



    def sendControl(self, roll, pitch, yaw, throttle):
        
        if  ( (not isinstance(roll, int)) or (not isinstance(pitch, int)) or (not isinstance(yaw, int)) or (not isinstance(throttle, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Control
        header.length   = ControlQuad8.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = ControlQuad8()

        data.roll       = roll
        data.pitch      = pitch
        data.yaw        = yaw
        data.throttle   = throttle

        return self.transfer(header, data)



    def sendControlWhile(self, roll, pitch, yaw, throttle, timeMs):
        
        if  ( (not isinstance(roll, int)) or (not isinstance(pitch, int)) or (not isinstance(yaw, int)) or (not isinstance(throttle, int)) ):
            return None

        timeSec     = timeMs / 1000
        timeStart   = time.time()

        while ((time.time() - timeStart) < timeSec):
            self.sendControl(roll, pitch, yaw, throttle)
            sleep(0.02)

        return self.sendControl(roll, pitch, yaw, throttle)



    def sendControlDrive(self, wheel, accel):
        
        if  ( (not isinstance(wheel, int)) or (not isinstance(accel, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Control
        header.length   = ControlDouble8.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = ControlDouble8()

        data.wheel      = wheel
        data.accel      = accel

        return self.transfer(header, data)



    def sendControlDriveWhile(self, wheel, accel, timeMs):
        
        if  ( (not isinstance(wheel, int)) or (not isinstance(accel, int)) ):
            return None

        timeSec     = timeMs / 1000
        timeStart   = time.time()

        while ((time.time() - timeStart) < timeSec):
            self.sendControlDrive(wheel, accel)
            sleep(0.02)

        return self.sendControlDrive(wheel, accel)


# Control End



# Setup Start


    def sendModeVehicle(self, modeVehicle):
        
        if  ( not isinstance(modeVehicle, ModeVehicle) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.ModeVehicle
        data.option         = modeVehicle.value

        return self.transfer(header, data)



    def sendHeadless(self, headless):
        
        if  ( not isinstance(headless, Headless) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.Headless
        data.option         = headless.value

        return self.transfer(header, data)



    def sendTrimFlight(self, roll, pitch, yaw, throttle):
        
        if  ( (not isinstance(roll, int)) or (not isinstance(pitch, int)) or (not isinstance(yaw, int)) or (not isinstance(throttle, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.TrimFlight
        header.length   = TrimFlight.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = TrimFlight()

        data.roll       = roll
        data.pitch      = pitch
        data.yaw        = yaw
        data.throttle   = throttle

        return self.transfer(header, data)



    def sendTrimDrive(self, wheel, accel):
        
        if  ( (not isinstance(wheel, int)) or (not isinstance(accel, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.TrimDrive
        header.length   = TrimDrive.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = TrimDrive()

        data.wheel      = wheel
        data.accel      = accel

        return self.transfer(header, data)



    def sendFlightEvent(self, flightEvent):
        
        if  ( (not isinstance(flightEvent, FlightEvent)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.FlightEvent
        data.option         = flightEvent.value

        return self.transfer(header, data)



    def sendDriveEvent(self, driveEvent):
        
        if  ( (not isinstance(driveEvent, DriveEvent)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.DriveEvent
        data.option         = driveEvent.value

        return self.transfer(header, data)



    def sendClearTrim(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.ClearTrim
        data.option         = 0

        return self.transfer(header, data)



    def sendClearGyroBias(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.ClearGyroBias
        data.option         = 0

        return self.transfer(header, data)


# Setup End



# Device Start

    def sendMotor(self, motor0, motor1, motor2, motor3):
        
        if  ((not isinstance(motor0, int)) or
            (not isinstance(motor1, int)) or
            (not isinstance(motor2, int)) or
            (not isinstance(motor3, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Motor
        header.length   = Motor.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = Motor()

        data.motor[0].rotation  = Rotation.Clockwise
        data.motor[0].value     = motor0

        data.motor[1].rotation  = Rotation.Counterclockwise
        data.motor[1].value     = motor1

        data.motor[2].rotation  = Rotation.Clockwise
        data.motor[2].value     = motor2

        data.motor[3].rotation  = Rotation.Counterclockwise
        data.motor[3].value     = motor3

        return self.transfer(header, data)


    def sendMotorSingle(self, target, rotation, value):
        
        if  ((not isinstance(target, int)) or
            (not isinstance(rotation, Rotation)) or
            (not isinstance(value, int))):
            return None

        header = Header()
        
        header.dataType = DataType.MotorSingle
        header.length   = MotorSingle.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = MotorSingle()

        data.target     = target
        data.rotation   = Rotation.Clockwise
        data.value      = motor0

        return self.transfer(header, data)



    def sendIrMessage(self, value):
        
        if  ((not isinstance(value, int))):
            return None

        header = Header()
        
        header.dataType = DataType.IrMessage
        header.length   = IrMessage.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Drone

        data = IrMessage()

        data.value      = value

        return self.transfer(header, data)


# Device End



# Light Start


    def sendLightManual(self, deviceType, flags, brightness):
        
        if  (((deviceType != DeviceType.Drone) and (deviceType != DeviceType.Controller)) or
            (not isinstance(flags, int)) or
            (not isinstance(brightness, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightManual
        header.length   = LightManual.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = deviceType

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



# Buzzer Start


    def sendBuzzer(self, mode, value, time):
        
        if ( (not isinstance(mode, BuzzerMode)) or (not isinstance(value, int)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = mode
        data.value      = value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerMute(self, time):
        
        if ( (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.Mute
        data.value      = BuzzerScale.Mute.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerMuteReserve(self, time):
        
        if ( (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.MuteReserve
        data.value      = BuzzerScale.Mute.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerScale(self, scale, time):
        
        if ( (not isinstance(scale, BuzzerScale)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.Scale
        data.value      = scale.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerScaleReserve(self, scale, time):
        
        if ( (not isinstance(scale, BuzzerScale)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.ScaleReserve
        data.value      = scale.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerHz(self, hz, time):
        
        if ( (not isinstance(hz, int)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.Hz
        data.value      = hz
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerHzReserve(self, hz, time):
        
        if ( (not isinstance(hz, int)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.HzReserve
        data.value      = hz
        data.time       = time

        return self.transfer(header, data)


# Buzzer End



# Vibrator Start


    def sendVibrator(self, on, off, total):
        
        if ( (not isinstance(on, int)) or (not isinstance(off, int)) or (not isinstance(total, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Vibrator
        header.length   = Vibrator.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Vibrator()

        data.mode       = VibratorMode.Instantally
        data.on         = on
        data.off        = off
        data.total      = total

        return self.transfer(header, data)



    def sendVibratorReserve(self, on, off, total):
        
        if ( (not isinstance(on, int)) or (not isinstance(off, int)) or (not isinstance(total, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Vibrator
        header.length   = Vibrator.getSize()
        header.from_    = DeviceType.Tester
        header.to_      = DeviceType.Controller
        
        data = Vibrator()

        data.mode       = VibratorMode.Continually
        data.on         = on
        data.off        = off
        data.total      = total

        return self.transfer(header, data)


# Vibrator End

