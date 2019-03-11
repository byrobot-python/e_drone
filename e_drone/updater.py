import os
import abc 
import numpy as np
from struct import *
from enum import Enum
from urllib.request import urlopen
from time import sleep

from e_drone.drone import *


# Firmware Start


class FirmwareHeader():

    def __init__(self):
        self.modelNumber        = 0
        self.version            = 0
        self.length             = 0

        self.year               = 0
        self.month              = 0
        self.day                = 0

        self.versionMajor       = 0
        self.versionMinor       = 0
        self.versionBuild       = 0


    @classmethod
    def getSize(cls):
        return 16


    @classmethod
    def parse(cls, dataArray):
        data = FirmwareHeader()
        
        if len(dataArray) != cls.getSize():
            return None
        
        data.modelNumber, data.version, data.length, data.year, data.month, data.day = unpack('<IIIHBB', dataArray)

        data.modelNumber = ModelNumber(data.modelNumber)

        data.versionMajor = (data.version >> 24) & 0xFF
        data.versionMinor = (data.version >> 16) & 0xFF
        data.versionBuild = (data.version & 0xFFFF)

        return data



class Firmware():

    def __init__(self, url = None):

        if url == None:
            self.url            = 0         # 펌웨어 URL
            self.resource       = None      # 펌웨어 전체 파일
            self.header         = None      # 펌웨어 헤더
            self.length         = 0         # 펌웨어 전체 파일의 길이

            self.rawHeader      = None      # 헤더 배열
            self.stringHeader   = None      # 헤더 배열을 HEX 문자열로 변환한 것
        else:
            self.open(url)


    def open(self, url):

        self.url = url
        
        with urlopen(self.url) as res:
            self.resource   = res.read()
            self.length     = len(self.resource)
            self.rawHeader  = self.resource[0:16]
            self.header     = FirmwareHeader.parse(self.rawHeader)

            self.stringHeader = ""
            for data in self.rawHeader:
                self.stringHeader += "{0:02X} ".format(data)

            print("* {0}".format(self.header.modelNumber))
            print("  Header Hex : {0}".format(self.stringHeader))
            print("   File Size : {0} bytes".format(self.length))
            print("     Version : {0}.{1}.{2}".format(self.header.versionMajor, self.header.versionMinor, self.header.versionBuild))
            print("        Date : {0}.{1}.{2}".format(self.header.year, self.header.month, self.header.day))
            print("      Length : {0}\n".format(self.header.length))


# Firmware End




# Updater Start

targetModelNumber   = None
modeUpdate          = ModeUpdate.None_
indexBlockNext      = 0
flagUpdated         = False
flagUpdateComplete  = False


def eventInformation(information):
    global targetModelNumber
    global modeUpdate
    global flagUpdated
    global flagUpdateComplete

    modeUpdate          = information.modeUpdate
    flagUpdated         = True
    targetModelNumber   = information.modelNumber
    if information.modeUpdate == ModeUpdate.Complete:
        flagUpdateComplete = True
    print("* eventInformation()")
    print("  Model Number : {0}".format(information.modelNumber))
    print("       Version : {0}.{1}.{2} ({3} / 0x{3:08X})\n".format(information.version.major, information.version.minor, information.version.build, information.version.v))
    print("   Mode Update : {0}".format(information.modeUpdate))


def eventUpdateLocation(updateLocation):
    global indexBlockNext
    indexBlockNext = updateLocation.indexBlockNext
    print("* eventUpdateLocation({0})\n".format(updateLocation.indexBlockNext))


if __name__ == '__main__':

    firmware = []
    firmware.append(Firmware("https://s3.ap-northeast-2.amazonaws.com/byrobot/fw_drone_4_drone_p5_latest.eb"))
    firmware.append(Firmware("https://s3.ap-northeast-2.amazonaws.com/byrobot/fw_drone_4_controller_p2_latest.eb"))

    print("E-Drone Firmware updater\n")

    drone = Drone()
    drone.open()

    # 이벤트 핸들링 함수 등록
    drone.setEventHandler(DataType.Information, eventInformation)
    drone.setEventHandler(DataType.UpdateLocation, eventUpdateLocation)

    # Range 정보 요청
    flagRun         = True
    countRequest    = 0
    countError      = 0
    timeTransfer    = 0
    
    # 헤더 만들기
    header = Header()
    header.dataType = DataType.Update
    header.length   = 18
    header.from_    = DeviceType.Updater
    header.to_      = DeviceType.Drone

    drone.sendRequest(DeviceType.Drone, DataType.Information)
    sleep(0.2)

    drone.sendRequest(DeviceType.Controller, DataType.Information)
    sleep(0.2)

    print("targetModelNumber : {0}\n".format(targetModelNumber))

    for fw in firmware:

        print("fw : {0}\n".format(fw.header.modelNumber))

        if targetModelNumber == fw.header.modelNumber:

            # 펌웨어의 모델 번호와 일치하는 드론이 있는 경우
            print("{0}\n".format(targetModelNumber))

            if modeUpdate == ModeUpdate.Ready or modeUpdate == ModeUpdate.Update:

                print("modeUpdate == ModeUpdate.Ready or modeUpdate == ModeUpdate.Update\n")

                header.to_ = DeviceType.Drone

                while flagRun:

                    now = time.time() * 1000

                    if now - timeTransfer > 20:
                        countError = countError + 1
                        
                        print("Error : {0}".format(countError))

                        # 오류가 과도하게 누적된 경우 업데이트 취소
                        if countError > 20:
                            print("Too much not response.")
                            flagRun = False


                    if (flagUpdated == True) or (now - timeTransfer > 20):

                        index = indexBlockNext * 16

                        # 업데이트 할 위치를 넘어서는 경우 종료
                        if index + 16 > fw.length:
                            print("Index over.")
                            flagRun = False
                            break

                        # 업데이트가 완료된 경우 종료
                        if flagUpdateComplete == True:
                            print("Update complete.")
                            flagRun = False
                            break

                        data = bytearray(2)
                        data[0] = indexBlockNext & 0xFF
                        data[1] = (indexBlockNext >> 8) & 0xFF
                        data.extend(fw.resource[index : index + 16])
                        drone.transfer(header, data)
                        
                        flagUpdated     = False
                        timeTransfer    = now
            else:
                print("Firmware update is not available.")

    print("Bye.")

    drone.close()


# Updater End

