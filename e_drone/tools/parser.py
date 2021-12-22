import sys
from e_drone.drone import *
from e_drone.tools.update import Updater

import colorama
from colorama import Fore, Back, Style

# Parser Start


class Parser():

    def __init__(self):

        self.program_name   = None
        self.arguments      = None
        self.count          = 0


    def run(self):
        
        self.program_name   = sys.argv[0]
        self.arguments      = sys.argv[1:]
        self.count          = len(self.arguments)

        colorama.init()

        if (self.count > 0) and (self.arguments != None):

            print("Count:{0} ".format(self.count) , end = '')

            for arg in self.arguments:
                print("/ {0} ".format(arg), end = '')

            print("")

            # > python -m e_drone upgrade
            # > python -m e_drone update
            if      (self.arguments[0] == "upgrade") or (self.arguments[0] == "update"):
                updater = Updater()
                updater.update()
                return

            # > python -m e_drone request State 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "state")):         # time interval
                #print("* State - Ready     Blue    Red     Black   Black   NONE             1830   1631   2230      76      ")    
                print ("         |ModeSystem   |ModeFlight |ModeControlFlight |ModeMovement |Headless |ControlSpeed |SensorOrientation |Battery |")
                self.request(DeviceType.DRONE, DataType.STATE, int(self.arguments[2]), float(self.arguments[3]))
                return

            # > python -m e_drone request Motion 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "motion")):         # time interval
                #print("* Motion      -38      64     -32     457     -40    -400      16       0   20500")    
                print ("         |Accel                  |Gyro                   |Angle                  |")
                print ("         |      X|      Y|      Z|   Roll|  Pitch|    Yaw|   Roll|  Pitch|    Yaw|")
                self.request(DeviceType.DRONE, DataType.MOTION, int(self.arguments[2]), float(self.arguments[3]))
                return

            # > python -m e_drone request CardRaw 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "cardraw")):         # time interval
                #print("* CardRaw   335  503  766  692  309  395 100  39  96  40   9  17 303  61  39 344  77  15   Magenta         Red")
                print ("          |Front Raw     |Rear Raw      |Front RGB  |Rear RGB   |Front HSVL      |Rear HSVL       |Front Color  |Rear Color   |")
                print ("          |   R    G    B|   R    G    B|  R   G   B|  R   G   B|  H   S   V   L|  H   S   V   L|             |             |")
                self.request(DeviceType.DRONE, DataType.CARD_RAW, int(self.arguments[2]), float(self.arguments[3]))
                return

            # > python -m e_drone request CardRange 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "cardrange")):         # time interval
                #print("* CardRange       200  2000   200  2000   200  2000   200     0   200     0   200     0")
                print ("               |Front                              |Rear                               |")
                print ("               |Red        |Green      |Blue       |Red        |Green      |Blue       |")
                print ("               |  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|")
                self.request(DeviceType.DRONE, DataType.CARD_RANGE, int(self.arguments[2]), float(self.arguments[3]))
                return

            # 이륙
            #                   0
            # python -m e_drone Takeoff
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "takeoff")):
                print (Fore.YELLOW + "takeoff" + Style.RESET_ALL)
                self.command(CommandType.FLIGHT_EVENT, FlightEvent.TAKEOFF.value)
                return

            # 착륙
            #                   0
            # python -m e_drone Landing
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "landing")):
                print (Fore.YELLOW + "landing" + Style.RESET_ALL)
                self.command(CommandType.FLIGHT_EVENT, FlightEvent.LANDING.value)
                return

            # 정지
            #                   0
            # python -m e_drone Stop
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "stop")):
                print (Fore.YELLOW + "stop" + Style.RESET_ALL)
                self.command(CommandType.FLIGHT_EVENT, FlightEvent.STOP.value)
                return

            # 조종
            #                   0        1      2       3     4          5
            # python -m e_drone control [roll] [pitch] [yaw] [throttle] [time(ms)]
            # 지정한 시간이 종료되면 입력값을 모두 0으로 변경하고 멈춤
            # > python -m e_drone control 40 0 3
            elif    ((self.count == 6) and 
                    (self.arguments[0] == "control")):
                print (Fore.YELLOW + "control" + Style.RESET_ALL)
                self.control(int(self.arguments[1]), int(self.arguments[2]), int(self.arguments[3]), int(self.arguments[4]), int(self.arguments[5]))
                return

            # 이동(전체)
            #                   0         1   2   3   4          5         6
            # python -m e_drone position [x] [y] [z] [velocity] [heading] [rotational velocity]
            elif    ((self.count == 7) and 
                    (self.arguments[0] == "position")):
                print (Fore.YELLOW + "position" + Style.RESET_ALL)
                self.control_Position(float(self.arguments[1]), float(self.arguments[2]), float(self.arguments[3]), float(self.arguments[4]), float(self.arguments[5]), float(self.arguments[6]))
                return

            # 이동(위치)
            #                   0         1   2   3   4
            # python -m e_drone position [x] [y] [z] [velocity]
            elif    ((self.count == 5) and 
                    (self.arguments[0] == "position")):
                print (Fore.YELLOW + "position" + Style.RESET_ALL)
                self.control_Position(float(self.arguments[1]), float(self.arguments[2]), float(self.arguments[3]), float(self.arguments[4]), 0, 0)
                return

            # 이동(헤딩)
            #                   0        1         2
            # python -m e_drone heading [heading] [rotational velocity]
            elif    ((self.count == 3) and 
                    (self.arguments[0] == "heading")):
                print (Fore.YELLOW + "heading" + Style.RESET_ALL)
                self.control_Position(0, 0, 0, 0, float(self.arguments[1]), float(self.arguments[2]))
                return

            # 버저
            #                   1       2    3
            # python -m e_drone buzzer [hz] [time(ms)]
            # > python -m e_drone buzzer 400 2000
            elif    ((self.count == 3) and 
                    (self.arguments[0] == "buzzer")):
                print (Fore.WHITE + "Buzz Sound: " + Fore.YELLOW + "{0}".format(int(self.arguments[1])) + Fore.WHITE + "Hz, " + Fore.CYAN + "{0}".format(int(self.arguments[2])) + Fore.WHITE + "ms" + Style.RESET_ALL)
                self.buzzer(DeviceType.CONTROLLER, int(self.arguments[1]), int(self.arguments[2]))
                return

            # 진동
            #                   1         2          3           4
            # python -m e_drone vibrator [on(ms)] [off(ms)] [total(ms)]
            # > python -m e_drone vibrator 500 500 2000
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "vibrator")):
                print (Fore.WHITE + "Vibrator: on " + Fore.YELLOW + "{0}".format(int(self.arguments[1])) + Fore.WHITE + "ms, off " + Fore.CYAN + "{0}".format(int(self.arguments[2])) + Fore.WHITE + "ms, total " + Fore.CYAN + "{0}".format(int(self.arguments[3])) + Fore.WHITE + "ms" + Style.RESET_ALL)
                self.vibrator(DeviceType.CONTROLLER, int(self.arguments[1]), int(self.arguments[2]), int(self.arguments[3]))
                return


            # > python -m e_drone light body flicker 100 50 50 10
            # > python -m e_drone light body flickerdouble 100 50 50 10
            # > python -m e_drone light body dimming 3 50 50 10
            # > python -m e_drone light body sunrise 5 50 50 10
            # > python -m e_drone light body sunset 5 50 50 10
            # > python -m e_drone light body rainbow 8 50 50 10
            # > python -m e_drone light body rainbow2 8 50 50 10
            elif    ((self.count == 7) and 
                    (self.arguments[0] == "light")):
                print (Fore.WHITE + "Light: " + Fore.YELLOW + "{0}, {1}, {2}, ({3}, {4}, {5})".format(self.arguments[1], self.arguments[2], int(self.arguments[3]), int(self.arguments[4]), int(self.arguments[5]), int(self.arguments[6])) + Style.RESET_ALL)
                self.light_mode_rgb(self.arguments[1], self.arguments[2], int(self.arguments[3]), int(self.arguments[4]), int(self.arguments[5]), int(self.arguments[6]))
                return

            # > python -m e_drone light front hold 100
            # > python -m e_drone light head hold 100
            # > python -m e_drone light tail hold 100
            # > python -m e_drone light left hold 100
            # > python -m e_drone light right hold 100
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "light")):
                print (Fore.WHITE + "Light: " + Fore.YELLOW + "{0}, {1}, {2}".format(self.arguments[1], self.arguments[2], int(self.arguments[3])) + Style.RESET_ALL)
                self.light_mode_single(self.arguments[1], self.arguments[2], int(self.arguments[3]))
                return

        # 아무것도 실행되지 않은 경우
        self.help()


    def request(self, device_type, data_type, repeat, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        drone.set_event_handler(DataType.STATE, self.eventState)
        drone.set_event_handler(DataType.MOTION, self.eventMotion)
        drone.set_event_handler(DataType.CARD_RAW, self.eventCardRaw)
        drone.set_event_handler(DataType.CARD_RANGE, self.eventCardRange)

        # 데이터 요청
        for i in range(repeat):
            drone.send_request(device_type, data_type)
            sleep(interval)


    def command(self, command_type, option = 0):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)

        # 데이터 요청
        drone.send_command(command_type, option);


    def control(self, roll, pitch, yaw, throttle, time_ms):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)

        # 데이터 요청
        drone.send_control_while(roll, pitch, yaw, throttle, time_ms)
        drone.send_control_while(0, 0, 0, 0, 200)


    def control_position(self, x, y, z, velocity, heading, rotational_velocity):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)

        # 데이터 요청
        drone.send_control_position(x, y, z, velocity, heading, rotational_velocity)
        sleep(0.1)


    def light_mode_rgb(self, str_light_part, str_light_mode, interval, r, g, b):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int)) ):
            return None

        light_mode_high = LightModeDrone.NONE

        if      str_light_part == "rear":
            light_mode_high = LightModeDrone.REAR_NONE
        elif    str_light_part == "body":
            light_mode_high = LightModeDrone.BODY_NONE
        elif    str_light_part == "a":
            light_mode_high = LightModeDrone.A_NONE
        elif    str_light_part == "b":
            light_mode_high = LightModeDrone.B_NONE

        light_mode_low = LightModeDrone.NONE

        if      str_light_mode == "hold":
            light_mode_low = LightModeDrone.BODY_HOLD
        elif    str_light_mode == "flicker":
            light_mode_low = LightModeDrone.BODY_FLICKER
        elif    str_light_mode == "flickerdouble":
            light_mode_low = LightModeDrone.BODY_FLICKER_DOUBLE
        elif    str_light_mode == "dimming":
            light_mode_low = LightModeDrone.BODY_DIMMING
        elif    str_light_mode == "sunrise":
            light_mode_low = LightModeDrone.BODY_SUNRISE
        elif    str_light_mode == "sunset":
            light_mode_low = LightModeDrone.BODY_SUNSET
        elif    str_light_mode == "rainbow":
            light_mode_low = LightModeDrone.BODY_RAINBOW
        elif    str_light_mode == "rainbow2":
            light_mode_low = LightModeDrone.BODY_RAINBOW2

        light_mode = LightModeDrone(light_mode_high.value + ((light_mode_low.value) & 0x0F))

        if light_mode_high != LightModeDrone.NONE and light_mode_low != LightModeDrone.NONE:
            drone.send_light_mode_color(light_mode, interval, r, g, b)


    def light_mode_single(self, str_light_part, str_light_mode, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(interval, int)) ):
            return None

        light_mode_high = LightModeDrone.NONE

        if      str_light_part == "rear":
            light_mode_high = LightModeDrone.REAR_NONE
        elif    str_light_part == "body":
            light_mode_high = LightModeDrone.BODY_NONE
        elif    str_light_part == "a":
            light_mode_high = LightModeDrone.A_NONE
        elif    str_light_part == "b":
            light_mode_high = LightModeDrone.B_NONE

        light_mode_low = LightModeDrone.NONE

        if      str_light_mode == "hold":
            light_mode_low = LightModeDrone.BODY_HOLD
        elif    str_light_mode == "flicker":
            light_mode_low = LightModeDrone.BODY_FLICKER
        elif    str_light_mode == "flickerdouble":
            light_mode_low = LightModeDrone.BODY_FLICKER_DOUBLE
        elif    str_light_mode == "dimming":
            light_mode_low = LightModeDrone.BODY_DIMMING
        elif    str_light_mode == "sunrise":
            light_mode_low = LightModeDrone.BODY_SUNRISE
        elif    str_light_mode == "sunset":
            light_mode_low = LightModeDrone.BODY_SUNSET
        elif    str_light_mode == "rainbow":
            light_mode_low = LightModeDrone.BODY_RAINBOW
        elif    str_light_mode == "rainbow2":
            light_mode_low = LightModeDrone.BODY_RAINBOW2

        light_mode = LightModeDrone(light_mode_high.value + ((light_mode_low.value) & 0x0F))

        if light_mode_high != LightModeDrone.NONE and light_mode_low != LightModeDrone.NONE:
            drone.send_light_mode(light_mode, interval)


    def buzzer(self, target, hz, time):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(hz, int)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length   = Buzzer.get_size()
        header.from_    = DeviceType.BASE
        header.to_      = target
        
        data = Buzzer()

        data.mode       = BuzzerMode.HZ
        data.value      = hz
        data.time       = time

        drone.transfer(header, data)
        sleep(time / 1000)


    def vibrator(self, target, on, off, total):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(on, int)) or (not isinstance(off, int)) or (not isinstance(total, int)) ):
            return None

        header = Header()
        
        header.data_type = DataType.VIBRATOR
        header.length    = Vibrator.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = target
        
        data = Vibrator()

        data.mode       = VibratorMode.INSTANTALLY
        data.on         = on
        data.off        = off
        data.total      = total

        drone.transfer(header, data)
        sleep(total / 1000)


    def help(self):

        print("")
        print(Fore.YELLOW + "* Command List " + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Firmware Upgrade" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "upgrade" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Request Data" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "request " + Fore.WHITE + "[" + Fore.YELLOW + "data type" + Fore.WHITE + "] [" + Fore.GREEN + "number of times" + Fore.WHITE + "] [" + Fore.YELLOW + "time interval(sec)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "request " + Fore.YELLOW + "state " + Fore.GREEN + "10 " + Fore.YELLOW + "0.2" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "request " + Fore.YELLOW + "motion " + Fore.GREEN + "10 " + Fore.YELLOW + "0.2" + Style.RESET_ALL)
        ## 카드 코딩과 관련된 내용이 최신 버전인지 알 수 없는 관계로 일단 보류(2021.1.4)
        ##print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "request " + Fore.YELLOW + "RawCard " + Fore.GREEN + "10 " + Fore.YELLOW + "0.2" + Style.RESET_ALL)
        ##print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "request " + Fore.YELLOW + "RawCardRange " + Fore.GREEN + "10 " + Fore.YELLOW + "0.2" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - FlightEvent" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.WHITE + "[" + Fore.YELLOW + "FlightEvent" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.YELLOW + "takeoff" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.YELLOW + "landing" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.YELLOW + "stop" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Control" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "control " + Fore.WHITE + "[" + Fore.RED + "roll" + Fore.WHITE + "] [" + Fore.GREEN + "pitch" + Fore.WHITE + "] [" + Fore.BLUE + "yaw" + Fore.WHITE + "] [" + Fore.MAGENTA + "throttle" + Fore.WHITE + "] [" + Fore.YELLOW + "time(ms)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "control " + Fore.RED + "0 " + Fore.GREEN + "30 " + Fore.BLUE + "0 " + Fore.MAGENTA + "0 " + Fore.YELLOW + "5000 " + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Control - Position, Heading" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "position " + Fore.WHITE + "[" + Fore.RED + "x(meter)" + Fore.WHITE + "] [" + Fore.GREEN + "y(meter)" + Fore.WHITE + "] [" + Fore.BLUE + "z(meter)" + Fore.WHITE + "] [" + Fore.YELLOW + "speed(m/sec)" + Fore.WHITE + "] [" + Fore.MAGENTA + "heading(degree)" + Fore.WHITE + "] [" + Fore.YELLOW + "rotational velocity(deg/sec)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "position " + Fore.RED + "5 " + Fore.GREEN + "0 " + Fore.BLUE + "0 "  + Fore.YELLOW + "2 " + Fore.MAGENTA + "90 " + Fore.YELLOW + "45 "+ Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Control - Position" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "position " + Fore.WHITE + "[" + Fore.RED + "x(meter)" + Fore.WHITE + "] [" + Fore.GREEN + "y(meter)" + Fore.WHITE + "] [" + Fore.BLUE + "z(meter)" + Fore.WHITE + "] [" + Fore.YELLOW + "speed(m/sec)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "position " + Fore.RED + "5 " + Fore.GREEN + "0 " + Fore.BLUE + "0 "  + Fore.YELLOW + "2 " + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Control - Heading" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "heading " + Fore.WHITE + "[" + Fore.MAGENTA + "heading(degree)" + Fore.WHITE + "] [" + Fore.YELLOW + "rotational velocity(deg/sec)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "heading " + Fore.MAGENTA + "90 " + Fore.YELLOW + "45" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Buzzer" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "buzzer " + Fore.WHITE + "[" + Fore.YELLOW + "hz" + Fore.WHITE + "] [" + Fore.GREEN + "time(ms)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "buzzer " + Fore.YELLOW + "400 " + Fore.GREEN + "2000" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Vibrator" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "vibrator " + Fore.WHITE + "[" + Fore.YELLOW + "on(ms)" + Fore.WHITE + "] [" + Fore.GREEN + "off(ms)" + Fore.WHITE + "] [" + Fore.YELLOW + "total(ms)" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "vibrator " + Fore.YELLOW + "500 " + Fore.GREEN + "500 " + Fore.YELLOW + "2000" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Light single" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.WHITE + "[" + Fore.MAGENTA + "part" + Fore.WHITE + "] [" + Fore.CYAN + "mode" + Fore.WHITE + "] [" + Fore.YELLOW + "interval" + Fore.WHITE + "]" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "rear " + Fore.CYAN + "hold " + Fore.YELLOW + "100" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "a " + Fore.CYAN + "hold " + Fore.YELLOW + "100" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "b " + Fore.CYAN + "hold " + Fore.YELLOW + "100" + Style.RESET_ALL)

        print("")
        print(Fore.CYAN + "  - Light RGB" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.WHITE + "[" + Fore.MAGENTA + "part" + Fore.WHITE + "] [" + Fore.CYAN + "mode" + Fore.WHITE + "] [" + Fore.YELLOW + "interval" + Fore.WHITE + "] [" + Fore.RED + "R" + Fore.WHITE + "] [" + Fore.GREEN + "G" + Fore.WHITE + "] [" + Fore.BLUE + "B" + Fore.WHITE + "] " + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "hold " + Fore.YELLOW + "100 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "flicker " + Fore.YELLOW + "100 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "flickerdouble " + Fore.YELLOW + "100 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "dimming " + Fore.YELLOW + "3 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "sunrise " + Fore.YELLOW + "5 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "sunset " + Fore.YELLOW + "5 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "rainbow " + Fore.YELLOW + "8 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print(Fore.GREEN + "   > " + Fore.WHITE + "python -m e_drone " + Fore.CYAN + "light " + Fore.MAGENTA + "body " + Fore.CYAN + "rainbow2 " + Fore.YELLOW + "8 " + Fore.RED + "50 " + Fore.GREEN + "50 " + Fore.BLUE + "10" + Style.RESET_ALL)
        print("")


    def event_state(self, state):

        print(  "* State   " +
                Fore.YELLOW + "{0:12}  ".format(state.mode_system.name) +
                Fore.YELLOW + "{0:10}  ".format(state.mode_flight.name) +
                Fore.WHITE + "{0:17}  ".format(state.mode_control_flight.name) +
                Fore.WHITE + "{0:12}  ".format(state.mode_movement.name) +
                Fore.WHITE + "{0:8}  ".format(state.headless.name) +
                Fore.CYAN + "{0:12}  ".format(state.control_speed) +
                Fore.CYAN + "{0:17}  ".format(state.sensor_orientation.name) +
                Fore.GREEN + "{0:7}".format(state.battery) + Style.RESET_ALL)
                


    def event_motion(self, motion):

        print(  "* Motion " +
                Fore.YELLOW + "{0:8}".format(motion.accel_x) +
                Fore.YELLOW + "{0:8}".format(motion.accel_y) +
                Fore.YELLOW + "{0:8}".format(motion.accel_z) +
                Fore.WHITE + "{0:8}".format(motion.gyro_roll) +
                Fore.WHITE + "{0:8}".format(motion.gyro_pitch) +
                Fore.WHITE + "{0:8}".format(motion.gyro_yaw) +
                Fore.CYAN + "{0:8}".format(motion.angle_roll) +
                Fore.CYAN + "{0:8}".format(motion.angle_pitch) +
                Fore.CYAN + "{0:8}".format(motion.angle_yaw) + Style.RESET_ALL)


    def event_card_range(self, card_range):
        
        print(  "* RawCardRange " +
                Fore.RED    + "{0:6}".format(card_range.range[0][0][0]) +
                Fore.RED    + "{0:6}".format(card_range.range[0][0][1]) +
                Fore.GREEN  + "{0:6}".format(card_range.range[0][1][0]) +
                Fore.GREEN  + "{0:6}".format(card_range.range[0][1][1]) +
                Fore.BLUE   + "{0:6}".format(card_range.range[0][2][0]) +
                Fore.BLUE   + "{0:6}".format(card_range.range[0][2][1]) +
                Fore.RED    + "{0:6}".format(card_range.range[1][0][0]) +
                Fore.RED    + "{0:6}".format(card_range.range[1][0][1]) +
                Fore.GREEN  + "{0:6}".format(card_range.range[1][1][0]) +
                Fore.GREEN  + "{0:6}".format(card_range.range[1][1][1]) +
                Fore.BLUE   + "{0:6}".format(card_range.range[1][2][0]) +
                Fore.BLUE   + "{0:6}".format(card_range.range[1][2][1]) + Style.RESET_ALL)


    def event_card_raw(self, card_raw):

        print(  "* RawCard " +
                Fore.RED    + "{0:5}".format(card_raw.rgb_raw[0][0]) +
                Fore.GREEN  + "{0:5}".format(card_raw.rgb_raw[0][1]) +
                Fore.BLUE   + "{0:5}".format(card_raw.rgb_raw[0][2]) +
                Fore.RED    + "{0:5}".format(card_raw.rgb_raw[1][0]) +
                Fore.GREEN  + "{0:5}".format(card_raw.rgb_raw[1][1]) +
                Fore.BLUE   + "{0:5}".format(card_raw.rgb_raw[1][2]) +
                Fore.RED    + "{0:4}".format(card_raw.rgb[0][0]) +
                Fore.GREEN  + "{0:4}".format(card_raw.rgb[0][1]) +
                Fore.BLUE   + "{0:4}".format(card_raw.rgb[0][2]) +
                Fore.RED    + "{0:4}".format(card_raw.rgb[1][0]) +
                Fore.GREEN  + "{0:4}".format(card_raw.rgb[1][1]) +
                Fore.BLUE   + "{0:4}".format(card_raw.rgb[1][2]) +
                Fore.RED    + "{0:4}".format(card_raw.hsvl[0][0]) +
                Fore.GREEN  + "{0:4}".format(card_raw.hsvl[0][1]) +
                Fore.BLUE   + "{0:4}".format(card_raw.hsvl[0][2]) +
                Fore.BLUE   + "{0:4}".format(card_raw.hsvl[0][3]) +
                Fore.RED    + "{0:4}".format(card_raw.hsvl[1][0]) +
                Fore.GREEN  + "{0:4}".format(card_raw.hsvl[1][1]) +
                Fore.BLUE   + "{0:4}".format(card_raw.hsvl[1][2]) +
                Fore.BLUE   + "{0:4}".format(card_raw.hsvl[1][3]) +
                Fore.CYAN   + "{0:14}".format(card_raw.color[0].name) +
                Fore.CYAN   + "{0:14}".format(card_raw.color[1].name) +
                Fore.CYAN   + "{0:14}".format(card_raw.card.name) + Style.RESET_ALL)


# Parser End
