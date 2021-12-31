import serial
import binascii
import random
import queue
import threading
from threading import Thread
from time import sleep
from struct import *
import time
from serial.tools.list_ports import comports
from queue import Queue
from operator import eq
import colorama
from colorama import Fore, Back, Style

from e_drone.protocol import *
from e_drone.storage import *
from e_drone.receiver import *
from e_drone.system import *
from e_drone.crc import *


def convert_byte_array_to_string(data_array):

    if data_array is None:
        return ""

    string = ""

    if (isinstance(data_array, bytes)) or (isinstance(data_array, bytearray)) or (not isinstance(data_array, list)):
        for data in data_array:
            string += "{0:02X} ".format(data)

    return string


class Drone:

    # BaseFunctions Start
    def __init__(self, flag_check_background=True, flag_show_error_message=False, flag_show_log_message=False, flag_show_transfer_data=False, flag_show_receive_data=False):
        
        self._serialport = None
        self._buffer_queue = Queue(4096)
        self._buffer_handler = bytearray()
        self._index = 0

        self._thread = None
        self._flag_thread_run = False

        self._receiver = Receiver()

        self._flag_check_background = flag_check_background

        self._flag_show_error_message = flag_show_error_message
        self._flag_show_log_message = flag_show_log_message
        self._flag_show_transfer_data = flag_show_transfer_data
        self._flag_show_receive_data = flag_show_receive_data

        self._event_handler = EventHandler()
        self._storage_header = StorageHeader()
        self._storage = Storage()
        self._storage_count = StorageCount()
        self._parser = Parser()

        self._devices = []            # 자동 연결 시 검색된 장치 목록을 저장
        self._flag_discover = False         # 자동 연결 시 장치를 검색중인지를 표시
        self._flag_connected = False         # 자동 연결 시 장치와 연결되었는지를 알려줌

        self.time_start_program = time.time()           # 프로그램 시작 시각 기록

        self.system_time_monitor_data = 0
        self.monitor_data = []

        for i in range(0, 36):
            self.monitor_data.append(i)

        colorama.init()


    def __del__(self):
        
        self.close()


    def _receiving(self):
        while self._flag_thread_run:
            
            self._buffer_queue.put(self._serialport.read())

            # 수신 데이터 백그라운드 확인이 활성화 된 경우 데이터 자동 업데이트
            if self._flag_check_background == True:
                while self.check() != DataType.NONE:
                    pass

            #sleep(0.001)


    def is_open(self):
        if self._serialport is not None:
            return self._serialport.is_open
        else:
            return False


    def is_connected(self):
        if self.is_open() == False:
            return False
        else:
            return self._flag_connected


    def open(self, port_name="None"):
        if eq(port_name, "None"):
            nodes = comports()
            size = len(nodes)
            if size > 0:
                port_name = nodes[size - 1].device
            else:
                return False

        try:
            self._serialport = serial.Serial(port=port_name, baudrate=57600)

            if(self.is_open()):
                self._flag_thread_run = True
                self._thread = Thread(target=self._receiving, args=(), daemon=True)
                self._thread.start()

                # 로그 출력
                self._print_log("Connected.({0})".format(port_name))

                return True
            else:
                # 오류 메세지 출력
                self._print_error("Could not connect to device.")

                return False

        except:
            # 오류 메세지 출력
            self._print_error("Could not connect to device.")

            return False


    def close(self):
        # 로그 출력
        if self.is_open():
            self._print_log("Closing serial port.")

        self._print_log("Thread Flag False.")

        if self._flag_thread_run == True:
            self._flag_thread_run = False
            sleep(0.1)
        
        self._print_log("Thread Join.")

        if self._thread is not None:
            self._thread.join(timeout = 1)

        self._print_log("Port Close.")

        if self.is_open() == True:
            self._serialport.close()
            sleep(0.2)


    def make_transfer_data_array(self, header, data):
        if (header is None) or (data is None):
            return None

        if (not isinstance(header, Header)):
            return None

        if (isinstance(data, ISerializable)):
            data = data.to_array()

        crc16 = Crc16.calc(header.to_array(), 0)
        crc16 = Crc16.calc(data, crc16)

        data_array = bytearray()
        data_array.extend((0x0A, 0x55))
        data_array.extend(header.to_array())
        data_array.extend(data)
        data_array.extend(pack('H', crc16))

        return data_array


    def transfer(self, header, data):
        if not self.is_open():
            return

        data_array = self.make_transfer_data_array(header, data)

        self._serialport.write(data_array)

        # 송신 데이터 출력
        self._print_transfer_data(data_array)

        return data_array


    def check(self):
        while self._buffer_queue.empty() == False:
            data_array = self._buffer_queue.get_nowait()
            self._buffer_queue.task_done()

            if (data_array is not None) and (len(data_array) > 0):
                # 수신 데이터 출력
                self._print_receive_data(data_array)

                self._buffer_handler.extend(data_array)

        while len(self._buffer_handler) > 0:
            state_loading = self._receiver.call(self._buffer_handler.pop(0))

            # 오류 출력
            if state_loading == StateLoading.FAILURE:
                # 수신 데이터 출력(줄넘김)
                self._print_receive_data_end()

                # 오류 메세지 출력
                self._print_error(self._receiver.message)
                

            # 로그 출력
            if state_loading == StateLoading.LOADED:
                # 수신 데이터 출력(줄넘김)
                self._print_receive_data_end()

                # 로그 출력
                self._print_log(self._receiver.message)

            if self._receiver.state == StateLoading.LOADED:
                self._handler(self._receiver.header, self._receiver.data)
                return self._receiver.header.data_type

        return DataType.NONE


    def check_detail(self):
        while self._buffer_queue.empty() == False:
            data_array = self._buffer_queue.get_nowait()
            self._buffer_queue.task_done()

            if (data_array is not None) and (len(data_array) > 0):
                # 수신 데이터 출력
                self._print_receive_data(data_array)

                self._buffer_handler.extend(data_array)

        while len(self._buffer_handler) > 0:
            state_loading = self._receiver.call(self._buffer_handler.pop(0))

            # 오류 출력
            if state_loading == StateLoading.FAILURE:
                # 수신 데이터 출력(줄넘김)
                self._print_receive_data_end()

                # 오류 메세지 출력
                self._print_error(self._receiver.message)
                

            # 로그 출력
            if state_loading == StateLoading.LOADED:
                # 수신 데이터 출력(줄넘김)
                self._print_receive_data_end()

                # 로그 출력
                self._print_log(self._receiver.message)

            if self._receiver.state == StateLoading.LOADED:
                self._handler(self._receiver.header, self._receiver.data)
                return self._receiver.header, self._receiver.data

        return None, None


    def _handler(self, header, data_array):

        # 들어오는 데이터를 저장
        self._run_handler(header, data_array)

        # 콜백 이벤트 실행
        self._run_event_handler(header.data_type)

        # Monitor 데이터 처리
        self._run_handler_for_monitor(header, data_array)

        # 데이터 처리 완료 확인
        self._receiver.checked()

        return header.data_type


    def _run_handler(self, header, data_array):
        
        # 일반 데이터 처리
        if self._parser.d[header.data_type] is not None:
            self._storage_header.d[header.data_type]   = header
            self._storage.d[header.data_type]          = self._parser.d[header.data_type](data_array)
            self._storage_count.d[header.data_type]    += 1


    def _run_event_handler(self, data_type):
        if (isinstance(data_type, DataType)) and (self._event_handler.d[data_type] is not None) and (self._storage.d[data_type] is not None):
            return self._event_handler.d[data_type](self._storage.d[data_type])
        else:
            return None


    def _run_handler_for_monitor(self, header, data_array):
        
        # Monitor 데이터 처리
        # 수신 받은 데이터를 파싱하여 self.monitor_data[] 배열에 데이터를 넣음
        if header.data_type == DataType.MONITOR:
            
            monitor_header_type = MonitorHeaderType(data_array[0])

            if monitor_header_type == MonitorHeaderType.MONITOR_0:
                
                monitor0 = Monitor0.parse(data_array[1:1 + Monitor0.get_size()])

                if monitor0.monitor_dataType == monitor_dataType.F32:
                    
                    data_count = (data_array.len() - 1 - Monitor0.get_size()) / 4

                    for i in range(0, data_count):
                        
                        if monitor0.index + i < len(self.monitor_data):
                            
                            index = 1 + Monitor0.get_size() + (i * 4)
                            self.monitor_data[monitor0.index + i], = unpack('<f', data_array[index:index + 4])

            elif monitor_header_type == MonitorHeaderType.MONITOR_4:
                
                monitor4 = Monitor4.parse(data_array[1:1 + Monitor4.get_size()])

                if monitor4.monitor_dataType == monitor_dataType.F32:
                    
                    self.system_time_monitor_data = monitor4.system_time
                    
                    data_count = (data_array.len() - 1 - Monitor4.get_size()) / 4

                    for i in range(0, data_count):
                        
                        if monitor4.index + i < len(self.monitor_data):
                            
                            index = 1 + Monitor4.get_size() + (i * 4)
                            self.monitor_data[monitor4.index + i], = unpack('<f', data_array[index:index + 4])

            elif monitor_header_type == MonitorHeaderType.MONITOR_8:
                
                monitor8 = Monitor8.parse(data_array[1:1 + Monitor8.get_size()])

                if monitor8.monitor_dataType == monitor_dataType.F32:
                    
                    self.system_time_monitor_data = monitor8.system_time
                    
                    data_count = (data_array.len() - 1 - Monitor8.get_size()) / 4

                    for i in range(0, data_count):
                        
                        if monitor8.index + i < len(self.monitor_data):
                            
                            index = 1 + Monitor8.get_size() + (i * 4)
                            self.monitor_data[monitor8.index + i], = unpack('<f', data_array[index:index + 4])


    def set_event_handler(self, data_type, eventHandler):
        
        if (not isinstance(data_type, DataType)):
            return

        self._event_handler.d[data_type] = eventHandler


    def get_header(self, data_type):
    
        if (not isinstance(data_type, DataType)):
            return None

        return self._storage_header.d[data_type]


    def get_data(self, data_type):

        if (not isinstance(data_type, DataType)):
            return None

        return self._storage.d[data_type]


    def get_count(self, data_type):

        if (not isinstance(data_type, DataType)):
            return None

        return self._storage_count.d[data_type]


    def _print_log(self, message):
        
        # 로그 출력
        if self._flag_show_log_message and message is not None:
            print(Fore.GREEN + "[{0:10.03f}] {1}".format((time.time() - self.time_start_program), message) + Style.RESET_ALL)


    def _print_error(self, message):
    
        # 오류 메세지 출력
        if self._flag_show_error_message and message is not None:
            print(Fore.RED + "[{0:10.03f}] {1}".format((time.time() - self.time_start_program), message) + Style.RESET_ALL)


    def _print_transfer_data(self, data_array):
    
        # 송신 데이터 출력
        if (self._flag_show_transfer_data) and (data_array is not None) and (len(data_array) > 0):
            print(Back.YELLOW + Fore.BLACK + convert_byte_array_to_string(data_array) + Style.RESET_ALL)


    def _print_receive_data(self, data_array):
        
        # 수신 데이터 출력
        if (self._flag_show_receive_data) and (data_array is not None) and (len(data_array) > 0):
            print(Back.CYAN + Fore.BLACK + convert_byte_array_to_string(data_array) + Style.RESET_ALL, end = '')


    def _print_receive_data_end(self):
        
        # 수신 데이터 출력(줄넘김)
        if self._flag_show_receive_data:
            print("")




# BaseFunctions End



# Common Start


    def send_ping(self, device_type):
        
        if  ( not isinstance(device_type, DeviceType) ):
            return None

        header = Header()
        
        header.data_type = DataType.PING
        header.length    = Ping.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = Ping()

        data.system_time = 0

        return self.transfer(header, data)


    def send_request(self, device_type, data_type):
    
        if ((not isinstance(device_type, DeviceType)) or 
            (not isinstance(data_type, DataType)) ):
            return None

        header = Header()
        
        header.data_type = DataType.REQUEST
        header.length    = Request.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = Request()

        data.data_type   = data_type

        return self.transfer(header, data)


    def send_pairing(self, device_type, address_0, address_1, address_2, scramble, channel_0, channel_1, channel_2, channel_3):
    
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(address_0, int)) or
            (not isinstance(address_1, int)) or
            (not isinstance(address_2, int)) or
            (not isinstance(scramble, int)) or
            (not isinstance(channel_0, int)) or
            (not isinstance(channel_1, int)) or
            (not isinstance(channel_2, int)) or
            (not isinstance(channel_3, int)) ):
            return None

        header = Header()
        
        header.data_type = DataType.PAIRING
        header.length    = Pairing.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = Pairing()

        data.address_0  = address_0
        data.address_1  = address_1
        data.address_2  = address_2
        data.scramble   = scramble
        data.channel_0  = channel_0
        data.channel_1  = channel_1
        data.channel_2  = channel_2
        data.channel_3  = channel_3

        return self.transfer(header, data)


# Common Start



# Control Start


    def send_takeoff(self):
        
        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.FLIGHT_EVENT
        data.option         = FlightEvent.TAKEOFF.value

        return self.transfer(header, data)
        '''

        return self.send_flight_event(FlightEvent.TAKEOFF)


    def send_landing(self):
        
        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.FLIGHT_EVENT
        data.option         = FlightEvent.LANDING.value

        return self.transfer(header, data)
        '''
        
        return self.send_flight_event(FlightEvent.LANDING)


    def send_stop(self):
        
        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length   = Command.get_size()
        header.from_    = DeviceType.BASE
        header.to_      = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.STOP
        data.option         = 0

        return self.transfer(header, data)
        '''
        
        return self.send_flight_event(FlightEvent.STOP)


    def send_control(self, roll, pitch, yaw, throttle):
        
        if ((not isinstance(roll, int)) or
            (not isinstance(pitch, int)) or
            (not isinstance(yaw, int)) or
            (not isinstance(throttle, int)) ):
            return None

        header = Header()
        
        header.data_type = DataType.CONTROL
        header.length    = ControlQuad8.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = ControlQuad8()

        data.roll       = int(roll)
        data.pitch      = int(pitch)
        data.yaw        = int(yaw)
        data.throttle   = int(throttle)

        return self.transfer(header, data)


    def send_control_time(self, roll, pitch, yaw, throttle, time_ms):
        
        if ((not isinstance(roll, int))     or
            (not isinstance(pitch, int))    or
            (not isinstance(yaw, int))      or
            (not isinstance(throttle, int)) ):
            return None

        time_sec     = time_ms / 1000
        time_start   = time.perf_counter()

        while ((time.perf_counter() - time_start) < time_sec):
            self.send_control(roll, pitch, yaw, throttle)
            sleep(0.02)

        return self.send_control(roll, pitch, yaw, throttle)


    def send_control_position_short(self, position_x, position_y, position_z, velocity, heading, rotational_velocity):
        
        if ((not (isinstance(position_x, float) or isinstance(position_x, int))) or
            (not (isinstance(position_y, float) or isinstance(position_y, int))) or
            (not (isinstance(position_z, float) or isinstance(position_z, int))) or
            (not (isinstance(velocity, float) or isinstance(velocity, int))) or
            (not (isinstance(heading, float) or isinstance(heading, int))) or
            (not (isinstance(rotational_velocity, float) or isinstance(rotational_velocity, int)))):
            return None

        header = Header()
        
        header.data_type = DataType.CONTROL
        header.length    = ControlPositionShort.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = ControlPositionShort()

        data.position_x             = int(position_x)
        data.position_y             = int(position_y)
        data.position_z             = int(position_z)
        data.velocity               = int(velocity)
        data.heading                = int(heading)
        data.rotational_velocity    = int(rotational_velocity)

        return self.transfer(header, data)


    def send_control_position(self, position_x, position_y, position_z, velocity, heading, rotational_velocity):
        
        if ((not (isinstance(position_x, float) or isinstance(position_x, int))) or
            (not (isinstance(position_y, float) or isinstance(position_y, int))) or
            (not (isinstance(position_z, float) or isinstance(position_z, int))) or
            (not (isinstance(velocity, float) or isinstance(velocity, int))) or
            (not (isinstance(heading, float) or isinstance(heading, int))) or
            (not (isinstance(rotational_velocity, float) or isinstance(rotational_velocity, int)))):
            return None

        header = Header()
        
        header.data_type = DataType.CONTROL
        header.length    = ControlPosition.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = ControlPosition()

        data.position_x             = float(position_x)
        data.position_y             = float(position_y)
        data.position_z             = float(position_z)
        data.velocity               = float(velocity)
        data.heading                = int(heading)
        data.rotational_velocity    = int(rotational_velocity)

        return self.transfer(header, data)


# Control End



# Setup Start


    def send_command(self, device_type, command_type, option = 0):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(command_type, CommandType)) or
            (not isinstance(option, int)) ):
            return None

        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = Command()

        data.command_type   = command_type
        data.option         = option

        return self.transfer(header, data)


    def send_command_light_event(self, device_type, command_type, option, light_event, interval, repeat):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(command_type, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int))):
            return None

        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = CommandLightEvent.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = CommandLightEvent()

        if ((isinstance(light_event, LightModeDrone)) or
            (isinstance(light_event, LightModeController))):
            data.event.event    = light_event.value
        elif isinstance(light_event, int):
            data.event.event    = light_event
        else:
            return None

        data.command.command_type   = command_type
        data.command.option         = option

        data.event.interval = interval
        data.event.repeat   = repeat

        return self.transfer(header, data)


    def send_command_light_event_color(self, device_type, command_type, option, light_event, interval, repeat, r, g, b):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(command_type, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = CommandLightEventColor.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = CommandLightEventColor()

        if ((isinstance(light_event, LightModeDrone)) or
            (isinstance(light_event, LightModeController))):
            data.event.event    = light_event.value
        elif isinstance(light_event, int):
            data.event.event    = light_event
        else:
            return None

        data.command.command_type   = command_type
        data.command.option         = option

        data.event.interval         = interval
        data.event.repeat           = repeat

        data.color.r                = r
        data.color.g                = g
        data.color.b                = b

        return self.transfer(header, data)


    def send_command_light_event_colors(self, device_type, command_type, option, light_event, interval, repeat, colors):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(command_type, CommandType)) or
            (not isinstance(option, int)) or
            (not isinstance(interval, int))  or
            (not isinstance(repeat, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = CommandLightEventColors.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = CommandLightEventColors()

        if ((isinstance(light_event, LightModeDrone)) or
            (isinstance(light_event, LightModeController))):
            data.event.event    = light_event.value
        elif isinstance(light_event, int):
            data.event.event    = light_event
        else:
            return None

        data.command.command_type   = command_type
        data.command.option         = option

        data.event.interval         = interval
        data.event.repeat           = repeat

        data.colors                 = colors

        return self.transfer(header, data)


    def send_mode_control_flight(self, mode_control_flight):
        
        if  ( not isinstance(mode_control_flight, ModeControlFlight) ):
            return None

        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.MODE_CONTROL_FLIGHT
        data.option         = mode_control_flight.value

        return self.transfer(header, data)
        '''
        return self.send_command(DeviceType.DRONE, CommandType.MODE_CONTROL_FLIGHT, mode_control_flight.value)


    def send_headless(self, headless):
        
        if  ( not isinstance(headless, Headless) ):
            return None

        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.HEADLESS
        data.option         = headless.value

        return self.transfer(header, data)
        '''
        return self.send_command(DeviceType.DRONE, CommandType.HEADLESS, headless.value)


    def send_trim(self, roll, pitch, yaw, throttle):
        
        if  ( (not isinstance(roll, int)) or (not isinstance(pitch, int)) or (not isinstance(yaw, int)) or (not isinstance(throttle, int)) ):
            return None

        header = Header()
        
        header.data_type = DataType.TRIM
        header.length    = Trim.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Trim()

        data.roll       = roll
        data.pitch      = pitch
        data.yaw        = yaw
        data.throttle   = throttle

        return self.transfer(header, data)


    def send_weight(self, weight):
        
        header = Header()
        
        header.data_type = DataType.WEIGHT
        header.length    = Weight.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Weight()

        data.weight     = weight

        return self.transfer(header, data)


    def send_lost_connection(self, time_neutral, time_landing, time_stop):
        
        header = Header()
        
        header.data_type = DataType.LOST_CONNECTION
        header.length    = LostConnection.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = LostConnection()

        data.time_neutral    = time_neutral
        data.time_landing    = time_landing
        data.time_stop       = time_stop

        return self.transfer(header, data)


    def send_flight_event(self, flight_event):
        
        if  ( (not isinstance(flight_event, FlightEvent)) ):
            return None

        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.FLIGHT_EVENT
        data.option         = flight_event.value

        return self.transfer(header, data)
        '''
        return self.send_command(DeviceType.DRONE, CommandType.FLIGHT_EVENT, flight_event.value)


    def send_clear_bias(self):
        
        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.CLEAR_BIAS
        data.option         = 0

        return self.transfer(header, data)
        '''
        return self.send_command(DeviceType.DRONE, CommandType.CLEAR_BIAS)


    def send_clear_trim(self):
        
        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Command()

        data.command_type   = CommandType.CLEAR_TRIM
        data.option         = 0

        return self.transfer(header, data)
        '''
        return self.send_command(DeviceType.DRONE, CommandType.CLEAR_TRIM)


    def send_set_default(self, device_type):
        
        if ((not isinstance(device_type, DeviceType))):
            return None

        '''
        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = Command()

        data.command_type   = CommandType.SET_DEFAULT
        data.option         = 0

        return self.transfer(header, data)
        '''
        return self.send_command(device_type, CommandType.SET_DEFAULT)


    def send_backlight_on(self):
        
        '''
        if ((not isinstance(flagPower, bool))):
            return None

        header = Header()
        
        header.data_type = DataType.COMMAND
        header.length    = Command.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER

        data = Command()

        data.command_type   = CommandType.BACKLIGHT
        data.option         = int(flagPower)

        return self.transfer(header, data)
        '''
        return self.send_command(DeviceType.CONTROLLER, CommandType.BACKLIGHT, 1)


    def send_backlight_off(self):
        
        return self.send_command(DeviceType.CONTROLLER, CommandType.BACKLIGHT, 0)


# Setup End



# Device Start


    def send_motor(self, motor_0, motor_1, motor_2, motor_3):
        
        if ((not isinstance(motor_0, int)) or
            (not isinstance(motor_1, int)) or
            (not isinstance(motor_2, int)) or
            (not isinstance(motor_3, int))):
            return None

        header = Header()
        
        header.data_type = DataType.MOTOR
        header.length    = Motor.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = Motor()

        data.motor[0].value     = motor_0
        data.motor[1].value     = motor_1
        data.motor[2].value     = motor_2
        data.motor[3].value     = motor_3

        return self.transfer(header, data)


    def send_motor_single(self, target, value):
        
        if ((not isinstance(target, int)) or
            (not isinstance(value, int))):
            return None

        header = Header()
        
        header.data_type = DataType.MOTOR_SINGLE
        header.length    = MotorSingle.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.DRONE

        data = MotorSingle()

        data.target     = target
        data.value      = value

        return self.transfer(header, data)


# Device End



# Light Start


    def send_light_manual(self, device_type, flags, brightness):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(flags, int)) or
            (not isinstance(brightness, int))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_MANUAL
        header.length    = LightManual.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightManual()

        data.flags      = flags
        data.brightness = brightness

        return self.transfer(header, data)


    def send_light_mode(self, device_type, light_mode, interval):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(interval, int))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_MODE
        header.length    = LightMode.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightMode()

        if ((isinstance(light_mode, LightModeDrone)) or
            (isinstance(light_mode, LightModeController))):
            data.mode  = light_mode.value
        elif isinstance(light_mode, int):
            data.mode  = light_mode
        else:
            return None

        data.interval  = interval

        return self.transfer(header, data)


    def send_light_mode_color(self, device_type, light_mode, interval, r, g, b):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_MODE
        header.length    = LightModeColor.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightModeColor()

        if ((isinstance(light_mode, LightModeDrone)) or
            (isinstance(light_mode, LightModeController))):
            data.mode.mode  = light_mode.value
        elif isinstance(light_mode, int):
            data.mode.mode  = light_mode
        else:
            return None

        data.mode.interval  = interval

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)


    def send_light_mode_colors(self, device_type, light_mode, interval, colors):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(interval, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_MODE
        header.length    = LightModeColors.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightModeColors()

        if ((isinstance(light_mode, LightModeDrone)) or
            (isinstance(light_mode, LightModeController))):
            data.mode.mode  = light_mode.value
        elif isinstance(light_mode, int):
            data.mode.mode  = light_mode
        else:
            return None

        data.mode.interval  = interval
        data.colors         = colors

        return self.transfer(header, data)


    def send_light_event(self, device_type, light_event, interval, repeat):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_EVENT
        header.length    = LightEvent.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightEvent()

        if ((isinstance(light_event, LightModeDrone)) or
            (isinstance(light_event, LightModeController))):
            data.event    = light_event.value
        elif isinstance(light_event, int):
            data.event    = light_event
        else:
            return None

        data.interval = interval
        data.repeat   = repeat

        return self.transfer(header, data)


    def send_light_event_color(self, device_type, light_event, interval, repeat, r, g, b):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_EVENT
        header.length    = LightEventColor.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightEventColor()

        if ((isinstance(light_event, LightModeDrone)) or
            (isinstance(light_event, LightModeController))):
            data.event.event    = light_event.value
        elif isinstance(light_event, int):
            data.event.event    = light_event
        else:
            return None

        data.event.interval = interval
        data.event.repeat   = repeat

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)


    def send_light_event_colors(self, device_type, light_event, interval, repeat, colors):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(interval, int)) or
            (not isinstance(repeat, int)) or
            (not isinstance(colors, Colors))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_EVENT
        header.length    = LightEventColors.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightEventColors()

        if ((isinstance(light_event, LightModeDrone)) or
            (isinstance(light_event, LightModeController))):
            data.event.event    = light_event.value
        elif isinstance(light_event, int):
            data.event.event    = light_event
        else:
            return None

        data.event.interval = interval
        data.event.repeat   = repeat

        data.colors         = colors

        return self.transfer(header, data)


    def send_light_default_color(self, device_type, light_mode, interval, r, g, b):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(interval, int)) or
            (not isinstance(r, int)) or
            (not isinstance(g, int)) or
            (not isinstance(b, int))):
            return None

        header = Header()
        
        header.data_type = DataType.LIGHT_DEFAULT
        header.length    = LightModeColor.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type

        data = LightModeColor()

        if ((isinstance(light_mode, LightModeDrone)) or
            (isinstance(light_mode, LightModeController))):
            data.mode.mode    = light_mode.value
        elif isinstance(light_mode, int):
            data.mode.mode    = light_mode
        else:
            return None

        data.mode.interval  = interval

        data.color.r        = r
        data.color.g        = g
        data.color.b        = b

        return self.transfer(header, data)


# Light End



# Display Start


    def send_display_clear_all(self, pixel = DisplayPixel.BLACK):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_CLEAR
        header.length    = DisplayClearAll.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayClearAll()

        data.pixel      = pixel

        return self.transfer(header, data)


    def send_display_clear(self, x, y, width, height, pixel = DisplayPixel.BLACK):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_CLEAR
        header.length    = DisplayClear.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayClear()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height
        data.pixel      = pixel

        return self.transfer(header, data)


    def send_display_invert(self, x, y, width, height):
        
        header = Header()
        
        header.data_type = DataType.DISPLAY_INVERT
        header.length    = DisplayInvert.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayInvert()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height

        return self.transfer(header, data)


    def send_display_draw_point(self, x, y, pixel = DisplayPixel.WHITE):
        
        if ( not isinstance(pixel, DisplayPixel) ):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_DRAW_POINT
        header.length    = DisplayDrawPoint.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayDrawPoint()

        data.x          = x
        data.y          = y
        data.pixel      = pixel

        return self.transfer(header, data)


    def send_display_draw_line(self, x1, y1, x2, y2, pixel = DisplayPixel.WHITE, line = DisplayLine.SOLID):
        
        if ((not isinstance(pixel, DisplayPixel)) or
            (not isinstance(line, DisplayLine)) ):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_DRAW_LINE
        header.length    = DisplayDrawLine.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayDrawLine()

        data.x1         = x1
        data.y1         = y1
        data.x2         = x2
        data.y2         = y2
        data.pixel      = pixel
        data.line       = line

        return self.transfer(header, data)


    def send_display_draw_rect(self, x, y, width, height, pixel = DisplayPixel.WHITE, flag_fill = False, line = DisplayLine.SOLID):
        
        if ((not isinstance(pixel, DisplayPixel)) or
            (not isinstance(flag_fill, bool)) or
            (not isinstance(line, DisplayLine)) ):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_DRAW_RECT
        header.length    = DisplayDrawRect.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayDrawRect()

        data.x          = x
        data.y          = y
        data.width      = width
        data.height     = height
        data.pixel      = pixel
        data.flag_fill  = flag_fill
        data.line       = line

        return self.transfer(header, data)


    def send_display_draw_circle(self, x, y, radius, pixel = DisplayPixel.WHITE, flag_fill = True):
        
        if ((not isinstance(pixel, DisplayPixel)) or
            (not isinstance(flag_fill, bool))):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_DRAW_CIRCLE
        header.length    = DisplayDrawCircle.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayDrawCircle()

        data.x          = x
        data.y          = y
        data.radius     = radius
        data.pixel      = pixel
        data.flag_fill  = flag_fill

        return self.transfer(header, data)


    def send_display_draw_string(self, x, y, message, font = DisplayFont.LIBERATION_MONO_5X8, pixel = DisplayPixel.WHITE):
        
        if ((not isinstance(font, DisplayFont)) or
            (not isinstance(pixel, DisplayPixel)) or
            (not isinstance(message, str))):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_DRAW_STRING
        header.length    = DisplayDrawString.get_size() + len(message)
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayDrawString()

        data.x          = x
        data.y          = y
        data.font       = font
        data.pixel      = pixel
        data.message    = message

        return self.transfer(header, data)


    def send_display_draw_string_align(self, x_start, x_end, y, message, align = DisplayAlign.CENTER, font = DisplayFont.LIBERATION_MONO_5X8, pixel = DisplayPixel.WHITE):
        
        if ((not isinstance(align, DisplayAlign)) or
            (not isinstance(font, DisplayFont)) or
            (not isinstance(pixel, DisplayPixel)) or
            (not isinstance(message, str))):
            return None

        header = Header()
        
        header.data_type = DataType.DISPLAY_DRAW_STRING_ALIGN
        header.length    = DisplayDrawStringAlign.get_size() + len(message)
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = DisplayDrawStringAlign()

        data.x_start    = x_start
        data.x_end      = x_end
        data.y          = y
        data.align      = align
        data.font       = font
        data.pixel      = pixel
        data.message    = message

        return self.transfer(header, data)


# Display End



# Buzzer Start


    def send_buzzer(self, device_type, mode, value, time):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(mode, BuzzerMode)) or
            (not isinstance(value, int)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length    = Buzzer.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type
        
        data = Buzzer()

        data.mode       = mode
        data.value      = value
        data.time       = time

        return self.transfer(header, data)


    def send_buzzer_mute(self, device_type, time):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length    = Buzzer.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type
        
        data = Buzzer()

        data.mode       = BuzzerMode.MUTE
        data.value      = BuzzerScale.MUTE.value
        data.time       = time

        return self.transfer(header, data)


    def send_buzzer_mute_reserve(self, device_type, time):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length    = Buzzer.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type
        
        data = Buzzer()

        data.mode       = BuzzerMode.MUTE_RESERVE
        data.value      = BuzzerScale.MUTE.value
        data.time       = time

        return self.transfer(header, data)


    def send_buzzer_scale(self, device_type, scale, time):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(scale, BuzzerScale)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length    = Buzzer.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type
        
        data = Buzzer()

        data.mode       = BuzzerMode.SCALE
        data.value      = scale.value
        data.time       = time

        return self.transfer(header, data)


    def send_buzzer_scale_reserve(self, device_type, scale, time):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(scale, BuzzerScale)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length    = Buzzer.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type
        
        data = Buzzer()

        data.mode       = BuzzerMode.SCALE_RESERVE
        data.value      = scale.value
        data.time       = time

        return self.transfer(header, data)


    def send_buzzer_hz(self, device_type, hz, time):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(hz, int)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length    = Buzzer.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type
        
        data = Buzzer()

        data.mode       = BuzzerMode.HZ
        data.value      = hz
        data.time       = time

        return self.transfer(header, data)


    def send_buzzer_hz_reserve(self, device_type, hz, time):
        
        if ((not isinstance(device_type, DeviceType)) or
            (not isinstance(hz, int)) or
            (not isinstance(time, int))):
            return None

        header = Header()
        
        header.data_type = DataType.BUZZER
        header.length    = Buzzer.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = device_type
        
        data = Buzzer()

        data.mode       = BuzzerMode.HZ_RESERVE
        data.value      = hz
        data.time       = time

        return self.transfer(header, data)


# Buzzer End



# Vibrator Start


    def send_vibrator(self, on, off, total):
        
        if ((not isinstance(on, int)) or
            (not isinstance(off, int)) or
            (not isinstance(total, int))):
            return None

        header = Header()
        
        header.data_type = DataType.VIBRATOR
        header.length    = Vibrator.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = Vibrator()

        data.mode       = VibratorMode.INSTANTLY
        data.on         = on
        data.off        = off
        data.total      = total

        return self.transfer(header, data)


    def send_vibrator_reserve(self, on, off, total):
        
        if ((not isinstance(on, int)) or
            (not isinstance(off, int)) or
            (not isinstance(total, int))):
            return None

        header = Header()
        
        header.data_type = DataType.VIBRATOR
        header.length    = Vibrator.get_size()
        header.from_     = DeviceType.BASE
        header.to_       = DeviceType.CONTROLLER
        
        data = Vibrator()

        data.mode       = VibratorMode.CONTINUALLY
        data.on         = on
        data.off        = off
        data.total      = total

        return self.transfer(header, data)


# Vibrator End



# Update Start




# Update End
