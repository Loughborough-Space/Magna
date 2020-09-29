import sys
import glob
import serial
import serial.tools.list_ports


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def get_serial(COM):
    global srl
    srl = serial.Serial(COM, 9600, timeout=0.1)

    if not (srl.dtr or srl.rts):
        srl.open()
    print("Serial Port on '%s' opened" % COM)


def get_serial_ports():
    ports_list = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    return ports_list


def send():
    ser = serial.Serial('COM3')
    print(ser.name)
    ser.write(b'E')
    ser.close()


if __name__ == '__main__':
    ports_list = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print(ports_list)
