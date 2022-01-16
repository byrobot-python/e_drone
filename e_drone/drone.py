import serial
import binascii
import random
import queue
import threading
from threading import Thread
from time import sleep
from struct import *
import time
from serial.tools.list_ports import comports
from queue import Queue
from operator import eq
import colorama
from colorama import Fore, Back, Style

from e_drone.protocol import *
from e_drone.storage import *
from e_drone.receiver import *
from e_drone.system import *
from e_drone.crc import *



def convertByteArrayToString(dataArray):

    if dataArray == None:
        return ""

    string = ""

    if (isinstance(dataArray, bytes)) or (isinstance(dataArray, bytearray)) or (not isinstance(dataArray, list)):
        for data in dataArray:
            string += "{0:02X} ".format(data)

    return string



class Drone:

# BaseFunctions Start

    def __init__(self, flagCheckBackground = True, flagShowErrorMessage = False, flagShowLogMessage = False, flagShowTransferData = False, flagShowReceiveData = False):
        
        self._serialport                = None
        self._bufferQueue               = Queue(4096)
        self._bufferHandler             = bytearray()
        self._index                     = 0

        self._thread                    = None
        self._flagThreadRun             = False

        self._receiver                  = Receiver()

        self._flagCheckBackground       = flagCheckBackground

        self._flagShowErrorMessage      = flagShowErrorMessage
        self._flagShowLogMessage        = flagShowLogMessage
        self._flagShowTransferData      = flagShowTransferData
        self._flagShowReceiveData       = flagShowReceiveData

        self._eventHandler              = EventHandler()
        self._storageHeader             = StorageHeader()
        self._storage                   = Storage()
        self._storageCount              = StorageCount()
        self._parser                    = Parser()

        self._devices                   = []            # 자동 연결 시 검색된 장치 목록을 저장
        self._flagDiscover              = False         # 자동 연결 시 장치를 검색중인지를 표시
        self._flagConnected             = False         # 자동 연결 시 장치와 연결되었는지를 알려줌

        self.timeStartProgram           = time.time()           # 프로그램 시작 시각 기록

        self.systemTimeMonitorData      = 0
        self.monitorData                = []

        for i in range(0, 36):
            self.monitorData.append(i)

        colorama.init()



    def __del__(self):
        
        self.close()



    def _receiving(self):
        while self._flagThreadRun:
            
            self._bufferQueue.put(self._serialport.read())

            # 수신 데이터 백그라운드 확인이 활성화 된 경우 데이터 자동 업데이트
            if self._flagCheckBackground == True:
                while self.check() != DataType.None_:
                    pass

            #sleep(0.001)



    def isOpen(self):
        if self._serialport != None:
            return self._serialport.isOpen()
        else:
            return False



    def isConnected(self):
        if self.isOpen() == False:
            return False
        else:
            return self._flagConnected



    def open(self, portname = "None"):
        if eq(portname, "None"):
            nodes = comports()
            size = len(nodes)
            if size > 0:
                portname = nodes[size - 1].device
            else:
                return False

        try:

            self._serialport = serial.Serial(
                port        = portname,
                baudrate    = 57600)

            if( self.isOpen() ):
                self._flagThreadRun = True
                self._thread = Thread(target=self._receiving, args=(), daemon=True)
                self._thread.start()

                # 로그 출력
                self._printLog("Connected.({0})".format(portname))

                return True
            else:
                # 오류 메세지 출력
                self._printError("Could not connect to device.")

                return False

        except:
                # 오류 메세지 출력
                self._printError("Could not connect to device.")

                return False



    def close(self):
        # 로그 출력
        if self.isOpen():
            self._printLog("Closing serial port.")

        self._printLog("Thread Flag False.")

        if self._flagThreadRun == True:
            self._flagThreadRun = False
            sleep(0.1)
        
        self._printLog("Thread Join.")

        if self._thread != None:
            self._thread.join(timeout=1)

        self._printLog("Port Close.")

        if self.isOpen() == True:
            self._serialport.close()
            sleep(0.2)



    def makeTransferDataArray(self, header, data):
        if (header == None) or (data == None):
            return None

        if (not isinstance(header, Header)):
            return None

        if (isinstance(data, ISerializable)):
            data = data.toArray()

        crc16 = CRC16.calc(header.toArray(), 0)
        crc16 = CRC16.calc(data, crc16)

        dataArray = bytearray()
        dataArray.extend((0x0A, 0x55))
        dataArray.extend(header.toArray())
        dataArray.extend(data)
        dataArray.extend(pack('H', crc16))

        return dataArray



    def transfer(self, header, data):
        if not self.isOpen():
            return

        dataArray = self.makeTransferDataArray(header, data)

        self._serialport.write(dataArray)

        # 송신 데이터 출력
        self._printTransferData(dataArray)

        return dataArray



    def check(self):
        while self._bufferQueue.empty() == False:
            dataArray = self._bufferQueue.get_nowait()
            self._bufferQueue.task_done()

            if (dataArray != None) and (len(dataArray) > 0):
                # 수신 데이터 출력
                self._printReceiveData(dataArray)

                self._bufferHandler.extend(dataArray)

        while len(self._bufferHandler) > 0:
            stateLoading = self._receiver.call(self._bufferHandler.pop(0))

            # 오류 출력
            if stateLoading == StateLoading.Failure:
                # 수신 데이터 출력(줄넘김)
                self._printReceiveDataEnd()

                # 오류 메세지 출력
                self._printError(self._receiver.message)
                

            # 로그 출력
            if stateLoading == StateLoading.Loaded:
                # 수신 데이터 출력(줄넘김)
                self._printReceiveDataEnd()

                # 로그 출력
                self._printLog(self._receiver.message)

            if self._receiver.state == StateLoading.Loaded:
                self._handler(self._receiver.header, self._receiver.data)
                return self._receiver.header.dataType

        return DataType.None_



    def checkDetail(self):
        while self._bufferQueue.empty() == False:
            dataArray = self._bufferQueue.get_nowait()
            self._bufferQueue.task_done()

            if (dataArray != None) and (len(dataArray) > 0):
                # 수신 데이터 출력
                self._printReceiveData(dataArray)

                self._bufferHandler.extend(dataArray)

        while len(self._bufferHandler) > 0:
            stateLoading = self._receiver.call(self._bufferHandler.pop(0))

            # 오류 출력
            if stateLoading == StateLoading.Failure:
                # 수신 데이터 출력(줄넘김)
                self._printReceiveDataEnd()

                # 오류 메세지 출력
                self._printError(self._receiver.message)
                

            # 로그 출력
            if stateLoading == StateLoading.Loaded:
                # 수신 데이터 출력(줄넘김)
                self._printReceiveDataEnd()

                # 로그 출력
                self._printLog(self._receiver.message)

            if self._receiver.state == StateLoading.Loaded:
                self._handler(self._receiver.header, self._receiver.data)
                return self._receiver.header, self._receiver.data

        return None, None



    def _handler(self, header, dataArray):

        # 들어오는 데이터를 저장
        self._runHandler(header, dataArray)

        # 콜백 이벤트 실행
        self._runEventHandler(header.dataType)

        # Monitor 데이터 처리
        self._runHandlerForMonitor(header, dataArray)

        # 데이터 처리 완료 확인
        self._receiver.checked()

        return header.dataType



    def _runHandler(self, header, dataArray):
        
        # 일반 데이터 처리
        if self._parser.d[header.dataType] != None:
            self._storageHeader.d[header.dataType]   = header
            self._storage.d[header.dataType]         = self._parser.d[header.dataType](dataArray)
            self._storageCount.d[header.dataType]    += 1



    def _runEventHandler(self, dataType):
        if (isinstance(dataType, DataType)) and (self._eventHandler.d[dataType] != None) and (self._storage.d[dataType] != None):
            return self._eventHandler.d[dataType](self._storage.d[dataType])
        else:
            return None



    def _runHandlerForMonitor(self, header, dataArray):
        
        # Monitor 데이터 처리
        # 수신 받은 데이터를 파싱하여 self.monitorData[] 배열에 데이터를 넣음
        if header.dataType == DataType.Monitor:
            
            monitorHeaderType = MonitorHeaderType(dataArray[0])

            if monitorHeaderType == MonitorHeaderType.Monitor0:
                
                monitor0 = Monitor0.parse(dataArray[1:1 + Monitor0.getSize()])

                if monitor0.monitorDataType == MonitorDataType.F32:
                    
                    dataCount = (dataArray.len() - 1 - Monitor0.getSize()) / 4

                    for i in range(0, dataCount):
                        
                        if monitor0.index + i < len(self.monitorData):
                            
                            index = 1 + Monitor0.getSize() + (i * 4)
                            self.monitorData[monitor0.index + i], = unpack('<f', dataArray[index:index + 4])

            elif monitorHeaderType == MonitorHeaderType.Monitor4:
                
                monitor4 = Monitor4.parse(dataArray[1:1 + Monitor4.getSize()])

                if monitor4.monitorDataType == MonitorDataType.F32:
                    
                    self.systemTimeMonitorData = monitor4.systemTime
                    
                    dataCount = (dataArray.len() - 1 - Monitor4.getSize()) / 4

                    for i in range(0, dataCount):
                        
                        if monitor4.index + i < len(self.monitorData):
                            
                            index = 1 + Monitor4.getSize() + (i * 4)
                            self.monitorData[monitor4.index + i], = unpack('<f', dataArray[index:index + 4])

            elif monitorHeaderType == MonitorHeaderType.Monitor8:
                
                monitor8 = Monitor8.parse(dataArray[1:1 + Monitor8.getSize()])

                if monitor8.monitorDataType == MonitorDataType.F32:
                    
                    self.systemTimeMonitorData = monitor8.systemTime
                    
                    dataCount = (dataArray.len() - 1 - Monitor8.getSize()) / 4

                    for i in range(0, dataCount):
                        
                        if monitor8.index + i < len(self.monitorData):
                            
                            index = 1 + Monitor8.getSize() + (i * 4)
                            self.monitorData[monitor8.index + i], = unpack('<f', dataArray[index:index + 4])



    def setEventHandler(self, dataType, eventHandler):
        
        if (not isinstance(dataType, DataType)):
            return

        self._eventHandler.d[dataType] = eventHandler



    def getHeader(self, dataType):
    
        if (not isinstance(dataType, DataType)):
            return None

        return self._storageHeader.d[dataType]



    def getData(self, dataType):

        if (not isinstance(dataType, DataType)):
            return None

        return self._storage.d[dataType]



    def getCount(self, dataType):

        if (not isinstance(dataType, DataType)):
            return None

        return self._storageCount.d[dataType]



    def _printLog(self, message):
        
        # 로그 출력
        if self._flagShowLogMessage and message != None:
            print(Fore.GREEN + "[{0:10.03f}] {1}".format((time.time() - self.timeStartProgram), message) + Style.RESET_ALL)



    def _printError(self, message):
    
        # 오류 메세지 출력
        if self._flagShowErrorMessage and message != None:
            print(Fore.RED + "[{0:10.03f}] {1}".format((time.time() - self.timeStartProgram), message) + Style.RESET_ALL)



    def _printTransferData(self, dataArray):
    
        # 송신 데이터 출력
        if (self._flagShowTransferData) and (dataArray != None) and (len(dataArray) > 0):
            print(Back.YELLOW + Fore.BLACK + convertByteArrayToString(dataArray) + Style.RESET_ALL)



    def _printReceiveData(self, dataArray):
        
        # 수신 데이터 출력
        if (self._flagShowReceiveData) and (dataArray != None) and (len(dataArray) > 0):
            print(Back.CYAN + Fore.BLACK + convertByteArrayToString(dataArray) + Style.RESET_ALL, end='')



    def _printReceiveDataEnd(self):
        
        # 수신 데이터 출력(줄넘김)
        if self._flagShowReceiveData:
            print("")




# BaseFunctions End



# Common Start


    def sendPing(self, deviceType):
        
        if  ( not isinstance(deviceType, DeviceType) ):
            return None

        header = Header()
        
        header.dataType = DataType.Ping
        header.length   = Ping.getSize()
        header.from_    = DeviceType.Base
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
        header.from_    = DeviceType.Base
        header.to_      = deviceType

        data = Request()

        data.dataType   = dataType

        return self.transfer(header, data)



    def sendPairing(self, deviceType, address0, address1, address2, scramble, channel0, channel1, channel2, channel3):
    
        if  ( (not isinstance(deviceType, DeviceType)) or
            (not isinstance(address0, int)) or
            (not isinstance(address1, int)) or
            (not isinstance(address2, int)) or
            (not isinstance(scramble, int)) or
            (not isinstance(channel0, int)) or
            (not isinstance(channel1, int)) or
            (not isinstance(channel2, int)) or
            (not isinstance(channel3, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Pairing
        header.length   = Pairing.getSize()
        header.from_    = DeviceType.Base
        header.to_      = deviceType

        data = Pairing()

        data.address0   = address0
        data.address1   = address1
        data.address2   = address2
        data.scramble   = scramble
        data.channel0   = channel0
        data.channel1   = channel1
        data.channel2   = channel2
        data.channel3   = channel3

        return self.transfer(header, data)


# Common Start



# Control Start


    def sendTakeOff(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.FlightEvent
        data.option         = FlightEvent.TakeOff.value

        return self.transfer(header, data)



    def sendLanding(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.FlightEvent
        data.option         = FlightEvent.Landing.value

        return self.transfer(header, data)



    def sendStop(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
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
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = ControlQuad8()

        data.roll       = roll
        data.pitch      = pitch
        data.yaw        = yaw
        data.throttle   = throttle

        return self.transfer(header, data)



    def sendControlWhile(self, roll, pitch, yaw, throttle, timeMs):
        
        if ((not isinstance(roll, int))     or
            (not isinstance(pitch, int))    or
            (not isinstance(yaw, int))      or
            (not isinstance(throttle, int)) ):
            return None

        timeSec     = timeMs / 1000
        timeStart   = time.perf_counter()

        while ((time.perf_counter() - timeStart) < timeSec):
            self.sendControl(roll, pitch, yaw, throttle)
            sleep(0.02)

        return self.sendControl(roll, pitch, yaw, throttle)



    def sendControlPosition16(self, positionX, positionY, positionZ, velocity, heading, rotationalVelocity):
        
        if ((not isinstance(positionX, int)) or
            (not isinstance(positionY, int)) or
            (not isinstance(positionZ, int)) or
            (not isinstance(velocity, int))):
            return None

        if ((not isinstance(heading, int)) or
            (not isinstance(rotationalVelocity, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Control
        header.length   = ControlPosition16.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = ControlPosition16()

        data.positionX          = positionX
        data.positionY          = positionY
        data.positionZ          = positionZ
        data.velocity           = velocity
        data.heading            = heading
        data.rotationalVelocity = rotationalVelocity

        return self.transfer(header, data)



    def sendControlPosition(self, positionX, positionY, positionZ, velocity, heading, rotationalVelocity):
        
        if  (not (isinstance(positionX, float) or isinstance(positionX, int))):
            return None

        if  (not (isinstance(positionY, float) or isinstance(positionY, int))):
            return None

        if  (not (isinstance(positionZ, float) or isinstance(positionZ, int))):
            return None

        if  (not (isinstance(velocity, float) or isinstance(velocity, int))):
            return None

        if  ( (not isinstance(heading, int)) or (not isinstance(rotationalVelocity, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Control
        header.length   = ControlPosition.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = ControlPosition()

        data.positionX          = float(positionX)
        data.positionY          = float(positionY)
        data.positionZ          = float(positionZ)
        data.velocity           = float(velocity)
        data.heading            = heading
        data.rotationalVelocity = rotationalVelocity

        return self.transfer(header, data)


# Control End



# Setup Start


    def sendCommand(self, commandType, option = 0):
        
        if ((not isinstance(commandType, CommandType)) or
            (not isinstance(option, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = commandType
        data.option         = option

        return self.transfer(header, data)



    def sendCommandLightEvent(self, commandType, option, lightEvent, interval, repeat):
        
        if ((not isinstance(commandType, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = CommandLightEvent.getSize()
        header.from_    = DeviceType.Base

        data = CommandLightEvent()

        if      isinstance(lightEvent, LightModeDrone):
            header.to_          = DeviceType.Drone
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, LightModeController):
            header.to_          = DeviceType.Controller
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, int):
            header.to_          = DeviceType.Drone
            data.event.event    = lightEvent

        else:
            return None

        data.command.commandType    = commandType
        data.command.option         = option

        data.event.interval = interval
        data.event.repeat   = repeat

        return self.transfer(header, data)



    def sendCommandLightEventColor(self, commandType, option, lightEvent, interval, repeat, r, g, b):
        
        if ((not isinstance(commandType, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = CommandLightEventColor.getSize()
        header.from_    = DeviceType.Base

        data = CommandLightEventColor()

        if        isinstance(lightEvent, LightModeDrone):
            header.to_          = DeviceType.Drone
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, LightModeController):
            header.to_          = DeviceType.Controller
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, int):
            header.to_          = DeviceType.Drone
            data.event.event    = lightEvent

        else:
            return None

        data.command.commandType    = commandType
        data.command.option         = option

        data.event.interval         = interval
        data.event.repeat           = repeat

        data.color.r                = r
        data.color.g                = g
        data.color.b                = b

        return self.transfer(header, data)



    def sendCommandLightEventColors(self, commandType, option, lightEvent, interval, repeat, colors):
        
        if ((not isinstance(commandType, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(interval, int))  or
            (not isinstance(repeat, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = CommandLightEventColors.getSize()
        header.from_    = DeviceType.Base

        data = CommandLightEventColors()

        if        isinstance(lightEvent, LightModeDrone):
            header.to_          = DeviceType.Drone
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, LightModeController):
            header.to_          = DeviceType.Controller
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, int):
            header.to_          = DeviceType.Drone
            data.event.event    = lightEvent

        else:
            return None


        data.command.commandType    = commandType
        data.command.option         = option

        data.event.interval         = interval
        data.event.repeat           = repeat

        data.colors                 = colors

        return self.transfer(header, data)



    def sendModeControlFlight(self, modeControlFlight):
        
        if  ( not isinstance(modeControlFlight, ModeControlFlight) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.ModeControlFlight
        data.option         = modeControlFlight.value

        return self.transfer(header, data)



    def sendHeadless(self, headless):
        
        if  ( not isinstance(headless, Headless) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.Headless
        data.option         = headless.value

        return self.transfer(header, data)



    def sendTrim(self, roll, pitch, yaw, throttle):
        
        if  ( (not isinstance(roll, int)) or (not isinstance(pitch, int)) or (not isinstance(yaw, int)) or (not isinstance(throttle, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Trim
        header.length   = Trim.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Trim()

        data.roll       = roll
        data.pitch      = pitch
        data.yaw        = yaw
        data.throttle   = throttle

        return self.transfer(header, data)



    def sendWeight(self, weight):
        
        header = Header()
        
        header.dataType = DataType.Weight
        header.length   = Weight.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Weight()

        data.weight     = weight

        return self.transfer(header, data)



    def sendLostConnection(self, timeNeutral, timeLanding, timeStop):
        
        header = Header()
        
        header.dataType = DataType.LostConnection
        header.length   = LostConnection.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = LostConnection()

        data.timeNeutral    = timeNeutral
        data.timeLanding    = timeLanding
        data.timeStop       = timeStop

        return self.transfer(header, data)



    def sendFlightEvent(self, flightEvent):
        
        if  ( (not isinstance(flightEvent, FlightEvent)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.FlightEvent
        data.option         = flightEvent.value

        return self.transfer(header, data)



    def sendClearBias(self):
        
        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = Command()

        data.commandType    = CommandType.ClearBias
        data.option         = 0

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



    def sendSetDefault(self, deviceType):
        
        if ((not isinstance(deviceType, DeviceType))):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = deviceType

        data = Command()

        data.commandType    = CommandType.SetDefault
        data.option         = 0

        return self.transfer(header, data)



    def sendBacklight(self, flagPower):
        
        if ((not isinstance(flagPower, bool))):
            return None

        header = Header()
        
        header.dataType = DataType.Command
        header.length   = Command.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller

        data = Command()

        data.commandType    = CommandType.Backlight
        data.option         = int(flagPower)

        return self.transfer(header, data)


# Setup End



# Device Start


    def sendMotor(self, motor0, motor1, motor2, motor3):
        
        if ((not isinstance(motor0, int)) or
            (not isinstance(motor1, int)) or
            (not isinstance(motor2, int)) or
            (not isinstance(motor3, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Motor
        header.length   = Motor.getSize()
        header.from_    = DeviceType.Base
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
        
        if ((not isinstance(target, int)) or
            (not isinstance(rotation, Rotation)) or
            (not isinstance(value, int))):
            return None

        header = Header()
        
        header.dataType = DataType.MotorSingle
        header.length   = MotorSingle.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Drone

        data = MotorSingle()

        data.target     = target
        data.rotation   = rotation
        data.value      = value

        return self.transfer(header, data)


# Device End



# Light Start


    def sendLightManual(self, deviceType, flags, brightness):
        
        if ((not isinstance(deviceType, DeviceType)) or
            (not isinstance(flags, int)) or
            (not isinstance(brightness, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightManual
        header.length   = LightManual.getSize()
        header.from_    = DeviceType.Base
        header.to_      = deviceType

        data = LightManual()

        data.flags      = flags
        data.brightness = brightness

        return self.transfer(header, data)



    def sendLightModeColor(self, lightMode, interval, r, g, b):
        
        if ((not isinstance(lightMode, int)) or
            (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightMode
        header.length   = LightModeColor.getSize()
        header.from_    = DeviceType.Base

        data = LightModeColor()

        if        isinstance(lightMode, LightModeDrone):
            header.to_         = DeviceType.Drone
            data.mode.mode  = lightMode.value

        elif    isinstance(lightMode, LightModeController):
            header.to_         = DeviceType.Controller
            data.mode.mode  = lightMode.value

        elif    isinstance(lightMode, int):
            header.to_         = DeviceType.Drone
            data.mode.mode  = lightMode

        else:
            return None

        data.mode.interval  = interval

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)



    def sendLightModeColors(self, lightMode, interval, colors):
        
        if ((not isinstance(interval, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.dataType = DataType.LightMode
        header.length   = LightModeColors.getSize()
        header.from_    = DeviceType.Base

        data = LightModeColors()

        if        isinstance(lightMode, LightModeDrone):
            header.to_         = DeviceType.Drone
            data.mode.mode  = lightMode.value

        elif    isinstance(lightMode, LightModeController):
            header.to_         = DeviceType.Controller
            data.mode.mode  = lightMode.value

        elif    isinstance(lightMode, int):
            header.to_         = DeviceType.Drone
            data.mode.mode  = lightMode

        else:
            return None

        data.mode.interval  = interval
        data.colors         = colors

        return self.transfer(header, data)



    def sendLightEventColor(self, lightEvent, interval, repeat, r, g, b):
        
        if ((not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEvent
        header.length   = LightEventColor.getSize()
        header.from_    = DeviceType.Base

        data = LightEventColor()

        if        isinstance(lightEvent, LightModeDrone):
            header.to_             = DeviceType.Drone
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, LightModeController):
            header.to_             = DeviceType.Controller
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, int):
            header.to_             = DeviceType.Drone
            data.event.event    = lightEvent

        else:
            return None

        data.event.interval = interval
        data.event.repeat   = repeat

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)



    def sendLightEventColors(self, lightEvent, interval, repeat, colors):
        
        if ((not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.dataType = DataType.LightEvent
        header.length   = LightEventColors.getSize()
        header.from_    = DeviceType.Base

        data = LightEventColors()

        if        isinstance(lightEvent, LightModeDrone):
            header.to_             = DeviceType.Drone
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, LightModeController):
            header.to_             = DeviceType.Controller
            data.event.event    = lightEvent.value

        elif    isinstance(lightEvent, int):
            header.to_             = DeviceType.Drone
            data.event.event    = lightEvent

        else:
            return None

        data.event.interval = interval
        data.event.repeat   = repeat

        data.colors         = colors

        return self.transfer(header, data)



    def sendLightDefaultColor(self, lightMode, interval, r, g, b):
        
        if ((not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.dataType = DataType.LightDefault
        header.length   = LightModeColor.getSize()
        header.from_    = DeviceType.Base

        data = LightModeColor()

        if        isinstance(lightMode, LightModeDrone):
            header.to_         = DeviceType.Drone
            data.mode.mode  = lightMode.value

        elif    isinstance(lightMode, LightModeController):
            header.to_         = DeviceType.Controller
            data.mode.mode  = lightMode.value

        elif    isinstance(lightMode, int):
            header.to_         = DeviceType.Drone
            data.mode.mode  = lightMode

        else:
            return None

        data.mode.interval  = interval

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)



# Light End



# Display Start


    def sendDisplayClearAll(self, pixel = DisplayPixel.Black):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayClear
        header.length   = DisplayClearAll.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = DisplayClearAll()

        data.pixel      = pixel

        return self.transfer(header, data)
    


    def sendDisplayClear(self, x, y, width, height, pixel = DisplayPixel.Black):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayClear
        header.length   = DisplayClear.getSize()
        header.from_    = DeviceType.Base
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
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = DisplayInvert()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height

        return self.transfer(header, data)



    def sendDisplayDrawPoint(self, x, y, pixel = DisplayPixel.White):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawPoint
        header.length   = DisplayDrawPoint.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawPoint()

        data.x          = x
        data.y          = y
        data.pixel      = pixel

        return self.transfer(header, data)



    def sendDisplayDrawLine(self, x1, y1, x2, y2, pixel = DisplayPixel.White, line = DisplayLine.Solid):
        
        if ( (not isinstance(pixel, DisplayPixel)) or (not isinstance(line, DisplayLine)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawLine
        header.length   = DisplayDrawLine.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawLine()

        data.x1         = x1
        data.y1         = y1
        data.x2         = x2
        data.y2         = y2
        data.pixel      = pixel
        data.line       = line

        return self.transfer(header, data)



    def sendDisplayDrawRect(self, x, y, width, height, pixel = DisplayPixel.White, flagFill = False, line = DisplayLine.Solid):
        
        if ( (not isinstance(pixel, DisplayPixel)) or (not isinstance(flagFill, bool)) or (not isinstance(line, DisplayLine)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawRect
        header.length   = DisplayDrawRect.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawRect()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height
        data.pixel      = pixel
        data.flagFill   = flagFill
        data.line       = line

        return self.transfer(header, data)



    def sendDisplayDrawCircle(self, x, y, radius, pixel = DisplayPixel.White, flagFill = True):
        
        if ( (not isinstance(pixel, DisplayPixel)) or (not isinstance(flagFill, bool)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawCircle
        header.length   = DisplayDrawCircle.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawCircle()

        data.x          = x
        data.y          = y
        data.radius     = radius
        data.pixel      = pixel
        data.flagFill   = flagFill

        return self.transfer(header, data)



    def sendDisplayDrawString(self, x, y, message, font = DisplayFont.LiberationMono5x8, pixel = DisplayPixel.White):
        
        if ( (not isinstance(font, DisplayFont)) or (not isinstance(pixel, DisplayPixel)) or (not isinstance(message, str)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawString
        header.length   = DisplayDrawString.getSize() + len(message)
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = DisplayDrawString()

        data.x          = x
        data.y          = y
        data.font       = font
        data.pixel      = pixel
        data.message    = message

        return self.transfer(header, data)



    def sendDisplayDrawStringAlign(self, x_start, x_end, y, message, align = DisplayAlign.Center, font = DisplayFont.LiberationMono5x8, pixel = DisplayPixel.White):
        
        if ( (not isinstance(align, DisplayAlign)) or (not isinstance(font, DisplayFont)) or (not isinstance(pixel, DisplayPixel)) or (not isinstance(message, str)) ):
            return None

        header = Header()
        
        header.dataType = DataType.DisplayDrawStringAlign
        header.length   = DisplayDrawStringAlign.getSize() + len(message)
        header.from_    = DeviceType.Base
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
        
        if ((not isinstance(mode, BuzzerMode)) or
            (not isinstance(value, int)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = mode
        data.value      = value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerMute(self, time):
        
        if (not isinstance(time, int)):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.Mute
        data.value      = BuzzerScale.Mute.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerMuteReserve(self, time):
        
        if (not isinstance(time, int)):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.MuteReserve
        data.value      = BuzzerScale.Mute.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerScale(self, scale, time):
        
        if ((not isinstance(scale, BuzzerScale)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.Scale
        data.value      = scale.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerScaleReserve(self, scale, time):
        
        if ((not isinstance(scale, BuzzerScale)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.ScaleReserve
        data.value      = scale.value
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerHz(self, hz, time):
        
        if ((not isinstance(hz, int)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.Hz
        data.value      = hz
        data.time       = time

        return self.transfer(header, data)



    def sendBuzzerHzReserve(self, hz, time):
        
        if ((not isinstance(hz, int)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Buzzer()

        data.mode       = BuzzerMode.HzReserve
        data.value      = hz
        data.time       = time

        return self.transfer(header, data)


# Buzzer End



# Vibrator Start


    def sendVibrator(self, on, off, total):
        
        if ((not isinstance(on, int)) or
            (not isinstance(off, int)) or
            (not isinstance(total, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Vibrator
        header.length   = Vibrator.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Vibrator()

        data.mode       = VibratorMode.Instantally
        data.on         = on
        data.off        = off
        data.total      = total

        return self.transfer(header, data)



    def sendVibratorReserve(self, on, off, total):
        
        if ((not isinstance(on, int)) or
            (not isinstance(off, int)) or
            (not isinstance(total, int))):
            return None

        header = Header()
        
        header.dataType = DataType.Vibrator
        header.length   = Vibrator.getSize()
        header.from_    = DeviceType.Base
        header.to_      = DeviceType.Controller
        
        data = Vibrator()

        data.mode       = VibratorMode.Continually
        data.on         = on
        data.off        = off
        data.total      = total

        return self.transfer(header, data)


# Vibrator End



# Update Start




# Update End
