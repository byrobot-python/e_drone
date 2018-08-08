from enum import Enum


class ModelNumber(Enum):

    None_                   = 0x00000000

    Drone_4_Drone_P3        = 0x00041003    # Drone_4_Drone_P3
    Drone_4_Controlle_P1    = 0x00042001    # Drone_4_Controlle_P1
    Drone_4_Link_P0         = 0x00043000    # Drone_4_Link_P0



class DeviceType(Enum):

    None_       = 0x00

    Drone       = 0x10      # 드론(Server)

    Controller  = 0x20      # 조종기(Client)

    Link        = 0x30      # 링크 모듈(Client)
    LinkServer  = 0x31      # 링크 모듈(Server, 링크 모듈이 서버로 동작하는 경우에만 통신 타입을 잠시 바꿈)

    ByScratch   = 0x80      # 바이스크래치
    Scratch     = 0x81      # 스크래치
    Entry       = 0x82      # 네이버 엔트리

    Tester      = 0xA0      # 테스터
    Monitor     = 0xA1      # 모니터
    Updater     = 0xA2      # 펌웨어 업데이트 도구
    Encrypter   = 0xA3      # 암호화 도구

    Broadcasting = 0xFF



class ModeSystem(Enum):
    
    None_               = 0x00

    Boot                = 0x01
    Start               = 0x02
    Running             = 0x03
    ReadyToReset        = 0x04
    Error               = 0x05

    EndOfType           = 0x07



class ModeControlFlight(Enum):
    
    None_               = 0x00

    Attitude            = 0x10      # 자세 - X,Y는 각도(deg)로 입력받음, Z,Yaw는 속도(m/s)로 입력 받음
    Position            = 0x11      # 위치 - X,Y,Z,Yaw는 속도(m/s)로 입력 받음
    Function            = 0x12      # 기능 - X,Y,Z,Yaw는 속도(m/s)로 입력 받음
    Rate                = 0x13      # Rate - X,Y는 각속도(deg/s)로 입력받음, Z,Yaw는 속도(m/s)로 입력 받음e
    
    EndOfType           = 0x14



class ModeFlight(Enum):
    
    None_               = 0x00

    Ready               = 0x10

    Start               = 0x11
    TakeOff             = 0x12
    Flight              = 0x13
    Landing             = 0x14
    Flip                = 0x15
    Reverse             = 0x16

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



class ErrorFlagsForSensor(Enum):

    None_                       = 0x00000000

    Motion_NoAnswer             = 0x00000001    # Motion 센서 응답 없음
    Motion_WrongValue           = 0x00000002
    Motion_NotCalibrated        = 0x00000004    # Bias 보정이 완료되지 않음
    Motion_Calibrating          = 0x00000008    # Bias 보정 중

    Pressure_NoAnswer           = 0x00000010    # 압력센서 응답 없음
    Pressure_WrongValue         = 0x00000020

    Range_NoAnswer              = 0x00000100    # 바닥 거리센서 응답 없음
    Range_WrongValue            = 0x00000200

    Flow_NoAnswer               = 0x00001000    # Flow 센서 응답 없음
    Flow_WrongValue             = 0x00002000

    Battery_NoAnswer            = 0x00010000    # 배터리 응답 없음
    Battery_WrongValue          = 0x00020000



class ErrorFlagsForState(Enum):

    None_                       = 0x00000000

    NotTested                   = 0x00000001    # 테스트하지 않음



class FlightEvent(Enum):
    
    None_               = 0x00

    Stop                = 0x10
    TakeOff             = 0x11
    Landing             = 0x12

    Reverse             = 0x13

    FlipFront           = 0x14
    FlipRear            = 0x15
    FlipLeft            = 0x16
    FlipRight           = 0x17

    ResetHeading        = 0xA0

    EndOfType           = 0xA1



class Direction(Enum):
    
    None_               = 0x00

    Left                = 0x01
    Front               = 0x02
    Right               = 0x03
    Rear                = 0x04

    Top                 = 0x05
    Bottom              = 0x06

    Center              = 0x07

    EndOfType           = 0x08



class Rotation(Enum):
    
    None_               = 0x00

    Clockwise           = 0x01
    Counterclockwise    = 0x02

    EndOfType           = 0x03



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



class TrimIncDec(Enum):
    
    None_               = 0x00  # 없음

    RollIncrease        = 0x01  # Roll 증가
    RollDecrease        = 0x02  # Roll 감소
    PitchIncrease       = 0x03  # Pitch 증가
    PitchDecrease       = 0x04  # Pitch 감소
    YawIncrease         = 0x05  # Yaw 증가
    YawDecrease         = 0x06  # Yaw 감소
    ThrottleIncrease    = 0x07  # Throttle 증가
    ThrottleDecrease    = 0x08  # Throttle 감소

    Reset               = 0x09  # 전체 트림 리셋

    EndOfType           = 0x0A



class ModeMovement(Enum):
    
    None_               = 0x00

    Hovering            = 0x01      # Hovering
    Moving              = 0x02      # Moving

    EndOfType           = 0x04



