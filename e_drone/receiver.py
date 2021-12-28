import time

from e_drone.protocol import *
from e_drone.crc import Crc16



# 데이터 수신 상태
class StateLoading(Enum):
    
    READY           = 0x00      # 수신 대기
    RECEIVING       = 0x01      # 수신중
    LOADED          = 0x02      # 수신 완료 후 명령어 보관소에 대기중
    FAILURE         = 0x03      # 수신 실패



# 데이터 섹션 구분
class Section(Enum):

    START           = 0x00      # 전송 시작 코드
    HEADER          = 0x01      # 헤더
    DATA            = 0x02      # 데이터
    END             = 0x03      # 데이터 확인



class Receiver:


    def __init__(self):
        
        self.state                    = StateLoading.READY
        self.section_old              = Section.END
        self.section                  = Section.START
        self.index                    = 0

        self.header                   = Header()
        self.time_receive_start       = 0
        self.time_receive_complete    = 0

        self._buffer                  = bytearray()
        self.data                     = bytearray()

        self.crc16_received           = 0
        self.crc16_calculated         = 0

        self.message                  = None



    def call(self, data):
        
        now = time.perf_counter() * 1000

        self.message = None


        # First Step
        if self.state == StateLoading.FAILURE:
            self.state = StateLoading.READY


        # Second Step
        if self.state == StateLoading.READY:
            self.section = Section.START
            self.index = 0

        elif self.state == StateLoading.RECEIVING:
            # 데이터 수신을 시작한지 600ms 시간이 지난 경우 오류 출력
            if (self.time_receive_start + 600) < now:
                self.state = StateLoading.FAILURE
                self.message = "Error / Receiver / StateLoading.RECEIVING / Time over."
                return self.state

        elif self.state == StateLoading.LOADED:
            return self.state


        # Third Step
        if self.section != self.section_old:
            self.index = 0
            self.section_old = self.section
        

        # Third Step
        if self.section == Section.START:
            if self.index == 0:
                if data == 0x0A:
                    self.state = StateLoading.RECEIVING

                else:
                    self.state = StateLoading.FAILURE
                    return self.state
                self.time_receive_start = now

            elif self.index == 1:
                if data != 0x55:
                    self.state = StateLoading.FAILURE
                    return self.state
                else:
                    self.section = Section.HEADER
            else:
                self.state = StateLoading.FAILURE
                self.message = "Error / Receiver / Section.START / Index over."
                return self.state
        
        elif self.section == Section.HEADER:
            
            if self.index == 0:
                self.header = Header()
                
                try:
                    self.header.data_type = DataType(data)

                except:
                    self.state = StateLoading.FAILURE
                    self.message = "Error / Receiver / Section.HEADER / DataType Error. 0x{0:02X}".format(data)
                    return self.state

                self.crc16_calculated = Crc16.calc(data, 0)

            elif self.index == 1:
                self.header.length = data
                self.crc16_calculated = Crc16.calc(data, self.crc16_calculated)

                if self.header.length > 128:
                    self.state = StateLoading.FAILURE
                    self.message = "Error / Receiver / Section.HEADER / Data length is longer than 128. [{0}]".format(self.header.length)
                    return self.state

            elif self.index == 2:
                try:
                    self.header.from_ = DeviceType(data)

                except:
                    self.state = StateLoading.FAILURE
                    self.message = "Error / Receiver / Section.HEADER / DeviceType Error. 0x{0:02X}".format(data)
                    return self.state

                self.crc16_calculated = Crc16.calc(data, self.crc16_calculated)

            elif self.index == 3:
                try:
                    self.header.to_ = DeviceType(data)

                except:
                    self.state = StateLoading.FAILURE
                    self.message = "Error / Receiver / Section.HEADER / DeviceType Error. 0x{0:02X}".format(data)
                    return self.state

                self.crc16_calculated = Crc16.calc(data, self.crc16_calculated)

                if self.header.length == 0:
                    self.section = Section.END

                else:
                    self.section = Section.DATA
                    self._buffer.clear()

            else:
                self.state = StateLoading.FAILURE
                self.message = "Error / Receiver / Section.HEADER / Index over."
                return self.state
        
        elif self.section == Section.DATA:
            self._buffer.append(data)
            self.crc16_calculated = Crc16.calc(data, self.crc16_calculated)

            if (self.index == self.header.length - 1):
                self.section = Section.END
        
        elif self.section == Section.END:
            if   self.index == 0:
                self.crc16_received = data

            elif self.index == 1:
                self.crc16_received = (data << 8) | self.crc16_received

                if self.crc16_received == self.crc16_calculated:
                    self.data = self._buffer.copy()
                    self.time_receive_complete = now
                    self.state = StateLoading.LOADED
                    self.message = "Success / Receiver / Section.END / Receive complete / {0} / [receive: 0x{1:04X}]".format(self.header.data_type, self.crc16_received)
                    return self.state

                else:
                    self.state = StateLoading.FAILURE
                    self.message = "Error / Receiver / Section.END / CRC Error / {0} / [receive: 0x{1:04X}, calculate: 0x{2:04X}]".format(self.header.data_type, self.crc16_received, self.crc16_calculated)
                    return self.state

            else:
                self.state = StateLoading.FAILURE
                self.message = "Error / Receiver / Section.END / Index over."
                return self.state

        else:
            self.state = StateLoading.FAILURE
            self.message = "Error / Receiver / Section over."
            return self.state


        #Forth Step
        if self.state == StateLoading.RECEIVING:
            self.index += 1

        return self.state



    def checked(self):
        self.state = StateLoading.READY

