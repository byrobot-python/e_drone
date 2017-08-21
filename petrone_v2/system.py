from enum import Enum


class DeviceType(Enum):
    
    None_               = 0x00      # 없음

    Drone               = 0x30      # 드론
    Controller          = 0x31      # 조종기
    Link                = 0x32      # 링크 모듈
    Tester              = 0x33      # 테스터
    Monitor             = 0x34      # 모니터
    Updater             = 0x35      # 펌웨어 업데이트 도구
    Encrypter           = 0x36      # 암호화 도구
    Scratch             = 0x37      # 스크래치
    Entry               = 0x38      # 네이버 엔트리
    ByScratch           = 0x39      # 바이스크래치

    EndOfType           = 0x40

    Broadcasting        = 0xFF



class Direction(Enum):
    
    None_               = 0x00      # 없음

    Left                = 0x01
    Front               = 0x02
    Right               = 0x03
    Rear                = 0x04

    Top                 = 0x05
    Bottom              = 0x06

    EndOfType           = 0x07



class ModeSystem(Enum):
    
    None_               = 0x00      # 없음

    Boot                = 0x01
    Start               = 0x02
    Running             = 0x03
    ReadyToReset        = 0x04
    Error               = 0x05

    EndOfType           = 0x07



class ModeVehicle(Enum):
    
    None_               = 0x00      # 없음

    FlightGuard         = 0x10
    FlightNoGuard       = 0x11
    FlightFPV           = 0x12

    Drive               = 0x20
    DriveFPV            = 0x21

    Test                = 0x30

    EndOfType           = 0x31



class ModeFlight(Enum):
    
    None_               = 0x00      # 없음

    Ready               = 0x10
    TakeOff             = 0x11
    Flight              = 0x12
    Landing             = 0x13
    Flip                = 0x14
    Reverse             = 0x15

    Stop                = 0x20

    Accident            = 0x30
    Error               = 0x31

    Test                = 0x40

    EndOfType           = 0x41



class ModeDrive(Enum):
    
    None_               = 0x00      # 없음

    Ready               = 0x10
    Start               = 0x11
    Drive               = 0x12

    Stop                = 0x20

    Accident            = 0x30
    Error               = 0x31

    Test                = 0x40

    EndOfType           = 0x41



class Rotation(Enum):
    
    None_               = 0x00      # 없음

    Clockwise           = 0x01
    Counterclockwise    = 0x02

    EndOfType           = 0x03



class FlightEvent(Enum):
    
    None_               = 0x00      # 없음

    Stop                = 0x10
    TakeOff             = 0x11
    Landing             = 0x12

    Reverse             = 0x13

    Shot                = 0x18
    UnderAttack         = 0x19

    ResetHeading        = 0x1A

    EndOfType           = 0x1B



class DriveEvent(Enum):
    
    None_               = 0x00      # 없음

    Stop                = 0x10
    
    Shot                = 0x11
    UnderAttack         = 0x12

    EndOfType           = 0x13



class SensorOrientation(Enum):
    
    None_               = 0x00      # 없음

    Normal              = 0x01
    ReverseStart        = 0x02
    Reversed            = 0x03

    EndOfType           = 0x04



class Coordinate(Enum):
    
    None_               = 0x00      # 없음

    World               = 0x01      # 고정 좌표계(Headless)
    Local               = 0x02      # 상대 좌표계(Normal)

    EndOfType           = 0x04



