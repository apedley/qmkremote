import rawhid
import enum

class QMKRemoteCommand(enum.Enum):
    MATRIX_OFF = 8
    MATRIX_ON = 9
    LAYER_ON = 11
    LAYER_OFF = 12
    LAYER_CLEAR = 13
    LAYER_MOVE = 14
    MATRIX_INDICATOR_RANGE = 128
    MATRIX_INDICATOR_RESET = 129
    MATRIX_INDICATOR_ALL = 130

class QMKRemote:
    layer = None
    matrix_status = True
    
    # def __init__(self, vendor_id=0xfffe, product_id=0x0002, debug=False):
    def __init__(self, vendor_id=0x3434, product_id=0x0260, debug=False):
        self.connect(vendor_id, product_id, debug)
    
    def connect(self, vendor_id, product_id, debug=False):
        raw_interfaces = rawhid.find_interfaces(vendor_id, product_id)
        if rawhid.RawHIDInterface(raw_interfaces[0]['path']) is None:
            raise Exception("No device found")
        self.raw_interface = rawhid.RawHIDInterface(raw_interfaces[0]['path'], debug)
    
    def status(self):
        return self.raw_interface.path
    
    def matrix_off(self):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_OFF.value])
        self.matrix_status = False
        
    def matrix_on(self):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_ON.value])
        self.matrix_status = True
        
    def matrix_toggle(self):
        if self.matrix_status:
            self.matrix_off()
        else:
            self.matrix_on()
        
    def matrix_indicator_reset(self):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_INDICATOR_RESET.value])
    
    def matrix_indicator_all(self, r, g, b):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_INDICATOR_ALL.value, 5, 0, 0, 0, r, g, b, 0, 67])
    
    def matrix_indicator_range(self, r, g, b, start, end):
        self.raw_interface.send([QMKRemoteCommand.MATRIX_INDICATOR_RANGE.value, 5, 0, 0, 0, r, g, b, start, end])
    
    def layer_on(self, layer):
        self.raw_interface.send([QMKRemoteCommand.LAYER_ON.value, 1, 0, 0, 0, layer]) 
        
    def layer_off(self, layer):
        self.raw_interface.send([QMKRemoteCommand.LAYER_OFF.value, 1, 0, 0, 0, layer]) 
        
    def layer_clear(self):
        self.raw_interface.send([QMKRemoteCommand.LAYER_CLEAR.value])
        
    def layer_move(self, layer):
        self.raw_interface.send([QMKRemoteCommand.LAYER_MOVE.value, 1, 0, 0, 0, layer]) 