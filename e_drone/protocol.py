import os
import abc 
from struct import *
from enum import Enum

from e_drone.system import *


# ISerializable Start


class ISerializable:
    
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_size(self):
        pass

    @abc.abstractmethod
    def to_array(self):
        pass


# ISerializable End



# DataType Start


class DataType(Enum):
    
    NONE                        = 0x00      # 없음
    
    PING                        = 0x01      # 통신 확인
    ACK                         = 0x02      # 데이터 수신에 대한 응답
    ERROR                       = 0x03      # 오류(reserve, 비트 플래그는 추후에 지정)
    REQUEST                     = 0x04      # 지정한 타입의 데이터 요청
    MESSAGE                     = 0x05      # 문자열 데이터
    ADDRESS                     = 0x06      # 장치 주소(MAC이 있는 경우 MAC) 혹은 고유번호(MAC이 없는 경우 UUID)
    INFORMATION                 = 0x07      # 펌웨어 및 장치 정보
    UPDATE                      = 0x08      # 펌웨어 업데이트
    UPDATE_LOCATION             = 0x09      # 펌웨어 업데이트 위치 정정
    ENCRYPT                     = 0x0A      # 펌웨어 암호화
    SYSTEM_COUNT                = 0x0B      # 시스템 카운트
    SYSTEM_INFORMATION          = 0x0C      # 시스템 정보
    REGISTRATION                = 0x0D      # 제품 등록
    ADMINISTRATOR               = 0x0E      # 관리자 권한 획득
    MONITOR                     = 0x0F      # 디버깅용 값 배열 전송. 첫번째 바이트에 타입, 두 번째 바이트에 페이지 지정(수신 받는 데이터의 저장 경로 구분)
    CONTROL                     = 0x10      # 조종

    COMMAND                     = 0x11      # 명령
    PAIRING                     = 0x12      # 페어링
    RSSI                        = 0x13      # RSSI
    TIME_SYNC                   = 0x14      # 시간 동기화
    TRANSMISSION_POWER          = 0x15      # 전송 출력
    CONFIGURATION               = 0x16      # 설정
    ECHO                        = 0x17      # 반향(정상적으로 송수신 되는 데이터 길이 확인용, 받은 데이터를 그대로 반환, RF로 송수신 가능한 데이터 길이를 확인할 목적으로 추가)

    BATTLE                      = 0x1F      # 전투

    # Light
    LIGHT_MANUAL                = 0x20      # LED 수동 제어
    LIGHT_MODE                  = 0x21      # LED 모드
    LIGHT_EVENT                 = 0x22      # LED 이벤트
    LIGHT_DEFAULT               = 0x23      # LED 초기 모드

    # 센서 RAW 데이터
    RAW_MOTION                  = 0x30      # Motion 센서 데이터 RAW 값
    RAW_FLOW                    = 0x31      # Flow 센서 데이터 RAW 값

    # 상태, 센서
    STATE                       = 0x40      # 드론의 상태(비행 모드 방위기준 배터리량)
    ATTITUDE                    = 0x41      # 드론의 자세(Angle)
    POSITION                    = 0x42      # 위치
    ALTITUDE                    = 0x43      # 높이, 고도
    MOTION                      = 0x44      # Motion 센서 데이터 처리한 값(IMU)
    RANGE                       = 0x45      # 거리센서 데이터

    # 설정
    COUNT                       = 0x50      # 카운트
    BIAS                        = 0x51      # 엑셀, 자이로 바이어스 값
    TRIM                        = 0x52      # 트림
    WEIGHT                      = 0x53      # 무게
    LOST_CONNECTION             = 0x54      # 연결이 끊긴 후 반응 시간 설정

    # Devices
    MOTOR                       = 0x60      # 모터 제어 및 현재 제어값 확인
    MOTOR_SINGLE                = 0x61      # 한 개의 모터 제어
    BUZZER                      = 0x62      # 부저 제어
    VIBRATOR                    = 0x63      # 진동 제어

    # Input
    BUTTON                      = 0x70      # 버튼 입력
    JOYSTICK                    = 0x71      # 조이스틱 입력

    # Display
    DISPLAY_CLEAR               = 0x80      # 화면 지우기
    DISPLAY_INVERT              = 0x81      # 화면 반전
    DISPLAY_DRAW_POINT          = 0x82      # 점 그리기
    DISPLAY_DRAW_LINE           = 0x83      # 선 그리기
    DISPLAY_DRAW_RECT           = 0x84      # 사각형 그리기
    DISPLAY_DRAW_CIRCLE         = 0x85      # 원 그리기
    DISPLAY_DRAW_STRING         = 0x86      # 문자열 쓰기
    DISPLAY_DRAW_STRING_ALIGN   = 0x87      # 문자열 쓰기
    DISPLAY_DRAW_Image          = 0x88      # 그림 그리기

    # Card
    CARD_CLASSIFY               = 0x90      # 카드 색상 분류 기준 설정
    CARD_RANGE                  = 0x91      # 카드 색 범위(RAW 데이터의 출력 범위)
    CARD_RAW                    = 0x92      # 카드 데이터 RAW 값(유선으로만 전송)
    CARD_COLOR                  = 0x93      # 카드 데이터
    CARD_LIST                   = 0x94      # 카드 리스트 데이터
    CARD_FUNCTION_LIST          = 0x95      # 카드 함수 리스트 데이터
    
    # Information Assembled
    INFORMATION_ASSEMBLED_FOR_CONTROLLER   = 0xA0      # 자주 갱신되는 데이터 모음
    INFORMATION_ASSEMBLED_FOR_ENTRY        = 0xA1      # 자주 갱신되는 데이터 모음
    INFORMATION_ASSEMBLED_FOR_BYBLOCKS     = 0xA2      # 자주 갱신되는 데이터 모음

    # Navigation
    NAVIGATION_TARGET            = 0xD0      # 네비게이션 목표점
    NAVIGATION_LOCATION          = 0xD1      # 네비게이션 드론 위치
    NAVIGATION_MONITOR           = 0xD2
    NAVIGATION_HEADING           = 0xD3
    NAVIGATION_COUNTER           = 0xD4
    NAVIGATION_SATELLITE         = 0xD5      # 위성 정보
    NAVIGATION_LOCATION_ADJUST   = 0xD6      # 드론 위치 조정

    NAVIGATION_TARGET_ECEF       = 0xD8      # 드론 타겟 위치(ECEF)
    NAVIGATION_LOCATION_ECEF     = 0xD9      # 드론 현재 위치(ECEF)

    GPS_RTK_NAVIGATION_STATE                 = 0xDA      # RTK RAW 데이터 전송
    GPS_RTK_EXTENDED_RAW_MEASUREMENT_DATA    = 0xDB      # RTK RAW 데이터 전송

    END_OF_TYPE                  = 0xDC


# DataType End



# CommandType Start


class CommandType(Enum):
    
    NONE                   = 0x00      # 없음

    STOP                    = 0x01      # 정지

    # 설정
    MODE_CONTROL_FLIGHT     = 0x02      # 비행 제어 모드 설정
    HEADLESS                = 0x03      # 헤드리스 모드 선택
    CONTROL_SPEED           = 0x04      # 제어 속도 설정

    CLEAR_BIAS              = 0x05      # 자이로 바이어스 리셋(트림도 같이 초기화 됨)
    CLEAR_TRIM              = 0x06      # 트림 초기화

    FLIGHT_EVENT            = 0x07      # 비행 이벤트 실행

    SET_DEFAULT             = 0x08      # 기본 설정으로 초기화
    BACKLIGHT               = 0x09      # 조종기 백라이트 설정
    MODE_CONTROLLER         = 0x0A      # 조종기 동작 모드(0x10:조종, 0x80:링크)
    LINK                    = 0x0B      # 링크 제어(0:Client Mode, 1:Server Mode, 2:Pairing Start)

    # 관리자
    CLEAR_COUNTER           = 0xA0      # 카운터 클리어(관리자 권한을 획득했을 경우에만 동작)

    # Navigation
    NAVIGATION_TARGET_CLEAR = 0xE0      # 네비게이션 목표점 초기화
    NAVIGATION_START        = 0xE1      # 네비게이션 시작(처음부터)
    NAVIGATION_PAUSE        = 0xE2      # 네비게이션 일시 정지
    NAVIGATION_RESTART      = 0xE3      # 네비게이션 다시 시작(일시 정지 후 다시 시작할 때 사용)
    NAVIGATION_STOP         = 0xE4      # 네비게이션 중단
    NAVIGATION_NEXT         = 0xE5      # 네비게이션 목표점을 다음으로 변경
    NAVIGATION_RETURN_HOME  = 0xE6      # 시작 위치로 귀환

    GPS_RTK_BASE            = 0xEA
    GPS_RTK_ROVER           = 0xEB

    END_OF_TYPE             = 0xEC


# CommandType End



# Header Start


class Header(ISerializable):

    def __init__(self):
        self.data_type   = DataType.NONE
        self.length      = 0
        self.from_       = DeviceType.NONE
        self.to_         = DeviceType.NONE


    @classmethod
    def get_size(cls):
        return 4


    def to_array(self):
        return pack('<BBBB', self.data_type.value, self.length, self.from_.value, self.to_.value)


    @classmethod
    def parse(cls, data_array):
        header = Header()

        if len(data_array) != cls.get_size():
            return None

        header.data_type, header.length, header.from_, header.to_ = unpack('<BBBB', data_array)

        header.data_type = DataType(header.data_type)
        header.from_ = DeviceType(header.from_)
        header.to_ = DeviceType(header.to_)

        return header


# Header End



# Common Start


class Ping(ISerializable):

    def __init__(self):
        self.system_time     = 0


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<Q', self.system_time)


    @classmethod
    def parse(cls, data_array):
        data = Ping()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.system_time, = unpack('<Q', data_array)
        return data



class Ack(ISerializable):

    def __init__(self):
        self.system_time    = 0
        self.data_type      = DataType.NONE
        self.crc16          = 0


    @classmethod
    def get_size(cls):
        return 11


    def to_array(self):
        return pack('<QBH', self.system_time, self.data_type.value, self.crc16)


    @classmethod
    def parse(cls, data_array):
        data = Ack()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.system_time, data.data_type, data.crc16 = unpack('<QBH', data_array)
        data.data_type = DataType(data.data_type)

        return data



class Error(ISerializable):

    def __init__(self):
        self.system_time               = 0
        self.error_flags_for_sensor    = 0
        self.error_flags_for_state     = 0


    @classmethod
    def get_size(cls):
        return 16


    def to_array(self):
        return pack('<QII', self.system_time, self.error_flags_for_sensor, self.error_flags_for_state)


    @classmethod
    def parse(cls, data_array):
        data = Error()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.system_time, data.error_flags_for_sensor, data.error_flags_for_state = unpack('<QII', data_array)

        return data



class Request(ISerializable):

    def __init__(self):
        self.data_type    = DataType.NONE


    @classmethod
    def get_size(cls):
        return 1


    def to_array(self):
        return pack('<B', self.data_type.value)


    @classmethod
    def parse(cls, data_array):
        data = Request()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.data_type, = unpack('<B', data_array)
        data.data_type = DataType(data.data_type)

        return data



class RequestOption(ISerializable):

    def __init__(self):
        self.data_type   = DataType.NONE
        self.option      = 0


    @classmethod
    def get_size(cls):
        return 5


    def to_array(self):
        return pack('<BI', self.data_type.value, self.option)


    @classmethod
    def parse(cls, data_array):
        data = Request()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.data_type, data.option = unpack('<BI', data_array)
        data.data_type = DataType(data.data_type)

        return data



class Message():

    def __init__(self):
        self.message    = ""


    def get_size(self):
        return len(self.message)


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.message.encode('ascii', 'ignore'))
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = Message()
        
        if len(data_array) == 0:
            return ""

        data.message = data_array[0:len(data_array)].decode()
        
        return data



class SystemInformation(ISerializable):

    def __init__(self):
        self.crc32_bootloader    = 0
        self.crc32_application   = 0


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<II', self.crc32_bootloader, self.crc32_application)


    @classmethod
    def parse(cls, data_array):
        data = SystemInformation()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.crc32_bootloader, data.crc32_application = unpack('<II', data_array)

        return data



class Version(ISerializable):

    def __init__(self):
        self.build          = 0
        self.minor          = 0
        self.major          = 0

        self.v              = 0         # build, minor, major을 하나의 UInt32로 묶은 것(버젼 비교 시 사용)


    @classmethod
    def get_size(cls):
        return 4


    def to_array(self):
        return pack('<HBB', self.build, self.minor, self.major)


    @classmethod
    def parse(cls, data_array):
        data = Version()
        
        if len(data_array) != cls.get_size():
            return None

        data.v, = unpack('<I', data_array)

        data.build, data.minor, data.major = unpack('<HBB', data_array)

        return data



class Information(ISerializable):

    def __init__(self):
        self.mode_update    = ModeUpdate.NONE

        self.model_number   = ModelNumber.NONE
        self.version        = Version()

        self.year           = 0
        self.month          = 0
        self.day            = 0


    @classmethod
    def get_size(cls):
        return 13


    def to_array(self):
        data_array = bytearray()
        data_array.extend(pack('<B', self.mode_update.value))
        data_array.extend(pack('<I', self.model_number.value))
        data_array.extend(self.version.to_array())
        data_array.extend(pack('<H', self.year))
        data_array.extend(pack('<B', self.month))
        data_array.extend(pack('<B', self.day))
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = Information()
        
        if len(data_array) != cls.get_size():
            return None
        
        index_start = 0;         index_end  = 1;                   data.mode_update,   = unpack('<B', data_array[index_start:index_end])
        index_start = index_end; index_end += 4;                   data.model_number,  = unpack('<I', data_array[index_start:index_end])
        index_start = index_end; index_end += Version.get_size();  data.version        = Version.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += 2;                   data.year,          = unpack('<H', data_array[index_start:index_end])
        index_start = index_end; index_end += 1;                   data.month,         = unpack('<B', data_array[index_start:index_end])
        index_start = index_end; index_end += 1;                   data.day,           = unpack('<B', data_array[index_start:index_end])

        data.mode_update     = ModeUpdate(data.mode_update)
        data.model_number    = ModelNumber(data.model_number)

        return data



class UpdateLocation(ISerializable):

    def __init__(self):
        self.index_block_next    = 0


    @classmethod
    def get_size(cls):
        return 2


    def to_array(self):
        return pack('<H', self.index_block_next)


    @classmethod
    def parse(cls, data_array):
        data = UpdateLocation()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.index_block_next, = unpack('<H', data_array)

        return data



class Address(ISerializable):

    def __init__(self):
        self.address    = bytearray()


    @classmethod
    def get_size(cls):
        return 16


    def to_array(self):
        return self.address


    @classmethod
    def parse(cls, data_array):
        data = Address()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.address = data_array[0:16]
        return data



class RegistrationInformation(ISerializable):

    def __init__(self):
        self.address        = bytearray()
        self.year           = 0
        self.month          = 0
        self.key            = 0
        self.flag_valid     = 0


    @classmethod
    def get_size(cls):
        return 21


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.address)
        data_array.extend(pack('<HBB?', self.year, self.month, self.key, self.flag_valid))
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = RegistrationInformation()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.address = data_array[0:16]
        data.year, data.month, data.key, data.flag_valid = unpack('<HBB?', data_array[16:21])
        return data



class Pairing(ISerializable):

    def __init__(self):
        self.address_0      = 0
        self.address_1      = 0
        self.address_2      = 0

        self.scramble       = 0

        self.channel_0      = 0
        self.channel_1      = 0
        self.channel_2      = 0
        self.channel_3      = 0


    @classmethod
    def get_size(cls):
        return 11


    def to_array(self):
        return pack('<HHHBBBBB', self.address_0, self.address_1, self.address_2, self.scramble, self.channel_0, self.channel_1, self.channel_2, self.channel_3)


    @classmethod
    def parse(cls, data_array):
        data = Pairing()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.address_0, data.address_1, data.address_2, data.scramble, data.channel_0, data.channel_1, data.channel_2, data.channel_3 = unpack('<HHHBBBBB', data_array)
        return data



class Rssi(ISerializable):

    def __init__(self):
        self.rssi       = 0


    @classmethod
    def get_size(cls):
        return 1


    def to_array(self):
        return pack('<b', self.rssi)


    @classmethod
    def parse(cls, data_array):
        data = Rssi()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.rssi, = unpack('<b', data_array)

        return data



class Command(ISerializable):

    def __init__(self):
        self.command_type   = CommandType.NONE
        self.option         = 0


    @classmethod
    def get_size(cls):
        return 2


    def to_array(self):
        return pack('<BB', self.command_type.value, self.option)


    @classmethod
    def parse(cls, data_array):
        data = Command()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.command_type, data.option = unpack('<BB', data_array)
        data.command_type = CommandType(data.command_type)

        return data



class CommandLightEvent(ISerializable):

    def __init__(self):
        self.command    = Command()
        self.event      = LightEvent()


    @classmethod
    def get_size(cls):
        return Command.get_size() + LightEvent.get_size()


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.command.to_array())
        data_array.extend(self.event.to_array())
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = CommandLightEvent()
        
        if len(data_array) != cls.get_size():
            return None
        
        index_start = 0;         index_end = Command.get_size();         data.command    = Command.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += LightEvent.get_size();     data.event      = LightEvent.parse(data_array[index_start:index_end])
        
        return data
        


class CommandLightEventColor(ISerializable):

    def __init__(self):
        self.command    = Command()
        self.event      = LightEvent()
        self.color      = Color()


    @classmethod
    def get_size(cls):
        return Command.get_size() + LightEvent.get_size() + Color.get_size()


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.command.to_array())
        data_array.extend(self.event.to_array())
        data_array.extend(self.color.to_array())
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = CommandLightEventColor()
        
        if len(data_array) != cls.get_size():
            return None

        index_start = 0;         index_end = Command.get_size();       data.command    = Command.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += LightEvent.get_size();   data.event      = LightEvent.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += Color.get_size();        data.color      = Color.parse(data_array[index_start:index_end])
        
        return data
        


class CommandLightEventColors(ISerializable):

    def __init__(self):
        self.command    = Command()
        self.event      = LightEvent()
        self.colors     = Colors.BLACK


    @classmethod
    def get_size(cls):
        return Command.get_size() + LightEvent.get_size() + 1


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.command.to_array())
        data_array.extend(self.event.to_array())
        data_array.extend(pack('<B', self.colors.value))
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = Command()
        
        if len(data_array) != cls.get_size():
            return None
        
        index_start = 0;         index_end = Command.get_size();       data.command    = Command.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += LightEvent.get_size();   data.event      = LightEvent.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += 1;                       data.colors,    = unpack('<B', data_array[index_start:index_end])

        data.colors     = Colors(data.colors)

        return data


# Common End



# Monitor Start


class MonitorHeaderType(Enum):
    
    MONITOR_0            = 0x00
    MONITOR_4            = 0x01
    MONITOR_8            = 0x02

    END_OF_TYPE          = 0x03



class monitor_dataType(Enum):
    
    U8          = 0x00, 
    S8          = 0x01, 
    U16         = 0x02, 
    S16         = 0x03, 
    U32         = 0x04, 
    S32         = 0x05, 
    U64         = 0x06, 
    S64         = 0x07, 
    F32         = 0x08, 
    F64         = 0x09, 

    END_OF_TYPE   = 0x0A



class MonitorType(ISerializable):

    def __init__(self):
        self.monitor_header_type    = MonitorHeaderType.MONITOR_8


    @classmethod
    def get_size(cls):
        return 1


    def to_array(self):
        return pack('<B', self.monitor_header_type.value)


    @classmethod
    def parse(cls, data_array):
        data = MonitorType()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.monitor_header_type, = unpack('<B', data_array)

        data.monitor_header_type  = MonitorHeaderType(data.monitor_header_type)

        return data



class Monitor0(ISerializable):

    def __init__(self):
        self.monitor_dataType   = monitor_dataType.F32
        self.index              = 0


    @classmethod
    def get_size(cls):
        return 2


    def to_array(self):
        return pack('<BB', self.monitor_dataType.value, self.index)


    @classmethod
    def parse(cls, data_array):
        data = Monitor0()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.monitor_dataType, data.index = unpack('<BB', data_array)

        data.monitor_dataType  = monitor_dataType(data.monitor_dataType)

        return data



class Monitor4(ISerializable):

    def __init__(self):
        self.system_time        = 0
        self.monitor_dataType   = monitor_dataType.F32
        self.index              = 0


    @classmethod
    def get_size(cls):
        return 6


    def to_array(self):
        return pack('<IBB', self.system_time, self.monitor_dataType.value, self.index)


    @classmethod
    def parse(cls, data_array):
        data = Monitor4()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.system_time, data.monitor_dataType, data.index = unpack('<IBB', data_array)

        data.monitor_dataType  = monitor_dataType(data.monitor_dataType)

        return data



class Monitor8(ISerializable):
    
    def __init__(self):
        self.system_time        = 0
        self.monitor_dataType   = monitor_dataType.F32
        self.index              = 0


    @classmethod
    def get_size(cls):
        return 10


    def to_array(self):
        return pack('<QBB', self.system_time, self.monitor_dataType.value, self.index)


    @classmethod
    def parse(cls, data_array):
        data = Monitor8()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.system_time, data.monitor_dataType, data.index = unpack('<QBB', data_array)

        data.monitor_dataType  = monitor_dataType(data.monitor_dataType)

        return data



# Monitor End



# Control Start


class ControlQuad8(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0
        self.throttle   = 0


    @classmethod
    def get_size(cls):
        return 4


    def to_array(self):
        return pack('<bbbb', self.roll, self.pitch, self.yaw, self.throttle)


    @classmethod
    def parse(cls, data_array):
        data = ControlQuad8()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.roll, data.pitch, data.yaw, data.throttle = unpack('<bbbb', data_array)
        return data



class ControlQuad8AndRequestData(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0
        self.throttle   = 0
        self.data_type  = DataType.NONE


    @classmethod
    def get_size(cls):
        return 5


    def to_array(self):
        return pack('<bbbbb', self.roll, self.pitch, self.yaw, self.throttle, self.data_type)


    @classmethod
    def parse(cls, data_array):
        data = ControlQuad8AndRequestData()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.roll, data.pitch, data.yaw, data.throttle, data.data_type = unpack('<bbbbb', data_array)
        
        data.data_type = DataType(data.data_type)
        
        return data



class ControlPositionShort(ISerializable):

    def __init__(self):
        self.position_x          = 0
        self.position_y          = 0
        self.position_z          = 0

        self.velocity            = 0
        
        self.heading             = 0
        self.rotational_velocity = 0


    @classmethod
    def get_size(cls):
        return 12


    def to_array(self):
        return pack('<hhhhhh', self.position_x, self.position_y, self.position_z, self.velocity, self.heading, self.rotational_velocity)


    @classmethod
    def parse(cls, data_array):
        data = ControlPositionShort()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.position_x, data.position_y, data.position_z, data.velocity, data.heading, data.rotational_velocity = unpack('<hhhhhh', data_array)
        return data



class ControlPosition(ISerializable):

    def __init__(self):
        self.position_x             = 0
        self.position_y             = 0
        self.position_z             = 0

        self.velocity               = 0

        self.heading                = 0
        self.rotational_velocity    = 0


    @classmethod
    def get_size(cls):
        return 20


    def to_array(self):
        return pack('<ffffhh', self.position_x, self.position_y, self.position_z, self.velocity, self.heading, self.rotational_velocity)


    @classmethod
    def parse(cls, data_array):
        data = ControlPosition()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.position_x, data.position_y, data.position_z, data.velocity, data.heading, data.rotational_velocity = unpack('<ffffhh', data_array)
        return data


# Control End



# Light Start


class LightModeDrone(Enum):
    
    NONE                    = 0x00

    REAR_NONE               = 0x10
    REAR_MANUAL             = 0x11      # 수동 제어
    REAR_HOLD               = 0x12      # 지정한 색상을 계속 켬
    REAR_FLICKER            = 0x13      # 깜빡임
    REAR_FLICKER_DOUBLE     = 0x14      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    REAR_DIMMING            = 0x15      # 밝기 제어하여 천천히 깜빡임
    REAR_SUNRISE            = 0x16
    REAR_SUNSET             = 0x17

    BODY_NONE               = 0x20
    BODY_MANUAL             = 0x21      # 수동 제어
    BODY_HOLD               = 0x22      # 지정한 색상을 계속 켬
    BODY_FLICKER            = 0x23      # 깜빡임
    BODY_FLICKER_DOUBLE     = 0x24      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    BODY_DIMMING            = 0x25      # 밝기 제어하여 천천히 깜빡임
    BODY_SUNRISE            = 0x26
    BODY_SUNSET             = 0x27
    BODY_RAINBOW            = 0x28
    BODY_RAINBOW2           = 0x29

    A_NONE                  = 0x30
    A_MANUAL                = 0x31      # 수동 제어
    A_HOLD                  = 0x32      # 지정한 색상을 계속 켬
    A_FLICKER               = 0x33      # 깜빡임
    A_FLICKER_DOUBLE        = 0x34      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    A_DIMMING               = 0x35      # 밝기 제어하여 천천히 깜빡임
    A_SUNRISE               = 0x36
    A_SUNSET                = 0x37

    B_NONE                  = 0x40
    B_MANUAL                = 0x41      # 수동 제어
    B_HOLD                  = 0x42      # 지정한 색상을 계속 켬
    B_FLICKER               = 0x43      # 깜빡임
    B_FLICKER_DOUBLE        = 0x44      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    B_DIMMING               = 0x45      # 밝기 제어하여 천천히 깜빡임
    B_SUNRISE               = 0x46
    B_SUNSET                = 0x47

    END_OF_TYPE             = 0x60



class LightFlagsDrone(Enum):
    
    NONE                = 0x0000

    REAR                = 0x0001

    BODY_RED            = 0x0002
    BODY_GREEN          = 0x0004
    BODY_BLUE           = 0x0008

    A                   = 0x0010
    B                   = 0x0020



class LightModeController(Enum):
    
    NONE                    = 0x00

    BODY_NONE               = 0x20
    BODY_MANUAL             = 0x21      # 수동 제어
    BODY_HOLD               = 0x22      # 지정한 색상을 계속 켬
    BODY_FLICKER            = 0x23      # 깜빡임
    BODY_FLICKER_DOUBLE     = 0x24      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)
    BODY_DIMMING            = 0x25      # 밝기 제어하여 천천히 깜빡임
    BODY_SUNRISE            = 0x26
    BODY_SUNSET             = 0x27
    BODY_RAINBOW            = 0x28
    BODY_RAINBOW2           = 0x29

    END_OF_TYPE             = 0x30



class LightFlagsController(Enum):
    
    NONE                = 0x00

    BODY_RED            = 0x01
    BODY_GREEN          = 0x02
    BODY_BLUE           = 0x04



class Color(ISerializable):

    def __init__(self):
        self.r      = 0
        self.g      = 0
        self.b      = 0


    @classmethod
    def get_size(cls):
        return 3


    def to_array(self):
        return pack('<BBB', self.r, self.g, self.b)


    @classmethod
    def parse(cls, data_array):
        data = Color()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.r, data.g, data.b = unpack('<BBB', data_array)
        return data



class Colors(Enum):

    ALICEBLUE              = 0
    ANTIQUEWHITE           = 1
    AQUA                   = 2
    AQUAMARINE             = 3
    AZURE                  = 4
    BEIGE                  = 5
    BISQUE                 = 6
    BLACK                  = 7
    BLANCHEDALMOND         = 8
    BLUE                   = 9
    BLUEVIOLET             = 10
    BROWN                  = 11
    BURLYWOOD              = 12
    CADETBLUE              = 13
    CHARTREUSE             = 14
    CHOCOLATE              = 15
    CORAL                  = 16
    CORNFLOWERBLUE         = 17
    CORNSILK               = 18
    CRIMSON                = 19
    CYAN                   = 20
    DARKBLUE               = 21
    DARKCYAN               = 22
    DARKGOLDENROD          = 23
    DARKGRAY               = 24
    DARKGREEN              = 25
    DARKKHAKI              = 26
    DARKMAGENTA            = 27
    DARKOLIVEGREEN         = 28
    DARKORANGE             = 29
    DARKORCHID             = 30
    DARKRED                = 31
    DARKSALMON             = 32
    DARKSEAGREEN           = 33
    DARKSLATEBLUE          = 34
    DARKSLATEGRAY          = 35
    DARKTURQUOISE          = 36
    DARKVIOLET             = 37
    DEEPPINK               = 38
    DEEPSKYBLUE            = 39
    DIMGRAY                = 40
    DODGERBLUE             = 41
    FIREBRICK              = 42
    FLORALWHITE            = 43
    FORESTGREEN            = 44
    FUCHSIA                = 45
    GAINSBORO              = 46
    GHOSTWHITE             = 47
    GOLD                   = 48
    GOLDENROD              = 49
    GRAY                   = 50
    GREEN                  = 51
    GREENYELLOW            = 52
    HONEYDEW               = 53
    HOTPINK                = 54
    INDIANRED              = 55
    INDIGO                 = 56
    IVORY                  = 57
    KHAKI                  = 58
    LAVENDER               = 59
    LAVENDERBLUSH          = 60
    LAWNGREEN              = 61
    LEMONCHIFFON           = 62
    LIGHTBLUE              = 63
    LIGHTCORAL             = 64
    LIGHTCYAN              = 65
    LIGHTGOLDENRODYELLOW   = 66
    LIGHTGRAY              = 67
    LIGHTGREEN             = 68
    LIGHTPINK              = 69
    LIGHTSALMON            = 70
    LIGHTSEAGREEN          = 71
    LIGHTSKYBLUE           = 72
    LIGHTSLATEGRAY         = 73
    LIGHTSTEELBLUE         = 74
    LIGHTYELLOW            = 75
    LIME                   = 76
    LIMEGREEN              = 77
    LINEN                  = 78
    MAGENTA                = 79
    MAROON                 = 80
    MEDIUMAQUAMARINE       = 81
    MEDIUMBLUE             = 82
    MEDIUMORCHID           = 83
    MEDIUMPURPLE           = 84
    MEDIUMSEAGREEN         = 85
    MEDIUMSLATEBLUE        = 86
    MEDIUMSPRINGGREEN      = 87
    MEDIUMTURQUOISE        = 88
    MEDIUMVIOLETRED        = 89
    MIDNIGHTBLUE           = 90
    MINTCREAM              = 91
    MISTYROSE              = 92
    MOCCASIN               = 93
    NAVAJOWHITE            = 94
    NAVY                   = 95
    OLDLACE                = 96
    OLIVE                  = 97
    OLIVEDRAB              = 98
    ORANGE                 = 99
    ORANGERED              = 100
    ORCHID                 = 101
    PALEGOLDENROD          = 102
    PALEGREEN              = 103
    PALETURQUOISE          = 104
    PALEVIOLETRED          = 105
    PAPAYAWHIP             = 106
    PEACHPUFF              = 107
    PERU                   = 108
    PINK                   = 109
    PLUM                   = 110
    POWDERBLUE             = 111
    PURPLE                 = 112
    REBECCAPURPLE          = 113
    RED                    = 114
    ROSYBROWN              = 115
    ROYALBLUE              = 116
    SADDLEBROWN            = 117
    SALMON                 = 118
    SANDYBROWN             = 119
    SEAGREEN               = 120
    SEASHELL               = 121
    SIENNA                 = 122
    SILVER                 = 123
    SKYBLUE                = 124
    SLATEBLUE              = 125
    SLATEGRAY              = 126
    SNOW                   = 127
    SPRINGGREEN            = 128
    STEELBLUE              = 129
    TAN                    = 130
    TEAL                   = 131
    THISTLE                = 132
    TOMATO                 = 133
    TURQUOISE              = 134
    VIOLET                 = 135
    WHEAT                  = 136
    WHITE                  = 137
    WHITESMOKE             = 138
    YELLOW                 = 139
    YELLOWGREEN            = 140
    
    END_OF_TYPE            = 141



class LightManual(ISerializable):

    def __init__(self):
        self.flags          = 0
        self.brightness     = 0


    @classmethod
    def get_size(cls):
        return 3


    def to_array(self):
        return pack('<HB', self.flags, self.brightness)


    @classmethod
    def parse(cls, data_array):
        data = LightManual()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.flags, data.brightness = unpack('<HB', data_array)
        return data



class LightMode(ISerializable):

    def __init__(self):
        self.mode        = 0
        self.interval    = 0


    @classmethod
    def get_size(cls):
        return 3


    def to_array(self):
        return pack('<BH', self.mode, self.interval)


    @classmethod
    def parse(cls, data_array):
        data = LightMode()
        
        if len(data_array) != cls.get_size():
            return None

        data.mode, data.interval = unpack('<BH', data_array)
        return data



class LightEvent(ISerializable):

    def __init__(self):
        self.event      = 0
        self.interval   = 0
        self.repeat     = 0


    @classmethod
    def get_size(cls):
        return 4


    def to_array(self):
        return pack('<BHB', self.event, self.interval, self.repeat)


    @classmethod
    def parse(cls, data_array):
        data = LightEvent()
        
        if len(data_array) != cls.get_size():
            return None

        data.event, data.interval, data.repeat = unpack('<BHB', data_array)

        return data



class LightModeColor(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.color      = Color()


    @classmethod
    def get_size(cls):
        return LightMode.get_size() + Color.get_size()


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.mode.to_array())
        data_array.extend(self.color.to_array())
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = LightModeColor()
        
        if len(data_array) != cls.get_size():
            return None

        index_start = 0;         index_end = LightMode.get_size();      data.mode       = LightMode.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += Color.get_size();         data.color      = Color.parse(data_array[index_start:index_end])
        return data



class LightModeColors(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.colors     = Colors.BLACK


    @classmethod
    def get_size(cls):
        return LightMode.get_size() + 1


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.mode.to_array())
        data_array.extend(pack('<B', self.colors.value))
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = LightModeColors()
        
        if len(data_array) != cls.get_size():
            return None

        index_start = 0;         index_end = LightMode.get_size();     data.mode       = LightMode.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += 1;                       data.colors,    = unpack('<B', data_array[index_start:index_end])

        data.colors     = Colors(data.colors)

        return data



class LightEventColor(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.color      = Color()


    @classmethod
    def get_size(cls):
        return LightEvent.get_size() + Color.get_size()


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.event.to_array())
        data_array.extend(self.color.to_array())
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = LightEventColor()
        
        if len(data_array) != cls.get_size():
            return None

        index_start = 0;         index_end = LightEvent.get_size();     data.event      = LightEvent.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += Color.get_size();         data.command    = Color.parse(data_array[index_start:index_end])
        
        return data



class LightEventColors(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.colors     = Colors.BLACK


    @classmethod
    def get_size(cls):
        return LightEvent.get_size() + 1


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.event.to_array())
        data_array.extend(pack('<B', self.colors.value))
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = LightEventColors()
        
        if len(data_array) != cls.get_size():
            return None

        index_start = 0;         index_end = LightEvent.get_size();    data.event      = LightEvent.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += 1;                       data.colors,    = unpack('<B', data_array[index_start:index_end])

        data.colors     = Colors(data.colors)

        return data


# Light End



# Display Start


class DisplayPixel(Enum):
    
    BLACK               = 0X00
    WHITE               = 0X01
    INVERSE             = 0X02
    OUTLINE             = 0X03



class DisplayFont(Enum):
    
    LIBERATION_MONO_5X8   = 0X00
    LIBERATION_MONO_10X16 = 0X01



class DisplayAlign(Enum):
    
    LEFT                = 0X00
    CENTER              = 0X01
    RIGHT               = 0X02



class DisplayLine(Enum):
    
    SOLID               = 0X00
    DOTTED              = 0X01
    DASHED              = 0X02



class DisplayClearAll(ISerializable):

    def __init__(self):
        self.pixel       = DisplayPixel.WHITE


    @classmethod
    def get_size(cls):
        return 1


    def to_array(self):
        return pack('<B', self.pixel.value)


    @classmethod
    def parse(cls, data_array):
        data = DisplayClearAll()
        
        if len(data_array) != cls.get_size():
            return None

        data.pixel, = unpack('<B', data_array)
        data.pixel  = DisplayPixel(data.pixel)
        
        return data



class DisplayClear(ISerializable):

    def __init__(self):
        self.x           = 0
        self.y           = 0
        self.width       = 0
        self.height      = 0
        self.pixel       = DisplayPixel.WHITE


    @classmethod
    def get_size(cls):
        return 9


    def to_array(self):
        return pack('<hhhhB', self.x, self.y, self.width, self.height, self.pixel.value)


    @classmethod
    def parse(cls, data_array):
        data = DisplayClear()
        
        if len(data_array) != cls.get_size():
            return None

        data.x, data.y, data.width, data.height, data.pixel = unpack('<hhhhB', data_array)

        data.pixel = DisplayPixel(data.pixel)
        
        return data



class DisplayInvert(ISerializable):

    def __init__(self):
        self.x           = 0
        self.y           = 0
        self.width       = 0
        self.height      = 0


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<hhhh', self.x, self.y, self.width, self.height)


    @classmethod
    def parse(cls, data_array):
        data = DisplayInvert()
        
        if len(data_array) != cls.get_size():
            return None

        data.x, data.y, data.width, data.height = unpack('<hhhh', data_array)
        
        return data



class DisplayDrawPoint(ISerializable):

    def __init__(self):
        self.x           = 0
        self.y           = 0
        self.pixel       = DisplayPixel.WHITE


    @classmethod
    def get_size(cls):
        return 5


    def to_array(self):
        return pack('<hhB', self.x, self.y, self.pixel.value)


    @classmethod
    def parse(cls, data_array):
        data = DisplayDrawPoint()
        
        if len(data_array) != cls.get_size():
            return None

        data.x, data.y, data.pixel = unpack('<hhB', data_array)

        data.pixel = DisplayPixel(data.pixel)
        
        return data



class DisplayDrawLine(ISerializable):

    def __init__(self):
        self.x1          = 0
        self.y1          = 0
        self.x2          = 0
        self.y2          = 0
        self.pixel       = DisplayPixel.WHITE
        self.line        = DisplayLine.SOLID


    @classmethod
    def get_size(cls):
        return 10


    def to_array(self):
        return pack('<hhhhBB', self.x1, self.y1, self.x2, self.y2, self.pixel.value, self.line.value)


    @classmethod
    def parse(cls, data_array):
        data = DisplayDrawLine()
        
        if len(data_array) != cls.get_size():
            return None

        data.x1, data.y1, data.x2, data.y2, data.pixel, data.line = unpack('<hhhhBB', data_array)

        data.pixel  = DisplayPixel(data.pixel)
        data.line   = DisplayLine(data.line)
        
        return data



class DisplayDrawRect(ISerializable):

    def __init__(self):
        self.x          = 0
        self.y          = 0
        self.width      = 0
        self.height     = 0
        self.pixel      = DisplayPixel.WHITE
        self.flag_fill  = True
        self.line       = DisplayLine.SOLID


    @classmethod
    def get_size(cls):
        return 11


    def to_array(self):
        return pack('<hhhhB?B', self.x, self.y, self.width, self.height, self.pixel.value, self.flag_fill, self.line.value)


    @classmethod
    def parse(cls, data_array):
        data = DisplayDrawRect()
        
        if len(data_array) != cls.get_size():
            return None

        data.x, data.y, data.width, data.height, data.pixel, data.flag_fill, data.line = unpack('<hhhhB?B', data_array)

        data.pixel  = DisplayPixel(data.pixel)
        data.line   = DisplayLine(data.line)
        
        return data



class DisplayDrawCircle(ISerializable):

    def __init__(self):
        self.x          = 0
        self.y          = 0
        self.radius     = 0
        self.pixel      = DisplayPixel.WHITE
        self.flag_fill  = True


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<hhhB?', self.x, self.y, self.radius, self.pixel.value, self.flag_fill)


    @classmethod
    def parse(cls, data_array):
        data = DisplayDrawCircle()
        
        if len(data_array) != cls.get_size():
            return None

        data.x, data.y, data.radius, data.pixel, data.flag_fill = unpack('<hhhB?', data_array)

        data.pixel = DisplayPixel(data.pixel)
        
        return data



class DisplayDrawString(ISerializable):

    def __init__(self):
        self.x          = 0
        self.y          = 0
        self.font       = DisplayFont.LIBERATION_MONO_5X8
        self.pixel      = DisplayPixel.WHITE
        self.message    = ""


    @classmethod
    def get_size(cls):
        return 6


    def get_size_total(self):
        return self.get_size() + len(self.message)


    def to_array(self):
        data_array = bytearray()
        data_array.extend(pack('<hhBB', self.x, self.y, self.font.value, self.pixel.value))
        data_array.extend(self.message.encode('ascii', 'ignore'))
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = DisplayDrawString()
        
        if len(data_array) <= cls.get_size():
            return None

        data.x, data.y, data.font, data.pixel = unpack('<hhBB', data_array[0:cls.get_size()])

        data.font       = DisplayFont(data.font)
        data.pixel      = DisplayPixel(data.pixel)
        data.message    = data_array[cls.get_size():len(data_array)].decode()
        
        return data



class DisplayDrawStringAlign(ISerializable):

    def __init__(self):
        
        self.x_start    = 0
        self.x_end      = 0
        self.y          = 0
        self.align      = DisplayAlign.CENTER
        self.font       = DisplayFont.LIBERATION_MONO_5X8
        self.pixel      = DisplayPixel.WHITE
        self.message    = ""


    @classmethod
    def get_size(cls):
        return 9



    def get_size_total(self):
        return self.get_size() + len(self.message)



    def to_array(self):
        data_array = bytearray()
        data_array.extend(pack('<hhhBBB', self.x_start, self.x_end, self.y, self.align.value, self.font.value, self.pixel.value))
        data_array.extend(self.message.encode('ascii', 'ignore'))
        return data_array
    

    @classmethod
    def parse(cls, data_array):
        data = DisplayDrawStringAlign()
        
        if len(data_array) <= cls.get_size():
            return None

        data.x_start, data.x_end, data.y, data.align, data.font, data.pixel, data.message = unpack('<hhhBBBs', data_array[0:cls.get_size()])
        data.align   = DisplayAlign(data.align)
        data.font    = DisplayFont(data.font)
        data.pixel   = DisplayPixel(data.pixel)
        data.message = data_array[cls.get_size():len(data_array)].decode()
        
        return data



class DisplayImage(ISerializable):

    def __init__(self):
        self.x          = 0
        self.y          = 0
        self.width      = 0
        self.height     = 0
        self.image      = bytearray()


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        data_array = bytearray()
        data_array.extend(pack('<hhhh', self.x, self.y, self.width, self.height))
        data_array.extend(self.image)
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = DisplayImage()
        
        if len(data_array) <= cls.get_size():
            return None

        data.x, data.y, data.width, data.height = unpack('<hhhh', data_array)
        data.image = data_array[cls.get_size():(len(data_array) - cls.get_size())]
        
        return data


# Display End



# Buzzer Start


class BuzzerMode(Enum):

    STOP                = 0     # 정지(Mode에서의 Stop은 통신에서 받았을 때 Buzzer를 끄는 용도로 사용, set으로만 호출)

    MUTE                = 1     # 묵음 즉시 적용
    MUTE_RESERVE        = 2     # 묵음 예약

    SCALE               = 3     # 음계 즉시 적용
    SCALE_RESERVE       = 4     # 음계 예약

    HZ                  = 5     # 주파수 즉시 적용
    HZ_RESERVE          = 6     # 주파수 예약

    END_OF_TYPE         = 7



class BuzzerScale(Enum):

    C1 = 0x00; CS1 = 0x01; D1 = 0x02; DS1 = 0x03; E1 = 0x04; F1 = 0x05; FS1 = 0x06; G1 = 0x07; GS1 = 0x08; A1 = 0x09; AS1 = 0x0A; B1 = 0x0B
    C2 = 0x0C; CS2 = 0x0D; D2 = 0x0E; DS2 = 0x0F; E2 = 0x10; F2 = 0x11; FS2 = 0x12; G2 = 0x13; GS2 = 0x14; A2 = 0x15; AS2 = 0x16; B2 = 0x17
    C3 = 0x18; CS3 = 0x19; D3 = 0x1A; DS3 = 0x1B; E3 = 0x1C; F3 = 0x1D; FS3 = 0x1E; G3 = 0x1F; GS3 = 0x20; A3 = 0x21; AS3 = 0x22; B3 = 0x23
    C4 = 0x24; CS4 = 0x25; D4 = 0x26; DS4 = 0x27; E4 = 0x28; F4 = 0x29; FS4 = 0x2A; G4 = 0x2B; GS4 = 0x2C; A4 = 0x2D; AS4 = 0x2E; B4 = 0x2F

    C5 = 0x30; CS5 = 0x31; D5 = 0x32; DS5 = 0x33; E5 = 0x34; F5 = 0x35; FS5 = 0x36; G5 = 0x37; GS5 = 0x38; A5 = 0x39; AS5 = 0x3A; B5 = 0x3B
    C6 = 0x3C; CS6 = 0x3D; D6 = 0x3E; DS6 = 0x3F; E6 = 0x40; F6 = 0x41; FS6 = 0x42; G6 = 0x43; GS6 = 0x44; A6 = 0x45; AS6 = 0x46; B6 = 0x47
    C7 = 0x48; CS7 = 0x49; D7 = 0x4A; DS7 = 0x4B; E7 = 0x4C; F7 = 0x4D; FS7 = 0x4E; G7 = 0x4F; GS7 = 0x50; A7 = 0x51; AS7 = 0x52; B7 = 0x53
    C8 = 0x54; CS8 = 0x55; D8 = 0x56; DS8 = 0x57; E8 = 0x58; F8 = 0x59; FS8 = 0x5A; G8 = 0x5B; GS8 = 0x5C; A8 = 0x5D; AS8 = 0x5E; B8 = 0x5F

    END_OF_TYPE   = 0x60

    MUTE        = 0xEE  # 묵음
    FIN         = 0xFF  # 악보의 끝



class Buzzer(ISerializable):

    def __init__(self):
        self.mode       = BuzzerMode.STOP
        self.value      = 0
        self.time       = 0


    @classmethod
    def get_size(cls):
        return 5


    def to_array(self):
        return pack('<BHH', self.mode.value, self.value, self.time)


    @classmethod
    def parse(cls, data_array):
        data = Buzzer()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.mode, data.value, data.time = unpack('<BHH', data_array)

        data.mode = BuzzerMode(data.mode)

        return data


# Buzzer End



# Vibrator Start


class VibratorMode(Enum):

    STOP            = 0     # 정지

    INSTANTLY       = 1     # 즉시 적용
    CONTINUALLY     = 2     # 예약

    END_OF_TYPE     = 3



class Vibrator(ISerializable):

    def __init__(self):
        self.mode       = VibratorMode.STOP
        self.on         = 0
        self.off        = 0
        self.total      = 0


    @classmethod
    def get_size(cls):
        return 7


    def to_array(self):
        return pack('<BHHH', self.mode.value, self.on, self.off, self.total)


    @classmethod
    def parse(cls, data_array):
        data = Vibrator()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.mode, data.on, data.off, data.total = unpack('<BHHH', data_array)

        data.mode = VibratorMode(data.mode)

        return data


# Vibrator End



# Button Start


class ButtonFlagController(Enum):

    NONE                = 0x0000

    FRONT_LEFT_TOP      = 0x0001
    FRONT_LEFT_BOTTOM   = 0x0002
    FRONT_RIGHT_TOP     = 0x0004
    FRONT_RIGHT_BOTTOM  = 0x0008

    TOP_LEFT            = 0x0010
    TOP_RIGHT           = 0x0020    # POWER ON/OFF

    MID_UP              = 0x0040
    MID_LEFT            = 0x0080
    MID_RIGHT           = 0x0100
    MID_DOWN            = 0x0200

    BOTTOM_LEFT         = 0x0400
    BOTTOM_RIGHT        = 0x0800



class ButtonFlagDrone(Enum):

    NONE        = 0x0000
    
    RESET       = 0x0001



class ButtonEvent(Enum):

    NONE                = 0x00
    
    DOWN                = 0x01  # 누르기 시작
    PRESS               = 0x02  # 누르는 중
    UP                  = 0x03  # 뗌
    
    END_CONTINUE_PRESS  = 0x04  # 연속 입력 종료



class Button(ISerializable):

    def __init__(self):
        self.button     = 0
        self.event      = ButtonEvent.NONE


    @classmethod
    def get_size(cls):
        return 3


    def to_array(self):
        return pack('<HB', self.button, self.event.value)


    @classmethod
    def parse(cls, data_array):
        data = Button()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.button, data.event = unpack('<HB', data_array)

        data.event = ButtonEvent(data.event)
        
        return data


# Button End



# Joystick Start


class JoystickDirection(Enum):

    NONE   = 0         # 정의하지 않은 영역(무시함)

    VT      = 0x10      #   위(세로)
    VM      = 0x20      # 중앙(세로)
    VB      = 0x40      # 아래(세로)

    HL      = 0x01      #   왼쪽(가로)
    HM      = 0x02      #   중앙(가로)
    HR      = 0x04      # 오른쪽(가로)

    TL = 0x11;  TM = 0x12;  TR = 0x14
    ML = 0x21;  CN = 0x22;  MR = 0x24
    BL = 0x41;  BM = 0x42;  BR = 0x44



class JoystickEvent(Enum):

    NONE        = 0     # 이벤트 없음
    
    IN          = 1     # 특정 영역에 진입
    STAY        = 2     # 특정 영역에서 상태 유지
    OUT         = 3     # 특정 영역에서 벗어남
    
    END_OF_TYPE = 4



class JoystickBlock(ISerializable):

    def __init__(self):
        self.x          = 0
        self.y          = 0
        self.direction  = JoystickDirection.NONE
        self.event      = JoystickEvent.NONE


    @classmethod
    def get_size(cls):
        return 4


    def to_array(self):
        return pack('<bbBB', self.x, self.y, self.direction.value, self.event.value)


    @classmethod
    def parse(cls, data_array):
        data = JoystickBlock()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.x, data.y, data.direction, data.event = unpack('<bbBB', data_array)

        data.direction  = JoystickDirection(data.direction)
        data.event      = JoystickEvent(data.event)

        return data



class Joystick(ISerializable):

    def __init__(self):
        self.left       = JoystickBlock()
        self.right      = JoystickBlock()


    @classmethod
    def get_size(cls):
        return JoystickBlock().get_size() * 2


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.left.to_array())
        data_array.extend(self.right.to_array())
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = Joystick()
        
        if len(data_array) != cls.get_size():
            return None
        
        index_start = 0;         index_end  = JoystickBlock.get_size();     data.left   = JoystickBlock.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += JoystickBlock.get_size();     data.right  = JoystickBlock.parse(data_array[index_start:index_end])

        return data


# Joystick End



# Sensor Raw Start


class RawMotion(ISerializable):

    def __init__(self):
        self.accel_x     = 0
        self.accel_y     = 0
        self.accel_z     = 0
        self.gyro_roll   = 0
        self.gyro_pitch  = 0
        self.gyro_yaw    = 0


    @classmethod
    def get_size(cls):
        return 12


    def to_array(self):
        return pack('<hhhhhh', self.accel_x, self.accel_y, self.accel_z, self.gyro_roll, self.gyro_pitch, self.gyro_yaw)


    @classmethod
    def parse(cls, data_array):
        data = RawMotion()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.accel_x, data.accel_y, data.accel_z, data.gyro_roll, data.gyro_pitch, data.gyro_yaw = unpack('<hhhhhh', data_array)
        
        return data



class RawFlow(ISerializable):

    def __init__(self):
        self.x     = 0
        self.y     = 0


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<ff', self.x, self.y)


    @classmethod
    def parse(cls, data_array):
        data = RawFlow()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.x, data.y = unpack('<ff', data_array)
        
        return data


# Sensor Raw End



# Information Start


class State(ISerializable):

    def __init__(self):
        self.mode_system          = ModeSystem.NONE
        self.mode_flight          = ModeFlight.NONE
        self.mode_control_flight  = ModeControlFlight.NONE
        self.mode_movement        = ModeMovement.NONE
        self.headless             = Headless.NONE
        self.control_speed        = 0
        self.sensor_orientation   = SensorOrientation.NONE
        self.battery              = 0


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<BBBBBBBB', self.mode_system.value, self.mode_flight.value, self.mode_control_flight.value, self.mode_movement.value, self.headless.value, self.control_speed, self.sensor_orientation.value, self.battery)


    @classmethod
    def parse(cls, data_array):
        data = State()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.mode_system, data.mode_flight, data.mode_control_flight, data.mode_movement, data.headless, data.control_speed, data.sensor_orientation, data.battery = unpack('<BBBBBBBB', data_array)

        data.mode_system          = ModeSystem(data.mode_system)
        data.mode_flight          = ModeFlight(data.mode_flight)
        data.mode_control_flight  = ModeControlFlight(data.mode_control_flight)
        data.mode_movement        = ModeMovement(data.mode_movement)
        data.headless             = Headless(data.headless)
        data.sensor_orientation   = SensorOrientation(data.sensor_orientation)
        
        return data



class Attitude(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0


    @classmethod
    def get_size(cls):
        return 6


    def to_array(self):
        return pack('<hhh', self.roll, self.pitch, self.yaw)


    @classmethod
    def parse(cls, data_array):
        data = Attitude()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.roll, data.pitch, data.yaw = unpack('<hhh', data_array)
        
        return data
        


class Position(ISerializable):

    def __init__(self):
        self.x      = 0
        self.y      = 0
        self.z      = 0


    @classmethod
    def get_size(cls):
        return 12


    def to_array(self):
        return pack('<fff', self.x, self.y, self.z)


    @classmethod
    def parse(cls, data_array):
        data = Position()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.x, data.y, data.z = unpack('<fff', data_array)
        
        return data



class Altitude(ISerializable):

    def __init__(self):
        self.temperature    = 0
        self.pressure       = 0
        self.altitude       = 0
        self.range_height   = 0


    @classmethod
    def get_size(cls):
        return 16


    def to_array(self):
        return pack('<ffff', self.temperature, self.pressure, self.altitude, self.range_height)


    @classmethod
    def parse(cls, data_array):
        data = Altitude()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.temperature, data.pressure, data.altitude, data.range_height = unpack('<ffff', data_array)
        
        return data



class Motion(ISerializable):

    def __init__(self):
        self.accel_x     = 0
        self.accel_y     = 0
        self.accel_z     = 0
        self.gyro_roll   = 0
        self.gyro_pitch  = 0
        self.gyro_yaw    = 0
        self.angle_roll  = 0
        self.angle_pitch = 0
        self.angle_yaw   = 0


    @classmethod
    def get_size(cls):
        return 18


    def to_array(self):
        return pack('<hhhhhhhhh', self.accel_x, self.accel_y, self.accel_z, self.gyro_roll, self.gyro_pitch, self.gyro_yaw, self.angle_roll, self.angle_pitch, self.angle_yaw)


    @classmethod
    def parse(cls, data_array):
        data = Motion()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.accel_x, data.accel_y, data.accel_z, data.gyro_roll, data.gyro_pitch, data.gyro_yaw, data.angle_roll, data.angle_pitch, data.angle_yaw = unpack('<hhhhhhhhh', data_array)
        
        return data



class Range(ISerializable):

    def __init__(self):
        self.left       = 0
        self.front      = 0
        self.right      = 0
        self.rear       = 0
        self.top        = 0
        self.bottom     = 0


    @classmethod
    def get_size(cls):
        return 12


    def to_array(self):
        return pack('<hhhhhh', self.left, self.front, self.right, self.rear, self.top, self.bottom)


    @classmethod
    def parse(cls, data_array):
        data = Range()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.left, data.front, data.right, data.rear, data.top, data.bottom = unpack('<hhhhhh', data_array)
        
        return data



class Trim(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0
        self.throttle   = 0


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<hhhh', self.roll, self.pitch, self.yaw, self.throttle)


    @classmethod
    def parse(cls, data_array):
        data = Trim()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.roll, data.pitch, data.yaw, data.throttle = unpack('<hhhh', data_array)
        
        return data


# Information End



# Sensor Start


class Vector(ISerializable):

    def __init__(self):
        self.x      = 0
        self.y      = 0
        self.z      = 0


    @classmethod
    def get_size(cls):
        return 6


    def to_array(self):
        return pack('<hhh', self.x, self.y, self.z)


    @classmethod
    def parse(cls, data_array):
        data = Vector()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.x, data.y, data.z = unpack('<hhh', data_array)
        
        return data



class Count(ISerializable):

    def __init__(self):
        self.time_flight     = 0

        self.count_takeoff   = 0
        self.count_landing   = 0
        self.count_accident  = 0


    @classmethod
    def get_size(cls):
        return 14


    def to_array(self):
        return pack('<QHHH', self.time_flight, self.count_takeoff, self.count_landing, self.count_accident)


    @classmethod
    def parse(cls, data_array):
        data = Count()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.time_flight, data.count_takeoff, data.count_landing, data.count_accident = unpack('<QHHH', data_array)
        
        return data



class Bias(ISerializable):
    
    def __init__(self):
        self.accel_x     = 0
        self.accel_y     = 0
        self.accel_z     = 0
        self.gyro_roll   = 0
        self.gyro_pitch  = 0
        self.gyro_yaw    = 0


    @classmethod
    def get_size(cls):
        return 12


    def to_array(self):
        return pack('<hhhhhh', self.accel_x, self.accel_y, self.accel_z, self.gyro_roll, self.gyro_pitch, self.gyro_yaw)


    @classmethod
    def parse(cls, data_array):
        data = Bias()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.accel_x, data.accel_y, data.accel_z, data.gyro_roll, data.gyro_pitch, data.gyro_yaw = unpack('<hhhhhh', data_array)
        
        return data



class Weight(ISerializable):

    def __init__(self):
        self.weight     = 0


    @classmethod
    def get_size(cls):
        return 4


    def to_array(self):
        return pack('<f', self.weight)


    @classmethod
    def parse(cls, data_array):
        data = Weight()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.weight, = unpack('<f', data_array)
        
        return data



class LostConnection(ISerializable):

    def __init__(self):
        self.time_neutral    = 0
        self.time_landing    = 0
        self.time_stop       = 0


    @classmethod
    def get_size(cls):
        return 8


    def to_array(self):
        return pack('<HHI', self.time_neutral, self.time_landing, self.time_stop)


    @classmethod
    def parse(cls, data_array):
        data = LostConnection()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.time_neutral, data.time_landing, data.time_stop = unpack('<HHI', data_array)
        
        return data


# Sensor End



# Device Start


class MotorBlock(ISerializable):

    def __init__(self):
        self.value      = 0


    @classmethod
    def get_size(cls):
        return 2


    def to_array(self):
        return pack('<h', self.value)


    @classmethod
    def parse(cls, data_array):
        data = MotorBlock()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.value, = unpack('<h', data_array)
        
        return data



class Motor(ISerializable):

    def __init__(self):
        self.motor      = []
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())


    @classmethod
    def get_size(cls):
        return MotorBlock.get_size() * 4


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.motor[0].to_array())
        data_array.extend(self.motor[1].to_array())
        data_array.extend(self.motor[2].to_array())
        data_array.extend(self.motor[3].to_array())
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = Motor()
        
        if len(data_array) != cls.get_size():
            return None
        
        index_start = 0;         index_end  = MotorBlock.get_size();    data.motor[0]   = MotorBlock.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += MotorBlock.get_size();    data.motor[1]   = MotorBlock.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += MotorBlock.get_size();    data.motor[2]   = MotorBlock.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += MotorBlock.get_size();    data.motor[3]   = MotorBlock.parse(data_array[index_start:index_end])
        
        return data


class MotorBlockRotationValue(ISerializable):

    def __init__(self):
        self.rotation   = Rotation.NONE
        self.value      = 0


    @classmethod
    def get_size(cls):
        return 3


    def to_array(self):
        return pack('<Bh', self.rotation.value, self.value)


    @classmethod
    def parse(cls, data_array):
        data = MotorBlockRotationValue()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.rotation, data.value = unpack('<Bh', data_array)
        data.rotation = Rotation(data.rotation)
        
        return data



class MotorRotationValue(ISerializable):

    def __init__(self):
        self.motor = []
        self.motor.append(MotorBlockRotationValue())
        self.motor.append(MotorBlockRotationValue())
        self.motor.append(MotorBlockRotationValue())
        self.motor.append(MotorBlockRotationValue())


    @classmethod
    def get_size(cls):
        return MotorBlockRotationValue.get_size() * 4


    def to_array(self):
        data_array = bytearray()
        data_array.extend(self.motor[0].to_array())
        data_array.extend(self.motor[1].to_array())
        data_array.extend(self.motor[2].to_array())
        data_array.extend(self.motor[3].to_array())
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = MotorRotationValue()
        
        if len(data_array) != cls.get_size():
            return None
        
        index_start = 0;         index_end  = MotorBlockRotationValue.get_size();    data.motor[0]   = MotorBlockRotationValue.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += MotorBlockRotationValue.get_size();    data.motor[1]   = MotorBlockRotationValue.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += MotorBlockRotationValue.get_size();    data.motor[2]   = MotorBlockRotationValue.parse(data_array[index_start:index_end])
        index_start = index_end; index_end += MotorBlockRotationValue.get_size();    data.motor[3]   = MotorBlockRotationValue.parse(data_array[index_start:index_end])
        
        return data



class MotorSingle(ISerializable):

    def __init__(self):
        self.target     = 0
        self.value      = 0


    @classmethod
    def get_size(cls):
        return 3


    def to_array(self):
        return pack('<Bh', self.target, self.value)


    @classmethod
    def parse(cls, data_array):
        data = MotorSingle()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.target, data.value = unpack('<Bh', data_array)
        
        return data



class MotorSingleRotationValue(ISerializable):

    def __init__(self):
        self.target     = 0
        self.rotation   = Rotation.NONE
        self.value      = 0


    @classmethod
    def get_size(cls):
        return 4


    def to_array(self):
        return pack('<BBh', self.target, self.rotation.value, self.value)


    @classmethod
    def parse(cls, data_array):
        data = MotorSingleRotationValue()
        
        if len(data_array) != cls.get_size():
            return None
        
        data.target, data.rotation, data.value = unpack('<BBh', data_array)
        data.rotation = Rotation(data.rotation)
        
        return data



class InformationAssembledForController(ISerializable):

    def __init__(self):
        self.angle_roll     = 0
        self.angle_pitch    = 0
        self.angle_yaw      = 0
        
        self.rpm            = 0
        
        self.position_x     = 0
        self.position_y     = 0
        self.position_z     = 0
        
        self.speed_x        = 0
        self.speed_y        = 0
        
        self.range_height   = 0
        
        self.rssi           = 0


    @classmethod
    def get_size(cls):
        return 18


    def to_array(self):
        return pack('<hhhHhhhbbBb', self.angle_roll, self.angle_pitch, self.angle_yaw, 
                                    self.rpm, 
                                    self.position_x, self.position_y, self.position_z, 
                                    self.speed_x, self.speed_y, 
                                    self.range_height, 
                                    self.rssi)


    @classmethod
    def parse(cls, data_array):
        data = InformationAssembledForController()
        
        if len(data_array) != cls.get_size():
            return None
        
        (data.angle_roll, data.angle_pitch, data.angle_yaw, 
        data.rpm, 
        data.position_x, data.position_y, data.position_z, 
        data.speed_x, data.speed_y, 
        data.range_height, 
        data.rssi) = unpack('<hhhHhhhbbBb', data_array)
        
        return data



class InformationAssembledForEntry(ISerializable):

    def __init__(self):
        self.angle_roll      = 0
        self.angle_pitch     = 0
        self.angle_yaw       = 0
        
        self.position_x      = 0
        self.position_y      = 0
        self.position_z      = 0

        self.range_height    = 0
        self.altitude       = 0


    @classmethod
    def get_size(cls):
        return 18


    def to_array(self):
        return pack('<hhhhhhhf',    self.angle_roll, self.angle_pitch, self.angle_yaw, 
                                    self.position_x, self.position_y, self.position_z, 
                                    self.range_height, self.altitude)


    @classmethod
    def parse(cls, data_array):
        data = InformationAssembledForEntry()
        
        if len(data_array) != cls.get_size():
            return None
        
        (data.angle_roll, data.angle_pitch, data.angle_yaw, 
        data.position_x, data.position_y, data.position_z, 
        data.range_height, data.altitude) = unpack('<hhhhhhhf', data_array)
        
        return data


# Device End



# Cards Start


class CardClassify(ISerializable):
    
    def __init__(self):
        self.index      = 0
        self.cc         = [[[0 for i in range(2)] for j in range(3)] for k in range(6)]
        self.l          = [0 for i in range(2)]


    @classmethod
    def get_size(cls):
        return (1 + (2 * 3 * 6) + 2)


    def to_array(self):
        #             123456789012345678901234567890123456789
        return pack('<bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', 
                    self.index, 
                    self.cc[0][0][0], self.cc[0][0][1], self.cc[0][1][0], self.cc[0][1][1], self.cc[0][2][0], self.cc[0][2][1], 
                    self.cc[1][0][0], self.cc[1][0][1], self.cc[1][1][0], self.cc[1][1][1], self.cc[1][2][0], self.cc[1][2][1], 
                    self.cc[2][0][0], self.cc[2][0][1], self.cc[2][1][0], self.cc[2][1][1], self.cc[2][2][0], self.cc[2][2][1], 
                    self.cc[3][0][0], self.cc[3][0][1], self.cc[3][1][0], self.cc[3][1][1], self.cc[3][2][0], self.cc[3][2][1], 
                    self.cc[4][0][0], self.cc[4][0][1], self.cc[4][1][0], self.cc[4][1][1], self.cc[4][2][0], self.cc[4][2][1], 
                    self.cc[5][0][0], self.cc[5][0][1], self.cc[5][1][0], self.cc[5][1][1], self.cc[5][2][0], self.cc[5][2][1], 
                    self.l[0], self.l[1])


    @classmethod
    def parse(cls, data_array):
        data = CardClassify()
        
        if len(data_array) != cls.get_size():
            return None
        
        (   data.index, 
            data.cc[0][0][0], data.cc[0][0][1], data.cc[0][1][0], data.cc[0][1][1], data.cc[0][2][0], data.cc[0][2][1], 
            data.cc[1][0][0], data.cc[1][0][1], data.cc[1][1][0], data.cc[1][1][1], data.cc[1][2][0], data.cc[1][2][1], 
            data.cc[2][0][0], data.cc[2][0][1], data.cc[2][1][0], data.cc[2][1][1], data.cc[2][2][0], data.cc[2][2][1], 
            data.cc[3][0][0], data.cc[3][0][1], data.cc[3][1][0], data.cc[3][1][1], data.cc[3][2][0], data.cc[3][2][1], 
            data.cc[4][0][0], data.cc[4][0][1], data.cc[4][1][0], data.cc[4][1][1], data.cc[4][2][0], data.cc[4][2][1], 
            data.cc[5][0][0], data.cc[5][0][1], data.cc[5][1][0], data.cc[5][1][1], data.cc[5][2][0], data.cc[5][2][1], 
            data.l[0], data.l[1]) = unpack('<bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', data_array)
        
        return data



class CardRange(ISerializable):

    def __init__(self):
        self.range      = [[[0 for i in range(2)] for j in range(3)] for k in range(2)]


    @classmethod
    def get_size(cls):
        return ((2 * 3 * 2) * 2)


    def to_array(self):
        #             123456789012
        return pack('<hhhhhhhhhhhh', 
                    self.range[0][0][0], self.range[0][0][1], self.range[0][1][0], self.range[0][1][1], self.range[0][2][0], self.range[0][2][1], 
                    self.range[1][0][0], self.range[1][0][1], self.range[1][1][0], self.range[1][1][1], self.range[1][2][0], self.range[1][2][1])


    @classmethod
    def parse(cls, data_array):
        data = CardRange()
        
        if len(data_array) != cls.get_size():
            return None
        
        (   data.range[0][0][0], data.range[0][0][1], data.range[0][1][0], data.range[0][1][1], data.range[0][2][0], data.range[0][2][1], 
            data.range[1][0][0], data.range[1][0][1], data.range[1][1][0], data.range[1][1][1], data.range[1][2][0], data.range[1][2][1]) = unpack('<hhhhhhhhhhhh', data_array)

        return data



class CardRaw(ISerializable):

    def __init__(self):
        self.rgb_raw    = [[0 for i in range(3)] for j in range(2)]
        self.rgb        = [[0 for i in range(3)] for j in range(2)]     # 0 ~ 255
        self.hsvl       = [[0 for i in range(4)] for j in range(2)]     # H: 0 ~ 360, S: 0 ~ 100, V: 0 ~ 100, L: 0 ~ 100
        self.color      = [0 for i in range(2)]
        self.card       = 0


    @classmethod
    def get_size(cls):
        return (12 + 6 + 16 + 2 + 1)


    def to_array(self):
        #             12345678901234567890123
        return pack('<hhhhhhBBBBBBhhhhhhhhBBB', 
                    self.rgb_raw[0][0], self.rgb_raw[0][1] , self.rgb_raw[0][2], self.rgb_raw[1][0], self.rgb_raw[1][1] , self.rgb_raw[1][2], 
                    self.rgb[0][0], self.rgb[0][1] , self.rgb[0][2], self.rgb[1][0], self.rgb[1][1] , self.rgb[1][2], 
                    self.hsvl[0][0], self.hsvl[0][1] , self.hsvl[0][2], self.hsvl[0][3], self.hsvl[1][0], self.hsvl[1][1] , self.hsvl[1][2], self.hsvl[1][3], 
                    self.color[0].value, self.color[1].value , self.card.value)


    @classmethod
    def parse(cls, data_array):
        data = CardRaw()
        
        if len(data_array) != cls.get_size():
            return None
        
        (   data.rgb_raw[0][0], data.rgb_raw[0][1] , data.rgb_raw[0][2], data.rgb_raw[1][0], data.rgb_raw[1][1] , data.rgb_raw[1][2], 
            data.rgb[0][0], data.rgb[0][1] , data.rgb[0][2], data.rgb[1][0], data.rgb[1][1] , data.rgb[1][2], 
            data.hsvl[0][0], data.hsvl[0][1], data.hsvl[0][2], data.hsvl[0][3], data.hsvl[1][0], data.hsvl[1][1], data.hsvl[1][2], data.hsvl[1][3], 
            data.color[0], data.color[1] , data.card) = unpack('<hhhhhhhhhhhhhhhhhhBBBBBBhhhhhhBBB', data_array)

        data.color[0]   = CardColorIndex(data.color[0])
        data.color[1]   = CardColorIndex(data.color[1])
        data.card       = Card(data.card)
        
        return data



class CardColor(ISerializable):

    def __init__(self):
        self.hsvl       = [[0 for i in range(4)] for j in range(2)]     # H: 0 ~ 360, S: 0 ~ 100, V: 0 ~ 100, L: 0 ~ 100
        self.color      = [0 for i in range(2)]
        self.card       = 0


    @classmethod
    def get_size(cls):
        return (16 + 2 + 1)


    def to_array(self):
        #             12345678901
        return pack('<hhhhhhhhBBB', 
                    self.hsvl[0][0], self.hsvl[0][1] , self.hsvl[0][2], self.hsvl[0][3], self.hsvl[1][0], self.hsvl[1][1] , self.hsvl[1][2], self.hsvl[1][3], 
                    self.color[0].value, self.color[1].value , self.card.value)


    @classmethod
    def parse(cls, data_array):
        data = CardColor()
        
        if len(data_array) != cls.get_size():
            return None
        
        (   data.hsvl[0][0], data.hsvl[0][1], data.hsvl[0][2], data.hsvl[0][3], data.hsvl[1][0], data.hsvl[1][1], data.hsvl[1][2], data.hsvl[1][3], 
            data.color[0], data.color[1] , data.card) = unpack('<hhhhhhhhBBB', data_array)

        data.color[0]   = CardColorIndex(data.color[0])
        data.color[1]   = CardColorIndex(data.color[1])
        data.card       = Card(data.card)
        
        return data



class CardList(ISerializable):

    def __init__(self):
        self.index       = 0     # 현재 실행중인 카드 인덱스
        self.size        = 0     # 입력된 카드의 총 갯수

        self.card_index  = 0     # 다음 카드의 시작 번호
        self.card        = [0 for i in range(12)]


    @classmethod
    def get_size(cls):
        return 15


    def to_array(self):
        data_array = bytearray()
        data_array.extend(pack('<BBB', self.index, self.size, self.card_index))

        for i in range(0, 12):
            data_array.extend(pack('<B', self.card[i]))
        
        return data_array


    @classmethod
    def parse(cls, data_array):
        data = CardList()
        
        if len(data_array) < 4:
            return None
        
        data.index, data.size, data.card_index = unpack('<BBB', data_array[0:3])

        length_list = len(data_array) - 3

        for i in range(0, length_list):
            index_array = 3 + i;
            data.card[i], = unpack('<B', data_array[index_array:(index_array + 1)])
        
        return data


# Cards End



