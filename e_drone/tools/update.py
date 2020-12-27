import os
import abc
import sys
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

            print(Fore.CYAN + "  - {0}".format(self.header.modelNumber) + Style.RESET_ALL)
            print("    Header Hex : {0}".format(self.stringHeader))
            print("     File Size : {0} bytes".format(self.length))
            print("       Version : {0}.{1}.{2}".format(self.header.versionMajor, self.header.versionMinor, self.header.versionBuild))
            print("          Date : {0}.{1}.{2}".format(self.header.year, self.header.month, self.header.day))
            print("        Length : {0}\n".format(self.header.length))


# Firmware End




# Updater Start

class Updater:


    def __init__(self):

        self.modelNumber        = None
        self.deviceType         = None
        self.modeUpdate         = ModeUpdate.None_
        self.indexBlockNext     = 0
        self.flagUpdated        = False
        self.flagUpdateComplete = False



    def eventInformation(self, information):

        self.modeUpdate         = information.modeUpdate
        self.flagUpdated        = True
        self.modelNumber        = information.modelNumber
        self.deviceType         = DeviceType(((self.modelNumber.value >> 8) & 0xFF))
        
        if information.modeUpdate == ModeUpdate.Complete:
            self.flagUpdateComplete = True
        else:
            print(Fore.YELLOW + "* Connected Device : {0}".format(self.deviceType) + Style.RESET_ALL)
            print("  Model Number : {0}".format(information.modelNumber))
            print("       Version : {0}.{1}.{2} ({3} / 0x{3:08X})".format(information.version.major, information.version.minor, information.version.build, information.version.v))
            print("  Release Date : {0}.{1}.{2}".format(information.year, information.month, information.day))
            print("   Mode Update : {0}\n".format(information.modeUpdate))



    def eventUpdateLocation(self, updateLocation):

        self.flagUpdated        = True
        self.indexBlockNext     = updateLocation.indexBlockNext
        #print("* eventUpdateLocation({0})\n".format(updateLocation.indexBlockNext))



    def update(self):

        colorama.init()

        print(Back.WHITE + Fore.BLUE + " FIRMWARE UPGRADE " + Style.RESET_ALL)
        print("")

        print(Fore.YELLOW + "* Firmware loading." + Style.RESET_ALL)
        print("")
        
        firmware = []
        firmware.append(Firmware("https://s3.ap-northeast-2.amazonaws.com/byrobot/fw_drone_4_drone_p5_latest.eb"))
        firmware.append(Firmware("https://s3.ap-northeast-2.amazonaws.com/byrobot/fw_drone_4_controller_p2_latest.eb"))

        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)


        # 이벤트 핸들링 함수 등록
        drone.setEventHandler(DataType.Information, self.eventInformation)
        drone.setEventHandler(DataType.UpdateLocation, self.eventUpdateLocation)


        # 변수
        flagRun             = True
        countError          = 0
        timeTransferNext    = 0
        timeDrawNext        = 0     # 업데이트 상태 다음 갱신 시각


        # 연결된 장치 확인
        drone.sendRequest(DeviceType.Drone, DataType.Information)
        sleep(0.2)

        drone.sendRequest(DeviceType.Controller, DataType.Information)
        sleep(0.2)


        if self.deviceType == None:
            print(Fore.RED + "* Error : No Answer." + Style.RESET_ALL)
            sys.exit(1)


        # 헤더 만들기
        header = Header()
        header.dataType = DataType.Update
        header.length   = 18
        header.from_    = DeviceType.Updater
        header.to_      = self.deviceType


        # 업데이트 위치 요청
        drone.sendRequest(header.to_, DataType.UpdateLocation)
        sleep(0.1)

        drone.sendRequest(header.to_, DataType.UpdateLocation)
        sleep(0.1)


        # 펌웨어 업데이트
        for fw in firmware:

            if self.modelNumber == fw.header.modelNumber:

                # 펌웨어의 모델 번호와 일치하는 드론이 있는 경우

                if self.modeUpdate == ModeUpdate.Ready or self.modeUpdate == ModeUpdate.Update:

                    while flagRun:

                        sleep(0.001)
                        now = time.perf_counter() * 1000

                        if (self.flagUpdated == True) or (timeTransferNext < now):

                            if self.indexBlockNext == 0:
                                timeTransferNext = now + 2400
                            else:
                                timeTransferNext = now + 100

                            # 에러 카운트
                            if self.flagUpdated == False:

                                countError = countError + 1

                                # 오류가 과도하게 누적된 경우 업데이트 취소
                                if countError > 30:
                                    print(Fore.RED + "* Error : No response." + Style.RESET_ALL)
                                    flagRun = False
                            
                            else:
                                countError = 0


                            index = self.indexBlockNext * 16

                            # 업데이트 할 위치를 넘어서는 경우 종료
                            if index + 16 > fw.length:
                                print(Fore.RED + "* Error : Index Over." + Style.RESET_ALL)
                                flagRun = False
                                break

                            # 업데이트가 완료된 경우 종료
                            if self.flagUpdateComplete == True:
                                sleep(1)
                                print("\n\n" + Fore.GREEN + "  Update Complete." + Style.RESET_ALL)
                                flagRun = False
                                break

                            data = bytearray(2)
                            data[0] = self.indexBlockNext & 0xFF
                            data[1] = (self.indexBlockNext >> 8) & 0xFF
                            data.extend(fw.resource[index : index + 16])
                            drone.transfer(header, data)
                            
                            self.flagUpdated = False

                            # 진행률 표시
                            if (timeDrawNext < now) or (fw.length - index < 128):

                                timeDrawNext    = now + 73
                                percentage      = index * 100 / fw.length
                                print(Fore.YELLOW + "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b{0:8.1f}%".format(percentage) + Style.RESET_ALL, end='')
                else:
                    print(Fore.RED + "* Error : Firmware update is not available." + Style.RESET_ALL)

                break

        drone.close()


# Updater End




# Main Start


if __name__ == '__main__':

    updater = Updater()

    updater.update()


# Main End

