from .core import Wallbox, registers, is_register_readable
import argparse
import minimalmodbus


parser = argparse.ArgumentParser()
parser.add_argument('device', action='store', nargs='?', default='/dev/ttyUSB0')
args = parser.parse_args()


def print_all_readable_registers(wb, registers):
    for item in registers.items():
        addr = item[0]
        fields = item[1]
        if is_register_readable(addr):
            print(fields['description'], wb.read_register(addr))


instrument = minimalmodbus.Instrument(args.device, 1)  # port name, slave address (in decimal)
instrument.serial.parity = minimalmodbus.serial.PARITY_ODD
instrument.serial.timeout = 1 # in seconds

wb = Wallbox(instrument, registers)

print_all_readable_registers(wb, registers)

# Note: if no car is connected, wallbox goes into Standby (not responding
# to Modbus requests) and needs to be restarted.
# wb.enable_standby(False)

# wb.set_max_current(65)
