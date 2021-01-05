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

            print("Count:{0} ".format(self.count) , end='')

            for arg in self.arguments:
                print("/ {0} ".format(arg), end='')

            print("")

            # >python -m e_drone upgrade
            # >python -m e_drone update
            if      (self.arguments[0] == "upgrade") or (self.arguments[0] == "update"):
                updater = Updater()
                updater.update()
                return

            # >python -m e_drone request State 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "state")):         # time interval
                #print("* State - Ready     Blue    Red     Black   Black   None_             1830   1631   2230      76      ")    
                print ("         |ModeSystem   |ModeFlight |ModeControlFlight |ModeMovement |Headless |ControlSpeed |SensorOrientation |Battery |")
                self.request(DeviceType.Drone, DataType.State, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drone request Motion 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "motion")):         # time interval
                #print("* Motion      -38      64     -32     457     -40    -400      16       0   20500")    
                print ("         |Accel                  |Gyro                   |Angle                  |")
                print ("         |      X|      Y|      Z|   Roll|  Pitch|    Yaw|   Roll|  Pitch|    Yaw|")
                self.request(DeviceType.Drone, DataType.Motion, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drone request CardRaw 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "cardraw")):         # time interval
                #print("* CardRaw   335  503  766  692  309  395 100  39  96  40   9  17 303  61  39 344  77  15   Magenta         Red")
                print ("          |Front Raw     |Rear Raw      |Front RGB  |Rear RGB   |Front HSVL      |Rear HSVL       |Front Color  |Rear Color   |")
                print ("          |   R    G    B|   R    G    B|  R   G   B|  R   G   B|  H   S   V   L|  H   S   V   L|             |             |")
                self.request(DeviceType.Drone, DataType.CardRaw, int(self.arguments[2]), float(self.arguments[3]))
                return

            # >python -m e_drone request CardRange 10 0.2
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "request") and
                    (self.arguments[1] == "cardrange")):         # time interval
                #print("* CardRange       200  2000   200  2000   200  2000   200     0   200     0   200     0")
                print ("               |Front                              |Rear                               |")
                print ("               |Red        |Green      |Blue       |Red        |Green      |Blue       |")
                print ("               |  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|  Min|  Max|")
                self.request(DeviceType.Drone, DataType.CardRange, int(self.arguments[2]), float(self.arguments[3]))
                return

            # 이륙
            #                   0
            # python -m e_drone Takeoff
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "takeoff")):
                print (Fore.YELLOW + "takeoff" + Style.RESET_ALL)
                self.command(CommandType.FlightEvent, FlightEvent.TakeOff.value)
                return

            # 착륙
            #                   0
            # python -m e_drone Landing
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "landing")):
                print (Fore.YELLOW + "landing" + Style.RESET_ALL)
                self.command(CommandType.FlightEvent, FlightEvent.Landing.value)
                return

            # 정지
            #                   0
            # python -m e_drone Stop
            elif    ((self.count == 1) and 
                    (self.arguments[0] == "stop")):
                print (Fore.YELLOW + "stop" + Style.RESET_ALL)
                self.command(CommandType.FlightEvent, FlightEvent.Stop.value)
                return

            # 조종
            #                   0        1      2       3     4          5
            # python -m e_drone control [roll] [pitch] [yaw] [throttle] [time(ms)]
            # 지정한 시간이 종료되면 입력값을 모두 0으로 변경하고 멈춤
            # >python -m e_drone control 40 0 3
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
                self.controlPosition(float(self.arguments[1]), float(self.arguments[2]), float(self.arguments[3]), float(self.arguments[4]), float(self.arguments[5]), float(self.arguments[6]))
                return

            # 이동(위치)
            #                   0         1   2   3   4
            # python -m e_drone position [x] [y] [z] [velocity]
            elif    ((self.count == 5) and 
                    (self.arguments[0] == "position")):
                print (Fore.YELLOW + "position" + Style.RESET_ALL)
                self.controlPosition(float(self.arguments[1]), float(self.arguments[2]), float(self.arguments[3]), float(self.arguments[4]), 0, 0)
                return

            # 이동(헤딩)
            #                   0        1         2
            # python -m e_drone heading [heading] [rotational velocity]
            elif    ((self.count == 3) and 
                    (self.arguments[0] == "heading")):
                print (Fore.YELLOW + "heading" + Style.RESET_ALL)
                self.controlPosition(0, 0, 0, 0, float(self.arguments[1]), float(self.arguments[2]))
                return

            # 버저
            #                   1       2    3
            # python -m e_drone buzzer [hz] [time(ms)]
            # >python -m e_drone buzzer 400 2000
            elif    ((self.count == 3) and 
                    (self.arguments[0] == "buzzer")):
                print (Fore.WHITE + "Buzz Sound: " + Fore.YELLOW + "{0}".format(int(self.arguments[1])) + Fore.WHITE + "Hz, " + Fore.CYAN + "{0}".format(int(self.arguments[2])) + Fore.WHITE + "ms" + Style.RESET_ALL)
                self.buzzer(DeviceType.Controller, int(self.arguments[1]), int(self.arguments[2]))
                return

            # 진동
            #                   1         2          3           4
            # python -m e_drone vibrator [on(ms)] [off(ms)] [total(ms)]
            # >python -m e_drone vibrator 500 500 2000
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "vibrator")):
                print (Fore.WHITE + "Vibrator: on " + Fore.YELLOW + "{0}".format(int(self.arguments[1])) + Fore.WHITE + "ms, off " + Fore.CYAN + "{0}".format(int(self.arguments[2])) + Fore.WHITE + "ms, total " + Fore.CYAN + "{0}".format(int(self.arguments[3])) + Fore.WHITE + "ms" + Style.RESET_ALL)
                self.vibrator(DeviceType.Controller, int(self.arguments[1]), int(self.arguments[2]), int(self.arguments[3]))
                return


            # >python -m e_drone light body flicker 100 50 50 10
            # >python -m e_drone light body flickerdouble 100 50 50 10
            # >python -m e_drone light body dimming 3 50 50 10
            # >python -m e_drone light body sunrise 5 50 50 10
            # >python -m e_drone light body sunset 5 50 50 10
            # >python -m e_drone light body rainbow 8 50 50 10
            # >python -m e_drone light body rainbow2 8 50 50 10
            elif    ((self.count == 7) and 
                    (self.arguments[0] == "light")):
                print (Fore.WHITE + "Light: " + Fore.YELLOW + "{0}, {1}, {2}, ({3}, {4}, {5})".format(self.arguments[1], self.arguments[2], int(self.arguments[3]), int(self.arguments[4]), int(self.arguments[5]), int(self.arguments[6])) + Style.RESET_ALL)
                self.lightModeRgb(self.arguments[1], self.arguments[2], int(self.arguments[3]), int(self.arguments[4]), int(self.arguments[5]), int(self.arguments[6]))
                return

            # >python -m e_drone light front hold 100
            # >python -m e_drone light head hold 100
            # >python -m e_drone light tail hold 100
            # >python -m e_drone light left hold 100
            # >python -m e_drone light right hold 100
            elif    ((self.count == 4) and 
                    (self.arguments[0] == "light")):
                print (Fore.WHITE + "Light: " + Fore.YELLOW + "{0}, {1}, {2}".format(self.arguments[1], self.arguments[2], int(self.arguments[3])) + Style.RESET_ALL)
                self.lightModeSingle(self.arguments[1], self.arguments[2], int(self.arguments[3]))
                return

        # 아무것도 실행되지 않은 경우
        self.help()


    def request(self, deviceType, dataType, repeat, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        # 이벤트 핸들링 함수 등록
        drone.setEventHandler(DataType.State, self.eventState)
        drone.setEventHandler(DataType.Motion, self.eventMotion)
        drone.setEventHandler(DataType.CardRaw, self.eventCardRaw)
        drone.setEventHandler(DataType.CardRange, self.eventCardRange)

        # 데이터 요청
        for i in range(repeat):
            drone.sendRequest(deviceType, dataType)
            sleep(interval)


    def command(self, commandType, option = 0):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)

        # 데이터 요청
        drone.sendCommand(commandType, option);


    def control(self, roll, pitch, yaw, throttle, timeMs):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)

        # 데이터 요청
        drone.sendControlWhile(roll, pitch, yaw, throttle, timeMs)
        drone.sendControlWhile(0, 0, 0, 0, 200)


    def controlPosition(self, x, y, z, velocity, heading, rotationalVelocity):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)

        # 데이터 요청
        drone.sendControlPosition(x, y, z, velocity, heading, rotationalVelocity)
        sleep(0.1)


    def lightModeRgb(self, strLightPart, strLightMode, interval, r, g, b):

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

        lightModeHigh = LightModeDrone.None_

        if      strLightPart == "rear":
            lightModeHigh = LightModeDrone.RearNone
        elif    strLightPart == "body":
            lightModeHigh = LightModeDrone.BodyNone
        elif    strLightPart == "a":
            lightModeHigh = LightModeDrone.ANone
        elif    strLightPart == "b":
            lightModeHigh = LightModeDrone.BNone

        lightModeLow = LightModeDrone.None_

        if      strLightMode == "hold":
            lightModeLow = LightModeDrone.BodyHold
        elif    strLightMode == "flicker":
            lightModeLow = LightModeDrone.BodyFlicker
        elif    strLightMode == "flickerdouble":
            lightModeLow = LightModeDrone.BodyFlickerDouble
        elif    strLightMode == "dimming":
            lightModeLow = LightModeDrone.BodyDimming
        elif    strLightMode == "sunrise":
            lightModeLow = LightModeDrone.BodySunrise
        elif    strLightMode == "sunset":
            lightModeLow = LightModeDrone.BodySunset
        elif    strLightMode == "rainbow":
            lightModeLow = LightModeDrone.BodyRainbow
        elif    strLightMode == "rainbow2":
            lightModeLow = LightModeDrone.BodyRainbow2

        lightMode = LightModeDrone(lightModeHigh.value + ((lightModeLow.value) & 0x0F))

        if lightModeHigh != LightModeDrone.None_ and lightModeLow != LightModeDrone.None_:
            drone.sendLightModeColor(lightMode, interval, r, g, b)


    def lightModeSingle(self, strLightPart, strLightMode, interval):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(interval, int)) ):
            return None

        lightModeHigh = LightModeDrone.None_

        if      strLightPart == "rear":
            lightModeHigh = LightModeDrone.RearNone
        elif    strLightPart == "body":
            lightModeHigh = LightModeDrone.BodyNone
        elif    strLightPart == "a":
            lightModeHigh = LightModeDrone.ANone
        elif    strLightPart == "b":
            lightModeHigh = LightModeDrone.BNone

        lightModeLow = LightModeDrone.None_

        if      strLightMode == "hold":
            lightModeLow = LightModeDrone.BodyHold
        elif    strLightMode == "flicker":
            lightModeLow = LightModeDrone.BodyFlicker
        elif    strLightMode == "flickerdouble":
            lightModeLow = LightModeDrone.BodyFlickerDouble
        elif    strLightMode == "dimming":
            lightModeLow = LightModeDrone.BodyDimming
        elif    strLightMode == "sunrise":
            lightModeLow = LightModeDrone.BodySunrise
        elif    strLightMode == "sunset":
            lightModeLow = LightModeDrone.BodySunset
        elif    strLightMode == "rainbow":
            lightModeLow = LightModeDrone.BodyRainbow
        elif    strLightMode == "rainbow2":
            lightModeLow = LightModeDrone.BodyRainbow2

        lightMode = LightModeDrone(lightModeHigh.value + ((lightModeLow.value) & 0x0F))

        if lightModeHigh != LightModeDrone.None_ and lightModeLow != LightModeDrone.None_:
            drone.sendLightMode(lightMode, interval)


    def buzzer(self, target, hz, time):

        #drone = Drone(True, True, True, True, True)
        drone = Drone()
        if drone.open() == False:
            print(Fore.RED + "* Error : Unable to open serial port." + Style.RESET_ALL)
            sys.exit(1)
        
        if ( (not isinstance(hz, int)) or (not isinstance(time, int)) ):
            return None

        header = Header()
        
        header.dataType = DataType.Buzzer
        header.length   = Buzzer.getSize()
        header.from_    = DeviceType.Base
        header.to_      = target
        
        data = Buzzer()

        data.mode       = BuzzerMode.Hz
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
        
        header.dataType = DataType.Vibrator
        header.length   = Vibrator.getSize()
        header.from_    = DeviceType.Base
        header.to_      = target
        
        data = Vibrator()

        data.mode       = VibratorMode.Instantally
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


    def eventState(self, state):

        print(  "* State   " +
                Fore.YELLOW + "{0:12}  ".format(state.modeSystem.name) +
                Fore.YELLOW + "{0:10}  ".format(state.modeFlight.name) +
                Fore.WHITE + "{0:17}  ".format(state.modeControlFlight.name) +
                Fore.WHITE + "{0:12}  ".format(state.modeMovement.name) +
                Fore.WHITE + "{0:8}  ".format(state.headless.name) +
                Fore.CYAN + "{0:12}  ".format(state.controlSpeed) +
                Fore.CYAN + "{0:17}  ".format(state.sensorOrientation.name) +
                Fore.GREEN + "{0:7}".format(state.battery) + Style.RESET_ALL)
                


    def eventMotion(self, motion):

        print(  "* Motion " +
                Fore.YELLOW + "{0:8}".format(motion.accelX) +
                Fore.YELLOW + "{0:8}".format(motion.accelY) +
                Fore.YELLOW + "{0:8}".format(motion.accelZ) +
                Fore.WHITE + "{0:8}".format(motion.gyroRoll) +
                Fore.WHITE + "{0:8}".format(motion.gyroPitch) +
                Fore.WHITE + "{0:8}".format(motion.gyroYaw) +
                Fore.CYAN + "{0:8}".format(motion.angleRoll) +
                Fore.CYAN + "{0:8}".format(motion.anglePitch) +
                Fore.CYAN + "{0:8}".format(motion.angleYaw) + Style.RESET_ALL)


    def eventCardRange(self, cardRange):
        
        print(  "* RawCardRange " +
                Fore.RED    + "{0:6}".format(cardRange.range[0][0][0]) +
                Fore.RED    + "{0:6}".format(cardRange.range[0][0][1]) +
                Fore.GREEN  + "{0:6}".format(cardRange.range[0][1][0]) +
                Fore.GREEN  + "{0:6}".format(cardRange.range[0][1][1]) +
                Fore.BLUE   + "{0:6}".format(cardRange.range[0][2][0]) +
                Fore.BLUE   + "{0:6}".format(cardRange.range[0][2][1]) +
                Fore.RED    + "{0:6}".format(cardRange.range[1][0][0]) +
                Fore.RED    + "{0:6}".format(cardRange.range[1][0][1]) +
                Fore.GREEN  + "{0:6}".format(cardRange.range[1][1][0]) +
                Fore.GREEN  + "{0:6}".format(cardRange.range[1][1][1]) +
                Fore.BLUE   + "{0:6}".format(cardRange.range[1][2][0]) +
                Fore.BLUE   + "{0:6}".format(cardRange.range[1][2][1]) + Style.RESET_ALL)


    def eventCardRaw(self, cardRaw):

        print(  "* RawCard " +
                Fore.RED    + "{0:5}".format(cardRaw.rgbRaw[0][0]) +
                Fore.GREEN  + "{0:5}".format(cardRaw.rgbRaw[0][1]) +
                Fore.BLUE   + "{0:5}".format(cardRaw.rgbRaw[0][2]) +
                Fore.RED    + "{0:5}".format(cardRaw.rgbRaw[1][0]) +
                Fore.GREEN  + "{0:5}".format(cardRaw.rgbRaw[1][1]) +
                Fore.BLUE   + "{0:5}".format(cardRaw.rgbRaw[1][2]) +
                Fore.RED    + "{0:4}".format(cardRaw.rgb[0][0]) +
                Fore.GREEN  + "{0:4}".format(cardRaw.rgb[0][1]) +
                Fore.BLUE   + "{0:4}".format(cardRaw.rgb[0][2]) +
                Fore.RED    + "{0:4}".format(cardRaw.rgb[1][0]) +
                Fore.GREEN  + "{0:4}".format(cardRaw.rgb[1][1]) +
                Fore.BLUE   + "{0:4}".format(cardRaw.rgb[1][2]) +
                Fore.RED    + "{0:4}".format(cardRaw.hsvl[0][0]) +
                Fore.GREEN  + "{0:4}".format(cardRaw.hsvl[0][1]) +
                Fore.BLUE   + "{0:4}".format(cardRaw.hsvl[0][2]) +
                Fore.BLUE   + "{0:4}".format(cardRaw.hsvl[0][3]) +
                Fore.RED    + "{0:4}".format(cardRaw.hsvl[1][0]) +
                Fore.GREEN  + "{0:4}".format(cardRaw.hsvl[1][1]) +
                Fore.BLUE   + "{0:4}".format(cardRaw.hsvl[1][2]) +
                Fore.BLUE   + "{0:4}".format(cardRaw.hsvl[1][3]) +
                Fore.CYAN   + "{0:14}".format(cardRaw.color[0].name) +
                Fore.CYAN   + "{0:14}".format(cardRaw.color[1].name) +
                Fore.CYAN   + "{0:14}".format(cardRaw.card.name) + Style.RESET_ALL)


# Parser End
