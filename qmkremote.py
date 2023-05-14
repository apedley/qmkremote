import rawhid
import enum

class QMKRemoteCommand(enum.Enum):
    MATRIX_OFF = 8
    MATRIX_ON = 9
    MATRIX_INDICATOR_RANGE = 128
    MATRIX_INDICATOR_RESET = 129
    MATRIX_INDICATOR_ALL = 130

class QMKRemote:
    
    def __init__(self, vendor_id=0x3434, product_id=0x0260):
        raw_interfaces = rawhid.find_interfaces(vendor_id, product_id)
        if rawhid.RawHIDInterface(raw_interfaces[0]['path']) is None:
            raise Exception("No device found")
        self.raw_interface = rawhid.RawHIDInterface(raw_interfaces[0]['path'])
    
    def status(self):
        return self.raw_interface.path
    def matrix_off(self):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_OFF.value])
    
    def matrix_on(self):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_ON.value])
        
    def matrix_indicator_reset(self):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_INDICATOR_RESET.value])
    
    def matrix_indicator_all(self, r, g, b):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_INDICATOR_ALL.value, 5, 0, 0, 0, r, g, b, 0, 67])
    
    def matrix_indicator_range(self, r, g, b, start, end):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_INDICATOR_RANGE.value, 5, 0, 0, 0, r, g, b, start, end])