import serial
import time

class TerabeeHub:
    def __init__(self, port_name=None, freq=None, baudrate=921600, number_of_sensors=4):
        # Activate and Deactivate streaming commands
        self._ACTIVATE_STREAMING    = bytearray([0x00, 0x52, 0x02, 0x01, 0xDF])
        self._DEACTIVATE_STREAMING  = bytearray([0x00, 0x52, 0x02, 0x00, 0xD8])
        # Output frequency commands
        self._50_HZ                 = bytearray([0x00  ,0x52  ,0x03  ,0x02  ,0xC3])
        self._100_HZ                = bytearray([0x00  ,0x52  ,0x03  ,0x03  ,0xC4])
        self._250_HZ                = bytearray([0x00  ,0x52  ,0x03  ,0x04  ,0xD1])
        self._500_HZ                = bytearray([0x00  ,0x52  ,0x03  ,0x05  ,0xD6])
        self._600_HZ                = bytearray([0x00  ,0x52  ,0x03  ,0x06  ,0xDF])

        if port_name is None:
            print("No port name specified.")
            exit()
        self.number_of_sensors = number_of_sensors
        self.rngfnd_list = 8*[0]
        self.port_name = port_name
        self.baudrate = baudrate

        self.port = serial.Serial(  port = self.port_name, 
                                    baudrate=self.baudrate, 
                                    bytesize=serial.EIGHTBITS,
                                    timeout=10, 
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE)
        
        print("Port opened.")
        time.sleep(0.1)
        
        self.port.flushInput()
        self.port.flushOutput()
        
        
        self.activate_streaming()
        self.set_sampling_frequency(freq)

    def activate_streaming(self):
        self.port.write(self._ACTIVATE_STREAMING)
        time.sleep(0.1)
        self.port.flushInput()
        self.port.flushOutput()
        
        
    def deactivate_streaming(self):
        self.port.write(self._DEACTIVATE_STREAMING)
        time.sleep(0.1)
        self.port.flushInput()
        self.port.flushOutput()

    def set_sampling_frequency(self, freq):
        if freq is None:
            print("No frequency specified. Frequency set to default.")
            self.port.write(self._50_HZ)
        else:
            if freq == 50:
                self.port.write(self._50_HZ)
            elif freq == 100:
                self.port.write(self._100_HZ)
            elif freq == 250:
                self.port.write(self._250_HZ)
            elif freq == 500:
                self.port.write(self._500_HZ)
            elif freq == 600:
                self.port.write(self._600_HZ)
            else:
                print("Invalid frequency specified. Frequency set to default.")
                self.port.write(self._50_HZ)
        time.sleep(0.1)
        self.port.flushInput()
        self.port.flushOutput()

    def read_data(self):
        rngfnd_raw_data = (self.port.read(20)).hex()
        for i in range(8):
            self.rngfnd_list[i] = int("0x"+rngfnd_raw_data[4*i+4:4*i+8],16)
        return self.rngfnd_list
    
    def close_port(self):
        self.port.close()
        print("Port closed.")

if __name__=="__main__":
    port_name = "/dev/ttyS0"
    freq = 250
    number_of_sensors = 4
    terabee_hub = TerabeeHub(port_name, freq, number_of_sensors)
    
    number_of_meas = 50
    t_start = time.time()
    for i in range(number_of_meas):
        rngfnd_list = terabee_hub.read_data()
        print(rngfnd_list)

    
    print("frequency: ", number_of_meas/(time.time() - t_start))
    terabee_hub.close_port()
