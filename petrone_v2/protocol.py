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
    Reserved_2          = 0x07      # 예약
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
    Attitude        = 0x41      # 드론의 자세(Angle)(Vector)
    GyroBias        = 0x42      # 자이로 바이어스 값(Vector)
    TrimAll         = 0x43      # 전체 트림
    TrimFlight      = 0x44      # 비행 트림
    TrimDrive       = 0x45      # 주행 트림

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
    Coordinate          = 0x20      # 방위 기준 변경
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


class Command(ISerializable):

    def __init__(self):
        self.commandType    = CommandType.None_
        self.option         = 0


    @classmethod
    def getSize(cls):
        return 2


    def toArray(self):
        return pack('<BB', self.commandType, self.option)


    @classmethod
    def parse(cls, dataarray):
        data = Command()
        
        if len(dataarray) != cls.getSize():
            return None
        
        data.commandType, data.option = unpack('<BB', dataarray)
        return data


# Common End


# Light Start


class LightDroneMode(Enum):
    
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



class LightDroneFlags(Enum):
    
    None_               = 0x00

    EyeRed              = 0x80
    EyeGreen            = 0x40
    EyeBlue             = 0x20

    ArmRed              = 0x10
    ArmGreen            = 0x08
    ArmBlue             = 0x04



class LightControllerMode(Enum):
    
    None_               = 0x00

    TeamNone            = 0x10
    TeamManual          = 0x11      # 수동 조작
    TeamHold            = 0x12      
    TeamFlicker         = 0x13      
    TeamFlickerDouble   = 0x14      
    TeamDimming         = 0x15      

    EndOfType           = 0x16      



class LightControllerFlags(Enum):
    
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
    
    EndOfColor             = 141



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
        indexStart = indexEnd; indexEnd += Color.getSize();         data.command    = Color.parse(dataarray[indexStart:indexEnd])
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
        indexStart = indexEnd; indexEnd += Color.getSize();         data.command    = Color.parse(dataarray[indexStart:indexEnd])
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

