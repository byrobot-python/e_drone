import time

from petrone_v2.protocol import *
from petrone_v2.crc import CRC16



# 데이터 수신 상태
class StateLoading(Enum):
    
    Ready           = 0x00      # 수신 대기
    Receiving       = 0x01      # 수신중
    Loaded          = 0x02      # 수신 완료 후 명령어 보관소에 대기중
    Failure         = 0x03      # 수신 실패



# 데이터 섹션 구분
class Section(Enum):

    Start           = 0x00      # 전송 시작 코드
    Header          = 0x01      # 헤더
    Data            = 0x02      # 데이터
    End             = 0x03      # 데이터 확인



class Receiver:


    def __init__(self):
        
        self.state                  = StateLoading.Ready
        self.sectionOld             = Section.End
        self.section                = Section.Start
        self.index                  = 0

        self.header                 = Header()
        self.timeReceiveStart       = 0
        self.timeReceiveComplete    = 0

        self._dataBuffer            = []
        self.data                   = bytearray()

        self.crc16received          = 0
        self.crc16calculated        = 0


    def call(self, data):
        
        now = time.clock() * 1000


        # First Step
        if self.state == StateLoading.Ready:
            self.section = Section.Start
            self.index = 0

        elif self.state == StateLoading.Receiving:
            if self.timeReceiveStart + 100 < now:
                self.state = StateLoading.Ready
                self.section = Section.Start
                self.index = 0

        elif self.state == StateLoading.Loaded:
            return


        # Second Step
        if self.section != self.sectionOld:
            self.index = 0
            self.sectionOld = self.section
        

        # Third Step
        if self.section == Section.Start:
            if self.index == 0:
                if data == 0x0A:
                    self.state = StateLoading.Receiving
                else:
                    self.state = StateLoading.Failure
                self.timeReceiveStart = now

            elif self.index == 1:
                if data != 0x55:
                    self.state = StateLoading.Failure
                else:
                    self.section = Section.Header
            else:
                self.state = StateLoading.Failure
        
        elif self.section == Section.Header:
            if self.index == 0:
                self.header = Header()
                self.header.dataType = DataType(data)
                self.crc16calculated = CRC16.calc(data, 0)
            elif self.index == 1:
                self.header.length = data
                self.crc16calculated = CRC16.calc(data, self.crc16calculated)
            elif self.index == 2:
                self.header.from_ = DeviceType(data)
                self.crc16calculated = CRC16.calc(data, self.crc16calculated)
            elif self.index == 3:
                self.header.to_ = DeviceType(data)
                self.crc16calculated = CRC16.calc(data, self.crc16calculated)

                if self.header.length > 128:
                    self.state = StateLoading.Failure
                elif self.header.length == 0:
                    self.section = Section.End
                else:
                    self.section = Section.Data
                    self._dataBuffer.clear()
            else:
                self.state = StateLoading.Failure
        
        elif self.section == Section.Data:
            self._dataBuffer.append(data)
            self.crc16calculated = CRC16.calc(data, self.crc16calculated)

            if (self.index == self.header.length - 1):
                self.section = Section.End
        
        elif self.section == Section.End:
            if self.index == 0:
                self.crc16received = data
            elif self.index == 1:
                self.crc16received = (data << 8) | self.crc16received

                if self.crc16received == self.crc16calculated:
                    self.data = bytearray(self._dataBuffer)
                    self.timeReceiveComplete = now
                    self.state = StateLoading.Loaded
                else:
                    self.state = StateLoading.Failure
            else:
                self.state = StateLoading.Failure

        else:
            self.state = StateLoading.Failure


        #Forth Step
        if self.state == StateLoading.Receiving:
            self.index += 1
        elif self.state == StateLoading.Failure:
            self.state = StateLoading.Ready


    def checked(self):
        self.state = StateLoading.Ready


