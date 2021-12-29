from enum import Enum


class ModelNumber(Enum):

    NONE = 0x00000000

    #                    AAAABBCC, AAAA(Project Number), BB(Device Type), CC(Revision)
    DRONE_3_DRONE_P1 = 0x00031001       # Lightrone / GD65 / HW2181
    DRONE_3_DRONE_P2 = 0x00031002       # Soccer Drone / HW2181
    DRONE_3_DRONE_P3 = 0x00031003       # GD240 / HW2181
    DRONE_3_DRONE_P4 = 0x00031004       # GD50N / HW2181
    DRONE_3_DRONE_P5 = 0x00031005       # GD30 / HW2181
    DRONE_3_DRONE_P6 = 0x00031006       # Soccer Drone 2 / HW2181
    DRONE_3_DRONE_P7 = 0x00031007       # SKYKICKV2 / HW2181 
    DRONE_3_DRONE_P8 = 0x00031008       # GD65 / HW2181
    DRONE_3_DRONE_P9 = 0x00031009       # GD65 / HW2181
    DRONE_3_DRONE_P10 = 0x0003100A      # Battle Drone / SPI / HW2181

    DRONE_3_CONTROLLER_P1 = 0x00032001  # (obsolete)
    DRONE_3_CONTROLLER_P2 = 0x00032002  # HW2000
    DRONE_3_CONTROLLER_P3 = 0x00032003  # HW2000B
    DRONE_3_CONTROLLER_P4 = 0x00032004
    DRONE_3_CONTROLLER_P5 = 0x00032005

    DRONE_3_LINK_P0 = 0x00033000

    DRONE_3_ANALYZER_P0 = 0x00034100    # for soccer drone

    DRONE_3_TESTER_P4 = 0x0003A004      # (obsolete)
    DRONE_3_TESTER_P6 = 0x0003A006      # Battle Drone Tester

    DRONE_4_DRONE_P4 = 0x00041004       # (obsolete)
    DRONE_4_DRONE_P5 = 0x00041005       # HW2000, 2m range sensor
    DRONE_4_DRONE_P6 = 0x00041006       # HW2000B, 4m range sensor
    DRONE_4_DRONE_P7 = 0x00041007       # HW2000B, 4m range sensor, BLDC Motor

    DRONE_4_CONTROLLER_P1 = 0x00042001  # (obsolete)
    DRONE_4_CONTROLLER_P2 = 0x00042002  # HW2000
    DRONE_4_CONTROLLER_P3 = 0x00042003  # HW2000B
    DRONE_4_CONTROLLER_P4 = 0x00042004  # HW2000B + PA
    DRONE_4_CONTROLLER_P5 = 0x00042005  # HW2000B + PA

    DRONE_4_LINK_P0 = 0x00043000

    DRONE_4_TESTER_P4 = 0x0004A004      # (obsolete)
    DRONE_4_TESTER_P6 = 0x0004A006
    DRONE_4_TESTER_P7 = 0x0004A007

    DRONE_4_MONITOR_P4 = 0x0004A104     # (obsolete)

    DRONE_7_DRONE_P1 = 0x00071001       # (obsolete)
    DRONE_7_DRONE_P2 = 0x00071002       # Coding Car

    DRONE_7_BLE_CLIENT_P0 = 0x00073200  # Coding Car Link
    DRONE_7_BLE_CLIENT_P5 = 0x00073205  # Coding Car Tester BLE

    DRONE_7_BLE_SERVER_P2 = 0x00073302  # Coding Car Ble Module

    DRONE_7_TESTER_P4 = 0x0003A004      # (obsolete)
    DRONE_7_TESTER_P5 = 0x0003A005      # (obsolete)
    DRONE_7_TESTER_P6 = 0x0003A006

    DRONE_7_MONITOR_P4 = 0x0003A104     # (obsolete)
    DRONE_7_MONITOR_P5 = 0x0003A105

    DRONE_8_DRONE_P0 = 0x00081000       # (obsolete)
    DRONE_8_DRONE_P1 = 0x00081001       # Coding Drone

    DRONE_8_TESTER_P4 = 0x0008A004      # (obsolete)
    DRONE_8_TESTER_P6 = 0x0008A006

    DRONE_8_MONITOR_P6 = 0x0008A106

    DRONE_9_DRONE_P0 = 0x00091000
    DRONE_9_DRONE_P1 = 0x00091001
    DRONE_9_DRONE_P2 = 0x00091002
    DRONE_9_DRONE_P3 = 0x00091003
    DRONE_9_DRONE_P4 = 0x00091004
    DRONE_9_DRONE_P5 = 0x00091005
    DRONE_9_DRONE_P6 = 0x00091006

    DRONE_9_TESTER_P6 = 0x0009A006
    DRONE_9_TESTER_P7 = 0x0009A007


class DeviceType(Enum):

    NONE = 0x00

    DRONE = 0x10        # 드론(Server)

    CONTROLLER = 0x20   # 조종기(Client)

    LINK = 0x30         # 링크 모듈(Client)
    LINK_SERVER = 0x31  # 링크 모듈(Server, 링크 모듈이 서버로 동작하는 경우에만 통신 타입을 잠시 바꿈)
    BLE_CLIENT = 0x32   # BLE 클라이언트
    BLE_SERVER = 0x33   # BLE 서버

    RANGE = 0x40        # 거리 센서 모듈
    ANALYZER = 0x41     # 분석 모듈

    BASE = 0x70         # 베이스

    BYSCRATCH = 0x80    # 바이스크래치
    SCRATCH = 0x81      # 스크래치
    ENTRY = 0x82        # 네이버 엔트리

    TESTER = 0xA0       # 테스터
    MONITOR = 0xA1      # 모니터
    UPDATER = 0xA2      # 펌웨어 업데이트 도구
    ENCRYPTER = 0xA3    # 암호화 도구

    # 바로 인접한 장치까지만 전달(받은 장치는 자기 자신에게 보낸 것처럼 처리하고 타 장치에 전달하지 않음)
    WHISPERING = 0xFE
    BROADCASTING = 0xFF


class ModeSystem(Enum):

    NONE = 0x00

    BOOT = 0x10
    START = 0x11
    RUNNING = 0x12
    READY_TO_RESET = 0x13

    ERROR = 0xA0

    END_OF_TYPE = 0xA1


class ModeControlFlight(Enum):

    NONE = 0x00

    ATTITUDE = 0x10     # 자세 - X, Y는 각도(deg)로 입력받음, Z, Yaw는 속도(m/s)로 입력 받음
    POSITION = 0x11     # 위치 - X, Y, Z, Yaw는 속도(m/s)로 입력 받음
    MANUAL = 0x12       # 고도를 수동으로 조종함
    RATE = 0x13         # Rate - X, Y는 각속도(deg/s)로 입력받음, Z, Yaw는 속도(m/s)로 입력 받음
    FUNCTION = 0x14     # 기능

    END_OF_TYPE = 0x15


class ModeFlight(Enum):

    NONE = 0x00

    READY = 0x10

    START = 0x11
    TAKEOFF = 0x12
    FLIGHT = 0x13
    LANDING = 0x14
    FLIP = 0x15
    REVERSE = 0x16

    STOP = 0x20

    ACCIDENT = 0x30
    ERROR = 0x31

    TEST = 0x40

    END_OF_TYPE = 0x41


class ModeUpdate(Enum):

    NONE = 0x00

    READY = 0x01            # 업데이트 가능 상태
    UPDATE = 0x02           # 업데이트 중
    COMPLETE = 0x03         # 업데이트 완료

    FAILED = 0x04           # 업데이트 실패(업데이트 완료까지 갔으나 body의 Crc16이 일치하지 않는 경우 등)

    NOT_AVAILABLE = 0x05    # 업데이트 불가능 상태(Debug 모드 등)
    RUN_APPLICATION = 0x06  # 어플리케이션 동작 중
    NOT_REGISTERED = 0x07   # 등록되지 않음

    END_OF_TYPE = 0x08


class ErrorFlagsForSensor(Enum):

    NONE = 0x00000000

    MOTION_NO_ANSWER = 0x00000001           # Motion 센서 응답 없음
    MOTION_WRONG_VALUE = 0x00000002         # Motion 센서 잘못된 값
    MOTION_NOT_CALIBRATED = 0x00000004      # Gyro Bias 보정이 완료되지 않음
    MOTION_CALIBRATING = 0x00000008         # Gyro Bias 보정 중

    PRESSURE_NO_ANSWER = 0x00000010         # 압력 센서 응답 없음
    PRESSURE_WRONG_VALUE = 0x00000020       # 압력 센서 잘못된 값

    RANGE_GROUND_NO_ANSWER = 0x00000100     # 바닥 거리 센서 응답 없음
    RANGE_GROUND_WRONG_VALUE = 0x00000200   # 바닥 거리 센서 잘못된 값
    RANGE_FRONT_NO_ANSWER = 0x00000400 	    # 정면 거리 센서 응답 없음
    RANGE_FRONT_WRONG_VALUE = 0x00000800    # 정면 거리 센서 잘못된 값

    FLOW_NO_ANSWER = 0x00001000             # Flow 센서 응답 없음
    FLOW_WRONG_VALUE = 0x00002000           # Flow 잘못된 값
    FLOW_CANNOT_RECOGNIZE_GROUND_IMAGE = 0x00004000     # 바닥 이미지를 인식할 수 없음

    RF_NO_ANSWER = 0x10000000               # RF 응답 없음
    RF_PAIRED = 0x20000000                  # RF 페어링 완료
    RF_CONNECTED = 0x40000000               # RF 연결됨


class ErrorFlagsForState(Enum):

    NONE = 0x00000000

    NOT_REGISTERED = 0x00000001                     # 장치 등록이 안됨
    FLASH_READ_LOCK_UNLOCKED = 0x00000002           # 플래시 메모리 읽기 Lock이 안 걸림
    BOOTLOADER_WRITE_LOCK_UNLOCKED = 0x00000004     # 부트로더 영역 쓰기 Lock이 안 걸림
    LOW_BATTERY = 0x00000008                        # Low Battery

    TAKEOFF_FAILURE_CHECK_PROPELLER_AND_MOTOR = 0x00000010  # 이륙 실패
    CHECK_PROPELLER_VIBRATION = 0x00000020          # 프로펠러 진동발생
    ATTITUDE_NOT_STABLE = 0x00000040                # 자세가 많이 기울어져 있거나 뒤집어져 있을때

    CANNOT_FLIP_LOW_BATTERY = 0x00000100            # 배터리가 30이하
    CANNOT_FLIP_TOO_HEAVY = 0x00000200              # 기체가 무거움


class FlightEvent(Enum):

    NONE = 0x00

    STOP = 0x10
    TAKEOFF = 0x11
    LANDING = 0x12

    REVERSE = 0x13

    FLIP_FRONT = 0x14
    FLIP_REAR = 0x15
    FLIP_LEFT = 0x16
    FLIP_RIGHT = 0x17

    RETURN_HOME = 0x18

    SHOT = 0x90
    UNDER_ATTACK = 0x91

    RESET_HEADING = 0xA0

    END_OF_TYPE = 0xA1


class Direction(Enum):

    NONE = 0x00

    LEFT = 0x01
    FRONT = 0x02
    RIGHT = 0x03
    REAR = 0x04

    TOP = 0x05
    BOTTOM = 0x06

    CENTER = 0x07

    END_OF_TYPE = 0x08


class Rotation(Enum):

    NONE = 0x00

    CLOCKWISE = 0x01
    COUNTERCLOCKWISE = 0x02

    END_OF_TYPE = 0x03


class SensorOrientation(Enum):

    NONE = 0x00

    NORMAL = 0x01
    REVERSE_START = 0x02
    REVERSED = 0x03

    END_OF_TYPE = 0x04


class Headless(Enum):

    NONE = 0x00

    HEADLESS = 0x01      # Headless
    NORMAL = 0x02      # Normal

    END_OF_TYPE = 0x03


class TrimDirection(Enum):

    NONE = 0x00  # 없음

    ROLL_INCREASE = 0x01  # ROLL 증가
    ROLL_DECREASE = 0x02  # ROLL 감소
    PITCH_INCREASE = 0x03  # PITCH 증가
    PITCH_DECREASE = 0x04  # PITCH 감소
    YAW_INCREASE = 0x05  # YAW 증가
    YAW_DECREASE = 0x06  # YAW 감소
    THROTTLE_INCREASE = 0x07  # THROTTLE 증가
    THROTTLE_DECREASE = 0x08  # THROTTLE 감소

    RESET = 0x09  # 전체 트림 리셋

    END_OF_TYPE = 0x0A


class ModeMovement(Enum):

    NONE = 0x00

    READY = 0x01      # Ready
    HOVERING = 0x02      # Hovering
    MOVING = 0x03      # Moving
    RETURN_HOME = 0x04      # Return Home

    END_OF_TYPE = 0x05


class CardColorIndex(Enum):

    UNKNOWN = 0x00

    WHITE = 0x01
    RED = 0x02
    YELLOW = 0x03
    GREEN = 0x04
    CYAN = 0x05
    BLUE = 0x06
    MAGENTA = 0x07
    BLACK = 0x08

    END_OF_TYPE = 0x09


class Card(Enum):

    NONE = 0x00

    WHITE_WHITE = 0x11
    WHITE_RED = 0x12
    WHITE_YELLOW = 0x13
    WHITE_GREEN = 0x14
    WHITE_CYAN = 0x15
    WHITE_BLUE = 0x16
    WHITE_MAGENTA = 0x17
    WHITE_BLACK = 0x18

    RED_WHITE = 0x21
    RED_RED = 0x22
    RED_YELLOW = 0x23
    RED_GREEN = 0x24
    RED_CYAN = 0x25
    RED_BLUE = 0x26
    RED_MAGENTA = 0x27
    RED_BLACK = 0x28

    YELLOW_WHITE = 0x31
    YELLOW_RED = 0x32
    YELLOW_YELLOW = 0x33
    YELLOW_GREEN = 0x34
    YELLOW_CYAN = 0x35
    YELLOW_BLUE = 0x36
    YELLOW_MAGENTA = 0x37
    YELLOW_BLACK = 0x38

    GREEN_WHITE = 0x41
    GREEN_RED = 0x42
    GREEN_YELLOW = 0x43
    GREEN_GREEN = 0x44
    GREEN_CYAN = 0x45
    GREEN_BLUE = 0x46
    GREEN_MAGENTA = 0x47
    GREEN_BLACK = 0x48

    CYAN_WHITE = 0x51
    CYAN_RED = 0x52
    CYAN_YELLOW = 0x53
    CYAN_GREEN = 0x54
    CYAN_CYAN = 0x55
    CYAN_BLUE = 0x56
    CYAN_MAGENTA = 0x57
    CYAN_BLACK = 0x58

    BLUE_WHITE = 0x61
    BLUE_RED = 0x62
    BLUE_YELLOW = 0x63
    BLUE_GREEN = 0x64
    BLUE_CYAN = 0x65
    BLUE_BLUE = 0x66
    BLUE_MAGENTA = 0x67
    BLUE_BLACK = 0x68

    MAGENTA_WHITE = 0x71
    MAGENTA_RED = 0x72
    MAGENTA_YELLOW = 0x73
    MAGENTA_GREEN = 0x74
    MAGENTA_CYAN = 0x75
    MAGENTA_BLUE = 0x76
    MAGENTA_MAGENTA = 0x77
    MAGENTA_BLACK = 0x78

    BLACK_WHITE = 0x81
    BLACK_RED = 0x82
    BLACK_YELLOW = 0x83
    BLACK_GREEN = 0x84
    BLACK_CYAN = 0x85
    BLACK_BLUE = 0x86
    BLACK_MAGENTA = 0x87
    BLACK_BLACK = 0x88
