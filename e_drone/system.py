from enum import Enum


class ModelNumber(Enum):
    
    None_                   = 0x00000000

    Drone_3_Drone_P1        = 0x00031001    # Drone_3_Drone_P1 (Lightrone / GD65 / HW2181 / Keil / 3.7v / barometer / RGB LED / Shaking binding)
    Drone_3_Drone_P2        = 0x00031002    # Drone_3_Drone_P2 (Soccer Drone / HW2181 / Keil / 7.4v / barometer / RGB LED / Shaking binding)
    Drone_3_Drone_P3        = 0x00031003    # Drone_3_Drone_P3 (GD240 / HW2181 / Keil / power button / u30 flow / 3.7v / geared motor / barometer)
    Drone_3_Drone_P4        = 0x00031004    # Drone_3_Drone_P4 (GD50N / HW2181 / Keil / power button / 3.7v / barometer)
    Drone_3_Drone_P5        = 0x00031005    # Drone_3_Drone_P5 (GD30 / HW2181 / Keil / 3.7v / nomal binding)

    Drone_3_Controller_P1   = 0x00032001    # Drone_3_Controller_P1

    Drone_4_Drone_P4        = 0x00041004    # Drone_4_Drone_P4
    Drone_4_Drone_P5        = 0x00041005    # Drone_4_Drone_P5

    Drone_4_Controlle_P1    = 0x00042001    # Drone_4_Controlle_P1
    Drone_4_Controlle_P2    = 0x00042002    # Drone_4_Controlle_P2

    Drone_4_Link_P0         = 0x00043000    # Drone_4_Link_P0

    Drone_4_Tester_P2       = 0x0004A002    # Drone_4_Tester_P2
    Drone_4_Monitor_P2      = 0x0004A102    # Drone_4_Monitor_P2



class DeviceType(Enum):

    None_       = 0x00

    Drone       = 0x10      # 드론(Server)

    Controller  = 0x20      # 조종기(Client)

    Link        = 0x30      # 링크 모듈(Client)
    LinkServer  = 0x31      # 링크 모듈(Server, 링크 모듈이 서버로 동작하는 경우에만 통신 타입을 잠시 바꿈)

    Range       = 0x40      # 거리 센서 모듈

    Base        = 0x70      # 베이스

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

    EndOfType           = 0x06



class ModeControlFlight(Enum):
    
    None_               = 0x00

    Attitude            = 0x10      # 자세 - X,Y는 각도(deg)로 입력받음, Z,Yaw는 속도(m/s)로 입력 받음
    Position            = 0x11      # 위치 - X,Y,Z,Yaw는 속도(m/s)로 입력 받음
    Function            = 0x12      # 기능 - X,Y,Z,Yaw는 속도(m/s)로 입력 받음
    Rate                = 0x13      # Rate - X,Y는 각속도(deg/s)로 입력받음, Z,Yaw는 속도(m/s)로 입력 받음
    
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

    Failed              = 0x04      # 업데이트 실패(업데이트 완료까지 갔으나 body의 CRC16이 일치하지 않는 경우 등)

    NotAvailable        = 0x05      # 업데이트 불가능 상태(Debug 모드 등)
    RunApplication      = 0x06      # 어플리케이션 동작 중
    NotRegistered       = 0x07      # 등록되지 않음

    EndOfType           = 0x08



class ErrorFlagsForSensor(Enum):

    None_                                   = 0x00000000

    Motion_NoAnswer                         = 0x00000001    # Motion 센서 응답 없음
    Motion_WrongValue                       = 0x00000002    # Motion 센서 잘못된 값
    Motion_NotCalibrated                    = 0x00000004    # Gyro Bias 보정이 완료되지 않음
    Motion_Calibrating                      = 0x00000008    # Gyro Bias 보정 중

    Pressure_NoAnswer                       = 0x00000010    # 압력 센서 응답 없음
    Pressure_WrongValue                     = 0x00000020    # 압력 센서 잘못된 값

    RangeGround_NoAnswer                    = 0x00000100    # 바닥 거리 센서 응답 없음
    RangeGround_WrongValue                  = 0x00000200    # 바닥 거리 센서 잘못된 값

    Flow_NoAnswer                           = 0x00001000    # Flow 센서 응답 없음
    Flow_WrongValue                         = 0x00002000    # Flow 잘못된 값
    Flow_CannotRecognizeGroundImage         = 0x00004000    # 바닥 이미지를 인식할 수 없음



class ErrorFlagsForState(Enum):

    None_                                   = 0x00000000

    NotRegistered                           = 0x00000001    # 장치 등록이 안됨
    FlashReadLock_UnLocked                  = 0x00000002    # 플래시 메모리 읽기 Lock이 안 걸림
    BootloaderWriteLock_UnLocked            = 0x00000004    # 부트로더 영역 쓰기 Lock이 안 걸림
    
    TakeoffFailure_CheckPropellerAndMotor   = 0x00000010    # 이륙 실패
    CheckPropellerVibration                 = 0x00000020    # 프로펠러 진동발생
    Attitude_NotStable                      = 0x00000040    # 자세가 많이 기울어져 있거나 뒤집어져 있을때
    
    CanNotFlip_LowBattery                   = 0x00000100    # 배터리가 30이하
    CanNotFlip_TooHeavy                     = 0x00000200    # 기체가 무거움



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

    Return              = 0x18

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

    EndOfType           = 0x03



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

    Ready               = 0x01      # Ready
    Hovering            = 0x02      # Hovering
    Moving              = 0x03      # Moving
    ReturnHome          = 0x04      # Return Home

    EndOfType           = 0x05



