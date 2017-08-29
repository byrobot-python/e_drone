from enum import Enum


class DeviceType(Enum):
    
    None_               = 0x00

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
    
    None_               = 0x00

    Left                = 0x01
    Front               = 0x02
    Right               = 0x03
    Rear                = 0x04

    Top                 = 0x05
    Bottom              = 0x06

    EndOfType           = 0x07



class Rotation(Enum):
    
    None_               = 0x00

    Clockwise           = 0x01
    Counterclockwise    = 0x02

    EndOfType           = 0x03



class ModeSystem(Enum):
    
    None_               = 0x00

    Boot                = 0x01
    Start               = 0x02
    Running             = 0x03
    ReadyToReset        = 0x04
    Error               = 0x05

    EndOfType           = 0x07



class ModeVehicle(Enum):
    
    None_               = 0x00

    FlightGuard         = 0x10
    FlightNoGuard       = 0x11
    FlightFPV           = 0x12

    Drive               = 0x20
    DriveFPV            = 0x21

    Test                = 0x30

    EndOfType           = 0x31



class ModeFlight(Enum):
    
    None_               = 0x00

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
    
    None_               = 0x00

    Ready               = 0x10
    Start               = 0x11
    Drive               = 0x12

    Stop                = 0x20

    Accident            = 0x30
    Error               = 0x31

    Test                = 0x40

    EndOfType           = 0x41



class ModeUpdate(Enum):
    
    None_               = 0x00

    Ready               = 0x01      # 업데이트 가능 상태
    Update              = 0x02      # 업데이트 중
    Complete            = 0x03      # 업데이트 완료

    Faild               = 0x04      # 업데이트 실패(업데이트 완료까지 갔으나 body의 CRC16이 일치하지 않는 경우 등)

    NotAvailable        = 0x05      # 업데이트 불가능 상태(Debug 모드 등)
    RunApplication      = 0x06      # 어플리케이션 동작 중

    EndOfType           = 0x07



class DevelopmentStage(Enum):
    
    Alpha               = 0x00
    Beta                = 0x01 
    ReleaseCandidate    = 0x02
    Release             = 0x03



class FlightEvent(Enum):
    
    None_               = 0x00

    Stop                = 0x10
    TakeOff             = 0x11
    Landing             = 0x12

    Reverse             = 0x13

    Shot                = 0x18
    UnderAttack         = 0x19

    ResetHeading        = 0x1A

    EndOfType           = 0x1B



class DriveEvent(Enum):
    
    None_               = 0x00

    Stop                = 0x10
    
    Shot                = 0x11
    UnderAttack         = 0x12

    EndOfType           = 0x13



class SensorOrientation(Enum):
    
    None_               = 0x00

    Normal              = 0x01
    ReverseStart        = 0x02
    Reversed            = 0x03

    EndOfType           = 0x04



class Headless(Enum):
    
    None_               = 0x00

    Headless            = 0x01      # Headless
    Normal              = 0x02      # Normal

    EndOfType           = 0x04



