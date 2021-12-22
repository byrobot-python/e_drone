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
        self.model_number       = 0
        self.version            = 0
        self.length             = 0

        self.year               = 0
        self.month              = 0
        self.day                = 0

        self.version_major      = 0
        self.version_minor      = 0
        self.version_build      = 0


    @classmethod
    def get_size(cls):
        return 16


    @classmethod
    def parse(cls, data_array):
        data = FirmwareHeader()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.model_number, data.version, data.length, data.year, data.month, data.day = unpack('<IIIHBB', data_array)

        data.model_number = ModelNumber(data.model_number)

        data.version_major = (data.version >> 24) & 0xFF
        data.version_minor = (data.version >> 16) & 0xFF
        data.version_build = (data.version & 0xFFFF)

        return data



class Firmware():

    def __init__(self, url = None):

        if url == None:
            self.url            = 0         # 펌웨어 URL
            self.resource       = None      # 펌웨어 전체 파일
            self.header         = None      # 펌웨어 헤더
            self.length         = 0         # 펌웨어 전체 파일의 길이

            self.raw_header     = None      # 헤더 배열
            self.string_header  = None      # 헤더 배열을 HEX 문자열로 변환한 것
        else:
            self.open(url)


    def open(self, url):

        self.url = url
        
        with urlopen(self.url) as res:
            self.resource   = res.read()
            self.length     = len(self.resource)
            self.raw_header = self.resource[0:16]
            self.header     = FirmwareHeader.parse(self.raw_header)

            self.string_header = ""
            for data in self.raw_header:
                self.string_header += "{0:02X} ".format(data)

            print(Fore.CYAN + "  - {0}".format(self.header.model_number) + Style.RESET_ALL)
            print("    Header Hex : {0}".format(self.string_header))
            print("     File Size : {0} bytes".format(self.length))
            print("       Version : {0}.{1}.{2}".format(self.header.version_major, self.header.version_minor, self.header.version_build))
            print("          Date : {0}.{1}.{2}".format(self.header.year, self.header.month, self.header.day))
            print("        Length : {0}\n".format(self.header.length))


# Firmware End




# Updater Start

class Updater:


    def __init__(self):

        self.model_number         = None
        self.device_type          = None
        self.mode_update          = ModeUpdate.NONE
        self.index_block_next     = 0
        self.flag_updated         = False
        self.flag_update_complete = False



    def event_information(self, information):

        self.mode_update         = information.mode_update
        self.flag_updated        = True
        self.model_number        = information.model_number
        self.device_type         = DeviceType(((self.model_number.value >> 8) & 0xFF))
        
        if information.mode_update == ModeUpdate.COMPLETE:
            self.flag_update_complete = True
        else:
            print(Fore.YELLOW + "* Connected Device : {0}".format(self.device_type) + Style.RESET_ALL)
            print("  Model Number : {0}".format(information.model_number))
            print("       Version : {0}.{1}.{2} ({3} / 0x{3:08X})".format(information.version.major, information.version.minor, information.version.build, information.version.v))
            print("  Release Date : {0}.{1}.{2}".format(information.year, information.month, information.day))
            print("   Mode Update : {0}\n".format(information.mode_update))



    def event_update_location(self, update_location):

        self.flag_updated         = True
        self.index_block_next     = update_location.index_block_next
        #print("* eventUpdateLocation({0})\n".format(update_location.index_block_next))



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
        drone.set_event_handler(DataType.INFORMATION, self.eventInformation)
        drone.set_event_handler(DataType.UPDATE_LOCATION, self.eventUpdateLocation)


        # 변수
        flag_run             = True
        count_error          = 0
        time_transfer_next   = 0
        time_draw_next       = 0     # 업데이트 상태 다음 갱신 시각


        # 연결된 장치 확인
        drone.send_request(DeviceType.DRONE, DataType.INFORMATION)
        sleep(0.2)

        drone.send_request(DeviceType.CONTROLLER, DataType.INFORMATION)
        sleep(0.2)


        if self.device_type == None:
            print(Fore.RED + "* Error : No Answer." + Style.RESET_ALL)
            sys.exit(1)


        # 헤더 만들기
        header = Header()
        header.data_type = DataType.UPDATE
        header.length    = 18
        header.from_     = DeviceType.UPDATER
        header.to_       = self.device_type


        # 업데이트 위치 요청
        drone.send_request(header.to_, DataType.UPDATE_LOCATION)
        sleep(0.1)

        drone.send_request(header.to_, DataType.UPDATE_LOCATION)
        sleep(0.1)


        # 펌웨어 업데이트
        for fw in firmware:

            if self.model_number == fw.header.model_number:

                # 펌웨어의 모델 번호와 일치하는 드론이 있는 경우

                if self.mode_update == ModeUpdate.READY or self.mode_update == ModeUpdate.UPDATE:

                    while flag_run:

                        sleep(0.001)
                        now = time.perf_counter() * 1000

                        if (self.flag_updated == True) or (time_transfer_next < now):

                            if self.index_block_next == 0:
                                time_transfer_next = now + 2400
                            else:
                                time_transfer_next = now + 100

                            # 에러 카운트
                            if self.flag_updated == False:

                                count_error = count_error + 1

                                # 오류가 과도하게 누적된 경우 업데이트 취소
                                if count_error > 30:
                                    print(Fore.RED + "* Error : No response." + Style.RESET_ALL)
                                    flag_run = False
                            
                            else:
                                count_error = 0


                            index = self.index_block_next * 16

                            # 업데이트 할 위치를 넘어서는 경우 종료
                            if index + 16 > fw.length:
                                print(Fore.RED + "* Error : Index Over." + Style.RESET_ALL)
                                flag_run = False
                                break

                            # 업데이트가 완료된 경우 종료
                            if self.flag_update_complete == True:
                                sleep(1)
                                print("\n\n" + Fore.GREEN + "  Update Complete." + Style.RESET_ALL)
                                flag_run = False
                                break

                            data = bytearray(2)
                            data[0] = self.index_block_next & 0xFF
                            data[1] = (self.index_block_next >> 8) & 0xFF
                            data.extend(fw.resource[index : index + 16])
                            drone.transfer(header, data)
                            
                            self.flag_updated = False

                            # 진행률 표시
                            if (time_draw_next < now) or (fw.length - index < 128):

                                time_draw_next    = now + 73
                                percentage      = index * 100 / fw.length
                                print(Fore.YELLOW + "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b{0:8.1f}%".format(percentage) + Style.RESET_ALL, end = '')
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

