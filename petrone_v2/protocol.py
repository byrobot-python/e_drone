import os
import abc 
import numpy as np
from struct import *
from enum import Enum

from petrone_v2.system import *


# ISerializable Start


class ISerializable:
    
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getSize(self):
        pass

    @abc.abstractmethod
    def ToArray(self):
        pass


# ISerializable End



# DataType Start


class DataType(Enum):
    
    None_               = 0x00      # 없음
    
    Ping                = 0x01      # 통신 확인
    Ack                 = 0x02      # 데이터 수신에 대한 응답
    Error               = 0x03      # 오류(reserve 비트 플래그는 추후에 지정)
    Request             = 0x04      # 지정한 타입의 데이터 요청
    Message             = 0x05      # 문자열 데이터
    Reserved_1          = 0x06      # 예약
    SystemInformation   = 0x07      # 시스템 정보
    Monitor             = 0x08      # 디버깅용 값 배열 전송. 첫번째 바이트에 타입 두 번째 바이트에 페이지 지정(수신 받는 데이터의 저장 경로 구분)
    SystemCounter       = 0x09      # 시스템 카운터
    Information         = 0x0A      # 장치 정보
    UpdateLocation      = 0x0B      # 펌웨어 업데이트 위치 정정
    Update              = 0x0C      # 펌웨어 업데이트
    Encrypt             = 0x0D      # 펌웨어 암호화
    Address             = 0x0E      # 장치 주소
    Administrator       = 0x0F      # 관리자 권한 획득
    Control             = 0x10      # 조종 명령

    Command             = 0x11      # 명령

    # Light
    LightManual                 = 0x20      # LED 수동 제어

    LightMode                   = 0x21      # LED 모드 지정
    LightModeCommand            = 0x22      # LED 모드 커맨드
    LightModeCommandIr          = 0x23      # LED 모드 커맨드 IR 데이터 송신
    LightModeColor              = 0x24      # LED 모드 3색 직접 지정
    LightModeColorCommand       = 0x25      # LED 모드 3색 직접 지정 커맨드
    LightModeColorCommandIr     = 0x26      # LED 모드 3색 직접 지정 커맨드 IR 데이터 송신
    LightModeColors             = 0x27      # LED 모드 팔레트의 색상으로 지정
    LightModeColorsCommand      = 0x28      # LED 모드 팔레트의 색상으로 지정 커맨드
    LightModeColorsCommandIr    = 0x29      # LED 모드 팔레트의 색상으로 지정 커맨드 IR 데이터 송신

    LightEvent                  = 0x2A      # LED 이벤트
    LightEventCommand           = 0x2B      # LED 이벤트 커맨드
    LightEventCommandIr         = 0x2C      # LED 이벤트 커맨드 IR 데이터 송신
    LightEventColor             = 0x2D      # LED 이벤트 3색 직접 지정
    LightEventColorCommand      = 0x2E      # LED 이벤트 3색 직접 지정 커맨드
    LightEventColorCommandIr    = 0x2F      # LED 이벤트 3색 직접 지정 커맨드 IR 데이터 송신
    LightEventColors            = 0x30      # LED 이벤트 팔레트의 색상으로 지정
    LightEventColorsCommand     = 0x31      # LED 이벤트 팔레트의 색상으로 지정 커맨드
    LightEventColorsCommandIr   = 0x32      # LED 이벤트 팔레트의 색상으로 지정 커맨드 IR 데이터 송신

    LightModeDefaultColor       = 0x33      # LED 초기 모드 3색 직접 지정

    # 상태 설정
    State           = 0x40      # 드론의 상태(비행 모드 방위기준 배터리량)
    Attitude        = 0x41      # 드론의 자세(Angle)
    AccelBias       = 0x42      # 엑셀 바이어스 값
    GyroBias        = 0x43      # 자이로 바이어스 값
    TrimAll         = 0x44      # 전체 트림
    TrimFlight      = 0x45      # 비행 트림
    TrimDrive       = 0x46      # 주행 트림

    # Sensor raw data
    Imu             = 0x50      # IMU Raw
    Pressure        = 0x51      # 압력 센서 데이터
    Battery         = 0x52      # 배터리
    Range           = 0x53      # 적외선 거리 센서
    ImageFlow       = 0x54      # ImageFlow
    CameraImage     = 0x55      # CameraImage

    # Input
    Button          = 0x70      # 버튼 입력
    Joystick        = 0x71      # 조이스틱 입력

    # Devices
    Motor           = 0x80      # 모터 제어 및 현재 제어값 확인
    MotorSingle     = 0x81      # 한 개의 모터 제어
    IrMessage       = 0x82      # IR 데이터 송수신
    Buzzer          = 0x83      # 부저 제어
    Vibrator        = 0x84      # 진동 제어

    # 카운트
    CountFlight     = 0x90      # 비행 관련 카운트
    CountDrive      = 0x91      # 주행 관련 카운트

    # RF
    Pairing         = 0xA0      # 페어링
    Rssi            = 0xA1      # RSSI

    # Display
    DisplayClear            = 0xB0      # 화면 지우기
    DisplayInvert           = 0xB1      # 화면 반전
    DisplayDrawPoint        = 0xB2      # 점 그리기
    DisplayDrawLine         = 0xB3      # 선 그리기
    DisplayDrawRect         = 0xB4      # 사각형 그리기
    DisplayDrawCircle       = 0xB5      # 원 그리기
    DisplayDrawString       = 0xB6      # 문자열 쓰기
    DisplayDrawStringAlign  = 0xB7      # 문자열 쓰기

    EndOfType               = 0xB8


# DataType End



# CommandType Start


class CommandType(Enum):
    
    None_               = 0x00      # 없음

    # 설정
    ModeVehicle         = 0x10      # Vehicle 동작 모드 전환

    # 제어
    Headless            = 0x20      # 헤드리스 모드 선택
    Trim                = 0x21      # 트림 변경
    FlightEvent         = 0x22      # 비행 이벤트 실행
    DriveEvent          = 0x23      # 주행 이벤트 실행
    Stop                = 0x24      # 정지

    ClearTrim           = 0x50      # 트림 초기화
    ClearGyroBias       = 0x51      # 자이로 바이어스 리셋(트림도 같이 초기화 됨)

    DataStorageWrite    = 0x80      # 변경사항이 있는 경우 데이터 저장소에 기록

    # 관리자
    ClearCounter        = 0xA0      # 카운터 클리어(관리자 권한을 획득했을 경우에만 동작)
    SetTestComplete     = 0xA1      # 테스트 완료 처리

    EndOfType           = 0xA2


# CommandType End



# Header Start


class Header(ISerializable):

    def __init__(self):
        
        self.dataType    = DataType.None_
        self.length      = 0
        self.from_       = DeviceType.None_
        self.to_         = DeviceType.None_


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<BBBB', self.dataType.value, self.length, self.from_.value, self.to_.value)


    @classmethod
    def parse(cls, dataArray):
        header = Header()

        if len(dataArray) != cls.getSize():
            #print("{0}".format(dataArray.count))
            return None

        header.dataType, header.length, header.from_, header.to_ = unpack('<BBBB', dataArray)

        header.dataType = DataType(header.dataType)
        header.from_ = DeviceType(header.from_)
        header.to_ = DeviceType(header.to_)
        
        return header


# Header End



# Common Start


class Ping(ISerializable):

    def __init__(self):
        self.systemTime     = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<Q', self.systemTime)


    @classmethod
    def parse(cls, dataarray):
        data = Ping()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.systemTime = unpack('<Q', dataarray)
        return data



class Ack(ISerializable):

    def __init__(self):
        self.systemTime     = 0
        self.dataType       = DataType.None_
        self.crc16          = 0


    @classmethod
    def getSize(cls):
        return 11


    def toArray(self):
        return pack('<QBH', self.systemTime, self.dataType.value, self.crc16)


    @classmethod
    def parse(cls, dataarray):
        data = Ack()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.systemTime, data.dataType, data.crc16 = unpack('<QBH', dataarray)
        data.dataType = DataType(data.dataType)
        return data



class Request(ISerializable):

    def __init__(self):
        self.dataType    = DataType.None_


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<B', self.dataType.value)


    @classmethod
    def parse(cls, dataarray):
        data = Request()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.dataType = unpack('<B', dataarray)
        data.dataType = DataType(data.dataType)
        return data



class Version(ISerializable):

    def __init__(self):
        self.build          = 0
        self.stage          = DevelopmentStage.Alpha
        self.minor          = 0
        self.major          = 0

        self.v              = 0         # build, stage, minor, major을 하나의 UInt32로 묶은 것(버젼 비교 시 사용)


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<HBB', ((self.stage.value << 14) | self.build), self.minor, self.major)


    @classmethod
    def parse(cls, dataarray):
        data = Version()
        
        if len(dataarray) != cls.getSize():
            return None

        data.v = unpack('<I', dataarray)

        data.build, data.minor, data.major = unpack('<HBB', dataarray)
        data.stage = DevelopmentStage((data.build >> 14) & 0x03)
        data.build = data.build & 0xFFFC
        return data



class SystemInformation(ISerializable):

    def __init__(self):
        self.crc32bootloader    = 0
        self.crc32application   = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<II', self.crc32bootloader, self.crc32application)


    @classmethod
    def parse(cls, dataarray):
        data = SystemInformation()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.crc32bootloader, data.crc32application = unpack('<II', dataarray)
        return data



class Information(ISerializable):

    def __init__(self):
        self.modeUpdate     = ModeUpdate.None_

        self.deviceType     = DeviceType.None_
        self.version        = Version()

        self.year           = 0
        self.month          = 0
        self.day            = 0


    @classmethod
    def getSize(cls):
        return 13


    def toArray(self):
        dataArray = []
        dataArray.extend(pack('<B', self.modeUpdate.value))
        dataArray.extend(pack('<I', self.deviceType.value))
        dataArray.extend(self.imageVersion.toArray())
        dataArray.extend(pack('<H', self.year))
        dataArray.extend(pack('<B', self.month))
        dataArray.extend(pack('<B', self.day))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = Information()
        
        if len(dataarray) != cls.getSize():
            return None
        
        indexStart = 0;        indexEnd = 1;                        data.modeUpdate     = ModeUpdate(unpack('<B', dataArray[indexStart:indexEnd]))
        indexStart = indexEnd; indexEnd += 4;                       data.deviceType     = DeviceType(unpack('<I', dataArray[indexStart:indexEnd]))
        indexStart = indexEnd; indexEnd += Version.getSize();       data.imageVersion   = Version.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 2;                       data.year           = unpack('<H', dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.month          = unpack('<B', dataArray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.day            = unpack('<B', dataArray[indexStart:indexEnd])
        return data



class Address(ISerializable):

    def __init__(self):
        self.address    = bytearray()


    @classmethod
    def getSize(cls):
        return 16


    def toArray(self):
        return self.address


    @classmethod
    def parse(cls, dataarray):
        data = SystemInformation()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.address = dataarray[0:16]
        return data



class Command(ISerializable):

    def __init__(self):
        self.commandType    = CommandType.None_
        self.option         = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<BB', self.commandType.value, self.option)


    @classmethod
    def parse(cls, dataarray):
        data = Command()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.commandType, data.option = unpack('<BB', dataarray)
        data.commandType = CommandType(data.commandType)
        return data



class Pairing(ISerializable):

    def __init__(self):
        self.addressLocal   = 0
        self.addressRemote  = 0
        self.channel        = 0


    @classmethod
    def getSize(cls):
        return 5


    def toArray(self):
        return pack('<HHB', self.addressLocal, self.addressRemote, self.channel)


    @classmethod
    def parse(cls, dataarray):
        data = Pairing()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.addressLocal, data.addressRemote, data.channel = unpack('<HHB', dataarray)
        return data



class Rssi(ISerializable):

    def __init__(self):
        self.rssi       = 0


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<b', self.rssi)


    @classmethod
    def parse(cls, dataarray):
        data = Rssi()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.rssi = unpack('<b', dataarray)
        return data


# Common End



# Control Start


class ControlQuad8(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0
        self.throttle   = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<bbbb', self.roll, self.pitch, self.yaw, self.throttle)


    @classmethod
    def parse(cls, dataarray):
        data = ControlQuad8()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.roll, data.pitch, data.yaw, data.throttle = unpack('<bbbb', dataarray)
        return data



class ControlQuad16(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0
        self.throttle   = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<hhhh', self.roll, self.pitch, self.yaw, self.throttle)


    @classmethod
    def parse(cls, dataarray):
        data = ControlQuad16()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.roll, data.pitch, data.yaw, data.throttle = unpack('<hhhh', dataarray)
        return data



class ControlDouble8(ISerializable):

    def __init__(self):
        self.wheel      = 0
        self.accel      = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<bb', self.wheel, self.accel)


    @classmethod
    def parse(cls, dataarray):
        data = ControlDouble8()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.wheel, data.accel = unpack('<bb', dataarray)
        return data



class ControlDouble16(ISerializable):

    def __init__(self):
        self.wheel      = 0
        self.accel      = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<hh', self.wheel, self.accel)


    @classmethod
    def parse(cls, dataarray):
        data = ControlDouble16()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.wheel, data.accel = unpack('<hh', dataarray)
        return data



class TrimFlight(ControlQuad16):
    pass



class TrimDrive(ControlDouble16):
    pass


# Control End



# Light Start


class LightModeDrone(Enum):
    
    None_               = 0x00

    EyeNone             = 0x10
    EyeManual           = 0x11      # 수동 제어
    EyeHold             = 0x12      # 지정한 색상을 계속 켬
    EyeFlicker          = 0x13      # 깜빡임    	
    EyeFlickerDouble    = 0x14      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)    	
    EyeDimming          = 0x15      # 밝기 제어하여 천천히 깜빡임

    ArmNone             = 0x40
    ArmManual           = 0x41      # 수동 제어
    ArmHold             = 0x42      # 지정한 색상을 계속 켬
    ArmFlicker          = 0x43      # 깜빡임    	
    ArmFlickerDouble    = 0x44      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)    	
    ArmDimming          = 0x45      # 밝기 제어하여 천천히 깜빡임

    TailNone            = 0x70
    TailManual          = 0x71      # 수동 제어
    TailHold            = 0x72      # 지정한 색상을 계속 켬
    TailFlicker         = 0x73      # 깜빡임    	
    TailFlickerDouble   = 0x74      # 깜빡임(두 번 깜빡이고 깜빡인 시간만큼 꺼짐)    	
    TailDimming         = 0x75      # 밝기 제어하여 천천히 깜빡임

    EndOfType           = 0x76



class LightFlagsDrone(Enum):
    
    None_               = 0x00

    EyeRed              = 0x80
    EyeGreen            = 0x40
    EyeBlue             = 0x20

    ArmRed              = 0x10
    ArmGreen            = 0x08
    ArmBlue             = 0x04

    TailGreen           = 0x02


class LightModeController(Enum):
    
    None_               = 0x00

    TeamNone            = 0x10
    TeamManual          = 0x11      # 수동 조작
    TeamHold            = 0x12      
    TeamFlicker         = 0x13      
    TeamFlickerDouble   = 0x14      
    TeamDimming         = 0x15      

    EndOfType           = 0x16      



class LightFlagsController(Enum):
    
    None_               = 0x00

    Red                 = 0x80
    Green               = 0x40
    Blue                = 0x20



class Color(ISerializable):

    def __init__(self):
        self.r      = 0
        self.g      = 0
        self.b      = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<BBB', self.r, self.g, self.b)


    @classmethod
    def parse(cls, dataarray):
        data = Color()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.r, data.g, data.b = unpack('<BBB', dataarray)
        return data



class Colors(Enum):

    AliceBlue              = 0
    AntiqueWhite           = 1
    Aqua                   = 2
    Aquamarine             = 3
    Azure                  = 4
    Beige                  = 5
    Bisque                 = 6
    Black                  = 7
    BlanchedAlmond         = 8
    Blue                   = 9
    BlueViolet             = 10
    Brown                  = 11
    BurlyWood              = 12
    CadetBlue              = 13
    Chartreuse             = 14
    Chocolate              = 15
    Coral                  = 16
    CornflowerBlue         = 17
    Cornsilk               = 18
    Crimson                = 19
    Cyan                   = 20
    DarkBlue               = 21
    DarkCyan               = 22
    DarkGoldenRod          = 23
    DarkGray               = 24
    DarkGreen              = 25
    DarkKhaki              = 26
    DarkMagenta            = 27
    DarkOliveGreen         = 28
    DarkOrange             = 29
    DarkOrchid             = 30
    DarkRed                = 31
    DarkSalmon             = 32
    DarkSeaGreen           = 33
    DarkSlateBlue          = 34
    DarkSlateGray          = 35
    DarkTurquoise          = 36
    DarkViolet             = 37
    DeepPink               = 38
    DeepSkyBlue            = 39
    DimGray                = 40
    DodgerBlue             = 41
    FireBrick              = 42
    FloralWhite            = 43
    ForestGreen            = 44
    Fuchsia                = 45
    Gainsboro              = 46
    GhostWhite             = 47
    Gold                   = 48
    GoldenRod              = 49
    Gray                   = 50
    Green                  = 51
    GreenYellow            = 52
    HoneyDew               = 53
    HotPink                = 54
    IndianRed              = 55
    Indigo                 = 56
    Ivory                  = 57
    Khaki                  = 58
    Lavender               = 59
    LavenderBlush          = 60
    LawnGreen              = 61
    LemonChiffon           = 62
    LightBlue              = 63
    LightCoral             = 64
    LightCyan              = 65
    LightGoldenRodYellow   = 66
    LightGray              = 67
    LightGreen             = 68
    LightPink              = 69
    LightSalmon            = 70
    LightSeaGreen          = 71
    LightSkyBlue           = 72
    LightSlateGray         = 73
    LightSteelBlue         = 74
    LightYellow            = 75
    Lime                   = 76
    LimeGreen              = 77
    Linen                  = 78
    Magenta                = 79
    Maroon                 = 80
    MediumAquaMarine       = 81
    MediumBlue             = 82
    MediumOrchid           = 83
    MediumPurple           = 84
    MediumSeaGreen         = 85
    MediumSlateBlue        = 86
    MediumSpringGreen      = 87
    MediumTurquoise        = 88
    MediumVioletRed        = 89
    MidnightBlue           = 90
    MintCream              = 91
    MistyRose              = 92
    Moccasin               = 93
    NavajoWhite            = 94
    Navy                   = 95
    OldLace                = 96
    Olive                  = 97
    OliveDrab              = 98
    Orange                 = 99
    OrangeRed              = 100
    Orchid                 = 101
    PaleGoldenRod          = 102
    PaleGreen              = 103
    PaleTurquoise          = 104
    PaleVioletRed          = 105
    PapayaWhip             = 106
    PeachPuff              = 107
    Peru                   = 108
    Pink                   = 109
    Plum                   = 110
    PowderBlue             = 111
    Purple                 = 112
    RebeccaPurple          = 113
    Red                    = 114
    RosyBrown              = 115
    RoyalBlue              = 116
    SaddleBrown            = 117
    Salmon                 = 118
    SandyBrown             = 119
    SeaGreen               = 120
    SeaShell               = 121
    Sienna                 = 122
    Silver                 = 123
    SkyBlue                = 124
    SlateBlue              = 125
    SlateGray              = 126
    Snow                   = 127
    SpringGreen            = 128
    SteelBlue              = 129
    Tan                    = 130
    Teal                   = 131
    Thistle                = 132
    Tomato                 = 133
    Turquoise              = 134
    Violet                 = 135
    Wheat                  = 136
    White                  = 137
    WhiteSmoke             = 138
    Yellow                 = 139
    YellowGreen            = 140
    
    EndOfType              = 141



class LightManual(ISerializable):

    def __init__(self):
        self.flags          = 0
        self.brightness     = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<BB', self.flags, self.brightness)


    @classmethod
    def parse(cls, dataarray):
        data = LightManual()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.flags, data.brightness = unpack('<BB', dataarray)
        return data



class LightMode(ISerializable):

    def __init__(self):
        self.mode        = 0
        self.interval    = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<BH', self.mode, self.interval)


    @classmethod
    def parse(cls, dataarray):
        data = LightMode()
        
        if len(dataarray) != cls.getSize():
            return None

        data.mode, data.interval = unpack('<BH', dataarray)
        return data



class LightEvent(ISerializable):

    def __init__(self):
        self.event      = 0
        self.interval   = 0
        self.repeat     = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<BHB', self.event, self.interval, self.repeat)


    @classmethod
    def parse(cls, dataarray):
        data = LightEvent()
        
        if len(dataarray) != cls.getSize():
            return None

        data.event, data.interval, data.repeat = unpack('<BHB', dataarray)

        return data



class LightModeCommand(ISerializable):

    def __init__(self):
        self.mode       = LightMode()
        self.command    = Command()


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + Command.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(self.command.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeCommand()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();    data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();     data.command    = Command.parse(dataarray[indexStart:indexEnd])
        return data



class LightModeCommandIr(ISerializable):

    def __init__(self):
        self.mode       = LightMode()
        self.command    = Command()
        self.irData     = 0


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + Command.getSize() + 4


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(self.command.toArray())
        dataArray.extend(pack('<I', self.irData))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeCommandIr()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 4;                       data.irData     = unpack('<I', dataArray[indexStart:indexEnd])
        return data



class LightModeColor(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.color      = Color()


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + Color.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(self.color.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeColor()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();         data.color      = Color.parse(dataarray[indexStart:indexEnd])
        return data



class LightModeColorCommand(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.color      = Color()
        self.command    = Command()


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + Color.getSize() + Command.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(self.color.toArray())
        dataArray.extend(self.command.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeColorCommand()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();    data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();       data.color      = Color.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();     data.command    = Command.parse(dataarray[indexStart:indexEnd])
        return data



class LightModeColorCommandIr(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.color      = Color()
        self.command    = Command()
        self.irData     = 0


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + Color.getSize() + Command.getSize() + 4


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(self.color.toArray())
        dataArray.extend(self.command.toArray())
        dataArray.extend(pack('<I', self.irData))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeColorCommandIr()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();         data.color      = Color.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 4;                       data.irData     = unpack('<I', dataArray[indexStart:indexEnd])
        return data



class LightModeColors(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.colors     = Colors.Black


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + 1


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeColors()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors     = Colors(unpack('<B', dataArray[indexStart:indexEnd]))
        return data



class LightModeColorsCommand(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.colors     = Colors.Black
        self.command    = Command()


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + 1 + Command.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        dataArray.extend(self.command.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeColorsCommand()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors     = Colors(unpack('<B', dataArray[indexStart:indexEnd]))
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        return data



class LightModeColorsCommandIr(ISerializable):
    
    def __init__(self):
        self.mode       = LightMode()
        self.colors     = Colors.Black
        self.command    = Command()
        self.irData     = 0


    @classmethod
    def getSize(cls):
        return LightMode.getSize() + 1 + Command.getSize() + 4


    def toArray(self):
        dataArray = []
        dataArray.extend(self.mode.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        dataArray.extend(self.command.toArray())
        dataArray.extend(pack('<I', self.irData))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightModeColorsCommandIr()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightMode.getSize();      data.mode       = LightMode.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors     = Colors(unpack('<B', dataArray[indexStart:indexEnd]))
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 4;                       data.irData     = unpack('<I', dataArray[indexStart:indexEnd])
        return data



class LightEventCommand(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.command    = Command()


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + Command.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.command.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventCommand()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        return data



class LightEventCommandIr(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.command    = Command()
        self.irData     = 0


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + Command.getSize() + 4


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.command.toArray())
        dataArray.extend(pack('<I', self.irData))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventCommandIr()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 4;                       data.irData     = unpack('<I', dataArray[indexStart:indexEnd])
        return data



class LightEventColor(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.color      = Color()


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + Color.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.color.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventColor()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();         data.command    = Color.parse(dataarray[indexStart:indexEnd])
        return data



class LightEventColorCommand(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.color      = Color()
        self.command    = Command()


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + Color.getSize() + Command.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.color.toArray())
        dataArray.extend(self.command.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventColorCommand()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();         data.color      = Color.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        return data



class LightEventColorCommandIr(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.color      = Color()
        self.command    = Command()
        self.irData     = 0


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + Color.getSize() + Command.getSize() + 4


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(self.color.toArray())
        dataArray.extend(self.command.toArray())
        dataArray.extend(pack('<I', self.irData))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventColorCommandIr()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Color.getSize();         data.color      = Color.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 4;                       data.irData     = unpack('<I', dataArray[indexStart:indexEnd])
        return data



class LightEventColors(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.colors     = Colors.Black


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + 1


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventColors()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors     = Colors(unpack('<B', dataArray[indexStart:indexEnd]))
        return data



class LightEventColorsCommand(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.colors     = Colors.Black
        self.command    = Command()


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + 1 + Command.getSize()


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        dataArray.extend(self.command.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventColorsCommand()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors     = Colors(unpack('<B', dataArray[indexStart:indexEnd]))
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        return data



class LightEventColorsCommandIr(ISerializable):
    
    def __init__(self):
        self.event      = LightEvent()
        self.colors     = Colors.Black
        self.command    = Command()
        self.irData     = 0


    @classmethod
    def getSize(cls):
        return LightEvent.getSize() + 1 + Command.getSize() + 4


    def toArray(self):
        dataArray = []
        dataArray.extend(self.event.toArray())
        dataArray.extend(pack('<B', self.colors.value))
        dataArray.extend(self.command.toArray())
        dataArray.extend(pack('<I', self.irData))
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = LightEventColorsCommandIr()
        
        if len(dataarray) != cls.getSize():
            return None

        indexStart = 0;        indexEnd = LightEvent.getSize();     data.event      = LightEvent.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 1;                       data.colors     = Colors(unpack('<B', dataArray[indexStart:indexEnd]))
        indexStart = indexEnd; indexEnd += Command.getSize();       data.command    = Command.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += 4;                       data.irData     = unpack('<I', dataArray[indexStart:indexEnd])
        return data


# Light End



# Display Start


class DisplayPixel(Enum):
    
    Black               = 0x00
    White               = 0x01



class DisplayFont(Enum):
    
    LiberationMono5x8   = 0x00
    LiberationMono10x16 = 0x01



class DisplayAlign(Enum):
    
    Left                = 0x00      # 수동 조작
    Center              = 0x01      
    Right               = 0x02      




class DisplayClearAll(ISerializable):

    def __init__(self):
        self.pixel       = DisplayPixel.White


    @classmethod
    def getSize(cls):
        return 1


    def toArray(self):
        return pack('<B', self.pixel.value)


    @classmethod
    def parse(cls, dataArray):
        data = DisplayClearAll()
        
        if len(dataArray) != cls.getSize():
            return None

        data.pixel = unpack('<B', dataArray)
        data.pixel = DisplayPixel(data.pixel)
        
        return data



class DisplayClear(ISerializable):

    def __init__(self):
        
        self.x           = 0
        self.y           = 0
        self.width       = 0
        self.height      = 0
        self.pixel       = DisplayPixel.White


    @classmethod
    def getSize(cls):
        return 9


    def toArray(self):
        return pack('<hhhhB', self.x, self.y, self.width, self.height, self.pixel.value)


    @classmethod
    def parse(cls, dataArray):
        data = DisplayClear()
        
        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.width, data.height, data.pixel = unpack('<hhhhB', dataArray)

        data.pixel = DisplayPixel(data.pixel);
        
        return data



class DisplayInvert(ISerializable):

    def __init__(self):
        
        self.x           = 0
        self.y           = 0
        self.width       = 0
        self.height      = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<hhhh', self.x, self.y, self.width, self.height)


    @classmethod
    def parse(cls, dataArray):
        data = DisplayInvert()
        
        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.width, data.height = unpack('<hhhh', dataArray)
        
        return data



class DisplayDrawPoint(ISerializable):

    def __init__(self):
        
        self.x           = 0
        self.y           = 0
        self.pixel       = DisplayPixel.White


    @classmethod
    def getSize(cls):
        return 5


    def toArray(self):
        return pack('<hhB', self.x, self.y, self.pixel.value)


    @classmethod
    def parse(cls, dataArray):
        data = DisplayDrawPoint()
        
        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.pixel = unpack('<hhB', dataArray)

        data.pixel = DisplayPixel(data.pixel);
        
        return data



class DisplayDrawRect(ISerializable):

    def __init__(self):
        
        self.x          = 0
        self.y          = 0
        self.width      = 0
        self.height     = 0
        self.pixel      = DisplayPixel.White
        self.flagFill   = True


    @classmethod
    def getSize(cls):
        return 10


    def toArray(self):
        return pack('<hhhhB?', self.x, self.y, self.width, self.height, self.pixel.value, self.flagFill)


    @classmethod
    def parse(cls, dataArray):
        data = DisplayDrawRect()
        
        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.width, data.height, data.pixel, data.flagFill = unpack('<hhhhB?', dataArray)

        data.pixel = DisplayPixel(data.pixel);
        
        return data



class DisplayDrawCircle(ISerializable):

    def __init__(self):
        
        self.x          = 0
        self.y          = 0
        self.radius     = 0
        self.pixel      = DisplayPixel.White
        self.flagFill   = True


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<hhhB?', self.x, self.y, self.radius, self.pixel.value, self.flagFill)


    @classmethod
    def parse(cls, dataArray):
        data = DisplayDrawCircle()
        
        if len(dataArray) != cls.getSize():
            return None

        data.x, data.y, data.radius, data.pixel, data.flagFill = unpack('<hhhB?', dataArray)

        data.pixel = DisplayPixel(data.pixel);
        
        return data



class DisplayDrawString(ISerializable):

    def __init__(self):
        
        self.x          = 0
        self.y          = 0
        self.font       = DisplayFont.LiberationMono5x8
        self.pixel      = DisplayPixel.White
        self.message    = ""


    @classmethod
    def getSize(cls):
        return 6

    def toArray(self):
        dataArray = []
        dataArray.extend(pack('<hhBB', self.x, self.y, self.font.value, self.pixel.value))
        dataArray.extend(self.message.encode('ascii', 'ignore'))
        return dataArray


    @classmethod
    def parse(cls, dataArray):
        data = DisplayDrawString()
        
        if len(dataArray) <= cls.getSize():
            return None

        data.x, data.y, data.font, data.pixel = unpack('<hhBB', dataArray[0:getSize()])
        data.font = DisplayFont(data.font);
        data.pixel = DisplayPixel(data.pixel);
        data.message = dataArray[getSize():len(dataArray)].decode()
        
        return data



class DisplayDrawStringAlign(ISerializable):

    def __init__(self):
        
        self.x_start    = 0
        self.x_end      = 0
        self.y          = 0
        self.align      = DisplayAlign.Center
        self.font       = DisplayFont.LiberationMono5x8
        self.pixel      = DisplayPixel.White
        self.message    = ""


    @classmethod
    def getSize(cls):
        return 9


    def toArray(self):
        dataArray = []
        dataArray.extend(pack('<hhhBBB', self.x_start, self.x_end, self.y, self.align.value, self.font.value, self.pixel.value))
        dataArray.extend(self.message.encode('ascii', 'ignore'))
        return dataArray
    

    @classmethod
    def parse(cls, dataArray):
        data = DisplayDrawStringAlign()
        
        if len(dataArray) <= cls.getSize():
            return None

        data.x_start, data.x_end, data.y, data.align, data.font, data.pixel, data.message = unpack('<hhhBBBs', dataArray[0:getSize()])
        data.align = DisplayAlign(data.align);
        data.font = DisplayFont(data.font);
        data.pixel = DisplayPixel(data.pixel);
        data.message = dataArray[getSize():len(dataArray)].decode()
        
        return data


# Display End



# Buzzer Start


class BuzzerMode(Enum):

    Stop                = 0     # 정지(Mode에서의 Stop은 통신에서 받았을 때 Buzzer를 끄는 용도로 사용, set으로만 호출)

    Mute                = 1     # 묵음 즉시 적용
    MuteReserve         = 2     # 묵음 예약

    Scale               = 3     # 음계 즉시 적용
    ScaleReserve        = 4     # 음계 예약

    Hz                  = 5     # 주파수 즉시 적용
    HzReserve           = 6     # 주파수 예약

    EndOfType           = 7



class BuzzerScale(Enum):

    C1 = 0x00; CS1 = 0x01; D1 = 0x02; DS1 = 0x03; E1 = 0x04; F1 = 0x05; FS1 = 0x06; G1 = 0x07; GS1 = 0x08; A1 = 0x09; AS1 = 0x0A; B1 = 0x0B;
    C2 = 0x0C; CS2 = 0x0D; D2 = 0x0E; DS2 = 0x0F; E2 = 0x10; F2 = 0x11; FS2 = 0x12; G2 = 0x13; GS2 = 0x14; A2 = 0x15; AS2 = 0x16; B2 = 0x17;
    C3 = 0x18; CS3 = 0x19; D3 = 0x1A; DS3 = 0x1B; E3 = 0x1C; F3 = 0x1D; FS3 = 0x1E; G3 = 0x1F; GS3 = 0x20; A3 = 0x21; AS3 = 0x22; B3 = 0x23;
    C4 = 0x24; CS4 = 0x25; D4 = 0x26; DS4 = 0x27; E4 = 0x28; F4 = 0x29; FS4 = 0x2A; G4 = 0x2B; GS4 = 0x2C; A4 = 0x2D; AS4 = 0x2E; B4 = 0x2F;

    C5 = 0x30; CS5 = 0x31; D5 = 0x32; DS5 = 0x33; E5 = 0x34; F5 = 0x35; FS5 = 0x36; G5 = 0x37; GS5 = 0x38; A5 = 0x39; AS5 = 0x3A; B5 = 0x3B;
    C6 = 0x3C; CS6 = 0x3D; D6 = 0x3E; DS6 = 0x3F; E6 = 0x40; F6 = 0x41; FS6 = 0x42; G6 = 0x43; GS6 = 0x44; A6 = 0x45; AS6 = 0x46; B6 = 0x47;
    C7 = 0x48; CS7 = 0x49; D7 = 0x4A; DS7 = 0x4B; E7 = 0x4C; F7 = 0x4D; FS7 = 0x4E; G7 = 0x4F; GS7 = 0x50; A7 = 0x51; AS7 = 0x52; B7 = 0x53;
    C8 = 0x54; CS8 = 0x55; D8 = 0x56; DS8 = 0x57; E8 = 0x58; F8 = 0x59; FS8 = 0x5A; G8 = 0x5B; GS8 = 0x5C; A8 = 0x5D; AS8 = 0x5E; B8 = 0x5F;

    EndOfType   = 0x60

    Mute        = 0xEE  # 묵음
    Fin         = 0xFF  # 악보의 끝



class Buzzer(ISerializable):

    def __init__(self):
        self.mode       = BuzzerMode.Stop
        self.value      = 0
        self.time       = 0


    @classmethod
    def getSize(cls):
        return 5


    def toArray(self):
        return pack('<BHH', self.mode.value, self.value, self.time)


    @classmethod
    def parse(cls, dataarray):
        data = Buzzer()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.mode, data.value, data.time = unpack('<BHH', dataarray)
        data.mode = BuzzerMode(data.mode)

        return data


# Buzzer End



# Vibrator Start


class VibratorMode(Enum):

    Stop                = 0     # 정지

    Instantally         = 1     # 즉시 적용
    Continually         = 2     # 예약

    EndOfType           = 3



class Vibrator(ISerializable):

    def __init__(self):
        self.mode       = VibratorMode.Stop
        self.on         = 0
        self.off        = 0
        self.total      = 0


    @classmethod
    def getSize(cls):
        return 7


    def toArray(self):
        return pack('<BHHH', self.mode.value, self.on, self.off, self.total)


    @classmethod
    def parse(cls, dataarray):
        data = Vibrator()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.mode, data.on, data.off, data.total = unpack('<BHHH', dataarray)
        data.mode = VibratorMode(data.mode)

        return data



# Vibrator End



# Joystick Start


class JoystickDirection(Enum):

    None_   = 0         # 정의하지 않은 영역(무시함)

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

    None_       = 0     # 이벤트 없음
    
    In          = 1     # 특정 영역에 진입
    Stay        = 2     # 특정 영역에서 상태 유지
    Out         = 3     # 특정 영역에서 벗어남
    
    EndOfType   = 4



class JoystickBlock(ISerializable):

    def __init__(self):
        self.x          = 0
        self.y          = 0
        self.direction  = JoystickDirection.None_
        self.event      = JoystickEvent.None_


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<BBBB', self.x, self.y, self.direction.value, self.event.value)


    @classmethod
    def parse(cls, dataarray):
        data = JoystickBlock()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.x, data.y, data.direction, data.event = unpack('<BBBB', dataarray)
        data.direction  = JoystickDirection(data.direction)
        data.event      = JoystickEvent(data.event)

        return data



class Joystick(ISerializable):

    def __init__(self):
        self.left       = JoystickBlock()
        self.right      = JoystickBlock()


    @classmethod
    def getSize(cls):
        return JoystickBlock().getSize() * 2


    def toArray(self):
        dataArray = []
        dataArray.extend(self.left.toArray())
        dataArray.extend(self.right.toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = Joystick()
        
        if len(dataarray) != cls.getSize():
            return None
        
        indexStart = 0;        indexEnd  = JoystickBlock.getSize();     data.left   = JoystickBlock.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += JoystickBlock.getSize();     data.right  = JoystickBlock.parse(dataarray[indexStart:indexEnd])

        return data


# Joystick End



# Button Start


class ButtonFlagController(Enum):

    None_           = 0x0000
    
    FrontLeft       = 0x0001
    FrontRight      = 0x0002
    
    MidTurnLeft     = 0x0004
    MidTurnRight    = 0x0008
    
    MidUp           = 0x0010
    MidLeft         = 0x0020
    MidRight        = 0x0040
    MidDown         = 0x0080
    
    RearLeft        = 0x0100
    RearRight       = 0x0200



class ButtonFlagDrone(Enum):

    None_           = 0x0000
    
    Reset           = 0x0001



class Button(ISerializable):

    def __init__(self):
        self.button     = 0
        self.event      = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<HB', self.button, self.event)


    @classmethod
    def parse(cls, dataarray):
        data = Button()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.button, data.event = unpack('<HB', dataarray)
        
        return data


# Button End



# Information Start


class State(ISerializable):

    def __init__(self):
        self.modeVehicle        = ModeVehicle.None_

        self.modeSystem         = ModeSystem.None_
        self.modeFlight         = ModeFlight.None_
        self.modeDrive          = ModeDrive.None_

        self.sensorOrientation  = SensorOrientation.None_
        self.headless           = Headless.None_
        self.battery            = 0


    @classmethod
    def getSize(cls):
        return 7


    def toArray(self):
        return pack('<BBBBBBB', self.modeVehicle.value, self.modeSystem.value, self.modeFlight.value, self.modeDrive.value, self.sensorOrientation.value, self.headless.value, self.battery)


    @classmethod
    def parse(cls, dataarray):
        data = Range()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.modeVehicle, data.modeSystem, data.modeFlight, data.modeDrive, data.sensorOrientation, data.headless, data.battery = unpack('<BBBBBBB', dataarray)
        
        return data



class CountFlight(ISerializable):

    def __init__(self):
        self.timeFlight     = 0

        self.countTakeOff   = 0
        self.countLanding   = 0
        self.countAccident  = 0


    @classmethod
    def getSize(cls):
        return 14


    def toArray(self):
        return pack('<QHHH', self.timeFlight, self.countTakeOff, self.countLanding, self.countAccident)


    @classmethod
    def parse(cls, dataarray):
        data = CountFlight()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.timeFlight, data.countTakeOff, data.countLanding, data.countAccident = unpack('<QHHH', dataarray)
        
        return data



class CountDrive(ISerializable):
    
    def __init__(self):
        self.timeDrive      = 0

        self.countAccident  = 0


    @classmethod
    def getSize(cls):
        return 10


    def toArray(self):
        return pack('<QH', self.timeDrive, self.countAccident)


    @classmethod
    def parse(cls, dataarray):
        data = CountDrive()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.timeDrive, data.countAccident = unpack('<QH', dataarray)
        
        return data


# Information End



# Sensor Start


class Vector(ISerializable):

    def __init__(self):
        self.x      = 0
        self.y      = 0
        self.z      = 0


    @classmethod
    def getSize(cls):
        return 6


    def toArray(self):
        return pack('<hhh', self.x, self.y, self.z)


    @classmethod
    def parse(cls, dataarray):
        data = Vector()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.x, data.y, data.z = unpack('<hhh', dataarray)
        
        return data



class Attitude(ISerializable):

    def __init__(self):
        self.roll       = 0
        self.pitch      = 0
        self.yaw        = 0


    @classmethod
    def getSize(cls):
        return 6


    def toArray(self):
        return pack('<hhh', self.roll, self.pitch, self.yaw)


    @classmethod
    def parse(cls, dataarray):
        data = Attitude()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.roll, data.pitch, data.yaw = unpack('<hhh', dataarray)
        
        return data



class IrMessage(ISerializable):

    def __init__(self):
        self.direction  = Direction.None_
        self.irData     = 0


    @classmethod
    def getSize(cls):
        return 5


    def toArray(self):
        return pack('<BI', self.direction.value, self.irData)


    @classmethod
    def parse(cls, dataarray):
        data = IrMessage()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.direction, data.irData = unpack('<BI', dataarray)
        data.direction = Direction(data.direction)
        
        return data



class Imu(ISerializable):

    def __init__(self):
        self.accelX     = 0
        self.accelY     = 0
        self.accelZ     = 0
        self.gyroRoll   = 0
        self.gyroPitch  = 0
        self.gyroYaw    = 0
        self.angleRoll  = 0
        self.anglePitch = 0
        self.angleYaw   = 0


    @classmethod
    def getSize(cls):
        return 18


    def toArray(self):
        return pack('<hhhhhhhhh', self.accelX, self.accelY, self.accelZ, self.gyroRoll, self.gyroPitch, self.gyroYaw, self.angleRoll, self.anglePitch, self.angleYaw)


    @classmethod
    def parse(cls, dataarray):
        data = Imu()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.accelX, data.accelY, data.accelZ, data.gyroRoll, data.gyroPitch, data.gyroYaw, data.angleRoll, data.anglePitch, data.angleYaw = unpack('<hhhhhhhhh', dataarray)
        
        return data



class Battery(ISerializable):

    def __init__(self):
        self.gradient                   = 0
        self.yIntercept                 = 0
        self.adjustGradient             = 0
        self.adjustYIntercept           = 0
        self.flagBatteryCalibration     = False
        self.batteryRaw                 = 0
        self.batteryPercent             = 0
        self.voltage                    = 0


    @classmethod
    def getSize(cls):
        return 27


    def toArray(self):
        return pack('<ffffBhff', self.gradient, self.yIntercept, self.adjustGradient, self.adjustYIntercept, self.flagBatteryCalibration, self.batteryRaw, self.batteryPercent, self.voltage)


    @classmethod
    def parse(cls, dataarray):
        data = Battery()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.gradient, data.yIntercept, data.adjustGradient, data.adjustYIntercept, data.flagBatteryCalibration, data.batteryRaw, data.batteryPercent, data.voltage = unpack('<ffffBhff', dataarray)
        data.flagBatteryCalibration = bool(data.flagBatteryCalibration)
        
        return data



class Pressure(ISerializable):

    def __init__(self):
        self.temperature    = 0
        self.pressure       = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<ff', self.temperature, self.pressure)


    @classmethod
    def parse(cls, dataarray):
        data = Pressure()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.temperature, data.pressure = unpack('<ff', dataarray)
        
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
    def getSize(cls):
        return 24


    def toArray(self):
        return pack('<ffffff', self.left, self.front, self.right, self.rear, self.top, self.bottom)


    @classmethod
    def parse(cls, dataarray):
        data = Range()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.left, data.front, data.right, data.rear, data.top, data.bottom = unpack('<ffffff', dataarray)
        
        return data



class ImageFlow(ISerializable):

    def __init__(self):
        self.positionX     = 0
        self.positionY     = 0


    @classmethod
    def getSize(cls):
        return 8


    def toArray(self):
        return pack('<ff', self.positionX, self.positionY)


    @classmethod
    def parse(cls, dataarray):
        data = ImageFlow()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.positionX, data.positionY = unpack('<ff', dataarray)
        
        return data



# Sensor End



# Device Start


class MotorBlock(ISerializable):

    def __init__(self):
        self.rotation   = Rotation.None_
        self.value      = 0


    @classmethod
    def getSize(cls):
        return 3


    def toArray(self):
        return pack('<Bh', self.rotation.value, self.value)


    @classmethod
    def parse(cls, dataarray):
        data = MotorBlock()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.rotation, data.value = unpack('<Bh', dataarray)
        data.rotation = Rotation(data.rotation)
        
        return data




class Motor(ISerializable):

    def __init__(self):
        self.motor      = []
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())
        self.motor.append(MotorBlock())


    @classmethod
    def getSize(cls):
        return MotorBlock.getSize() * 4


    def toArray(self):
        dataArray = []
        dataArray.extend(self.motor[0].toArray())
        dataArray.extend(self.motor[1].toArray())
        dataArray.extend(self.motor[2].toArray())
        dataArray.extend(self.motor[3].toArray())
        return dataArray


    @classmethod
    def parse(cls, dataarray):
        data = Motor()
        
        if len(dataarray) != cls.getSize():
            return None
        
        indexStart = 0;        indexEnd  = MotorBlock.getSize();    data.motor[0]   = MotorBlock.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += MotorBlock.getSize();    data.motor[1]   = MotorBlock.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += MotorBlock.getSize();    data.motor[2]   = MotorBlock.parse(dataarray[indexStart:indexEnd])
        indexStart = indexEnd; indexEnd += MotorBlock.getSize();    data.motor[3]   = MotorBlock.parse(dataarray[indexStart:indexEnd])
        return data



class MotorSingle(ISerializable):

    def __init__(self):
        self.target     = 0
        self.rotation   = Rotation.None_
        self.value      = 0


    @classmethod
    def getSize(cls):
        return 4


    def toArray(self):
        return pack('<BBh', self.target, self.rotation.value, self.value)


    @classmethod
    def parse(cls, dataarray):
        data = MotorBlock()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.target, data.rotation, data.value = unpack('<BBh', dataarray)
        data.rotation = Rotation(data.rotation)
        
        return data


# Device End

