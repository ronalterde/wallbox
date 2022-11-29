registers = {
    # Input Registers:
    4: { "functioncodes": [4], "datatype": "uint16", "description": "Register Layout Version"},
    5: { "functioncodes": [4], "datatype": "uint16", "description": "Charging State"},
    6: { "functioncodes": [4], "datatype": "uint16", "description": "Current L1"},
    7: { "functioncodes": [4], "datatype": "uint16", "description": "Current L2"},
    8: { "functioncodes": [4], "datatype": "uint16", "description": "Current L3"},
    9: { "functioncodes": [4], "datatype": "int16", "description": "PCB Temperature"},
    10: { "functioncodes": [4], "datatype": "uint16", "description": "Voltage L1"},
    11: { "functioncodes": [4], "datatype": "uint16", "description": "Voltage L2"},
    12: { "functioncodes": [4], "datatype": "uint16", "description": "Voltage L3"},
    13: { "functioncodes": [4], "datatype": "uint16", "description": "External Lock State"},
    14: { "functioncodes": [4], "datatype": "uint16", "description": "Power L123 [VA]"},
    15: { "functioncodes": [4], "datatype": "uint16", "description": "Energy since Power On high byte"},
    16: { "functioncodes": [4], "datatype": "uint16", "description": "Energy since Power On low byte [VAh]"},
    17: { "functioncodes": [4], "datatype": "uint16", "description": "Energy since Installation high byte"},
    18: { "functioncodes": [4], "datatype": "uint16", "description": "Energy since Installation low byte [VAh]"},
    100: { "functioncodes": [4], "datatype": "uint16", "description": "Hardware configuration max. current"},
    101: { "functioncodes": [4], "datatype": "uint16", "description": "Hardware configuration min. current"},

    # Holding Registers:
    257: { "functioncodes": [3, 6], "datatype": "uint16", "description": "Modbus Master Watchdog timeout"}, # in ms; 0 = Off
    258: { "functioncodes": [6], "datatype": "uint16", "description": "Standby Function Control"}, # Power saving if no car plugged (0: standby enable, 4: standby disable
    259: { "functioncodes": [3, 6], "datatype": "uint16", "description": "Remote Lock unlocked"}, # 0: locked, 1: unlocked. only if extern lock unlocked
    261: { "functioncodes": [3, 6], "datatype": "uint16", "description": "Maximal Current"}, # in 0.1A, range: 0, 60-160
    262: { "functioncodes": [3, 6], "datatype": "uint16", "description": "Failsafe Current"}, # in case modbus connection is lost. range: 0, 60-160; 0 = error
}


def is_register_readable(addr):
# 3: read holding register, 4: read input register
    return 3 in registers[addr]["functioncodes"] or 4 in registers[addr]["functioncodes"]


def is_register_writeable(addr):
# 6: write holding register
    return 6 in registers[addr]["functioncodes"]


class Wallbox:
    def __init__(self, instrument, registers):
        self.instrument = instrument
        self.registers = registers
    
    def read_register(self, addr):
        assert is_register_readable(addr)
        functioncode = self.registers[addr]['functioncodes'][0]
        return self.instrument.read_register(addr, functioncode=functioncode)

    def disable_watchdog(self):
        addr = 257
        functioncode = self.registers[addr]['functioncodes'][-1]
        self.instrument.write_register(addr, 0, functioncode=functioncode)

    def enable_standby(self, en):
        addr = 258
        value = 0 if en else 4
        functioncode = self.registers[addr]['functioncodes'][-1]
        self.instrument.write_register(addr, value, functioncode=functioncode)

    def set_max_current(self, value):
        # in 0.1A, range: 0, 60-160
        # setting values < 60 will result in a value of zero.
        assert value >= 60 and value <= 160
        addr = 261
        functioncode = self.registers[addr]['functioncodes'][-1]
        self.instrument.write_register(addr, value, functioncode=functioncode)
