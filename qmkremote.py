from struct import pack
import rawhid
import enum
import json

class QMKRemoteCommand(enum.Enum):
    OLED_OFF = 1
    OLED_ON = 2
    OLED_WRITE = 3
    OLED_CLEAR = 4
    RGB_OFF = 5
    RGB_ON = 6
    RGB_SETRGB_RANGE = 7
    MATRIX_OFF = 8
    MATRIX_ON = 9
    LAYER_ON = 11
    LAYER_OFF = 12
    LAYER_CLEAR = 13
    LAYER_MOVE = 14
    SEND_STRING = 15
    GET_LAYER = 16
    GET_INFO = 17
    MATRIX_INDICATOR_RANGE = 128
    MATRIX_INDICATOR_RESET = 129
    MATRIX_INDICATOR_ALL = 130
    MATRIX_GET_MODE = 131
    GET_KEYMAP_KEY = 132
class QMKRemote:
    layer = None
    matrix_status = True
    keycode_data = None
    
    # def __init__(self, vendor_id=0xfffe, product_id=0x0002, debug=False):
    def __init__(self, vendor_id=0x3434, product_id=0x0260, debug=False):
        self.connect(vendor_id, product_id, debug)
        with open('./keycodes.json', 'r') as f:
          self.keycode_data = json.load(f)
          
    
    def connect(self, vendor_id, product_id, debug=False):
        raw_interfaces = rawhid.find_interfaces(vendor_id, product_id)
        if rawhid.RawHIDInterface(raw_interfaces[0]['path']) is None:
            raise Exception("No device found")
        self.raw_interface = rawhid.RawHIDInterface(raw_interfaces[0]['path'], debug)
    
    def status(self):
        return self.raw_interface.path
    def read(self):
        return self.raw_interface.read()
    def read_long(self):
        return self.raw_interface.read(timeout=60000)
      
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
        
    def matrix_get_mode(self):
        packet = self.raw_interface.send([QMKRemoteCommand.MATRIX_GET_MODE.value], True)
        return packet[2]
    
    def layer_on(self, layer):
        self.raw_interface.send([QMKRemoteCommand.LAYER_ON.value, 1, 0, 0, 0, layer]) 
        
    def layer_off(self, layer):
        self.raw_interface.send([QMKRemoteCommand.LAYER_OFF.value, 1, 0, 0, 0, layer]) 
        
    def layer_clear(self):
        self.raw_interface.send([QMKRemoteCommand.LAYER_CLEAR.value])
        
    def layer_move(self, layer):
        self.raw_interface.send([QMKRemoteCommand.LAYER_MOVE.value, 1, 0, 0, 0, layer]) 
        
    def get_layer(self):
        packet = self.raw_interface.send([QMKRemoteCommand.GET_LAYER.value], True)
        return packet[2]
    # def get_keymap(self):
    #     packet = self.raw_interface.send([QMKRemoteCommand.GET_KEYMAP.value], True)
    #     return packet[2]
        
    def oled_off(self):
        self.raw_interface.send([QMKRemoteCommand.OLED_OFF.value])
        
    def oled_on(self):
        self.raw_interface.send([QMKRemoteCommand.OLED_ON.value]) 
        
    def rgb_off(self):
        self.raw_interface.send([QMKRemoteCommand.RGB_OFF.value])
        
    def rgb_on(self):
        self.raw_interface.send([QMKRemoteCommand.RGB_ON.value]) 
    
    def rgb_range(self, r, g, b, start, end):
        self.raw_interface.send([QMKRemoteCommand.RGB_SETRGB_RANGE.value, 5, 0, 0, 0, r, g, b, start, end])
    
    def get_info(self):
        packet = self.raw_interface.send([QMKRemoteCommand.GET_INFO.value], True)
        return packet[2, 3]
    
    def get_info(self):
        packet = self.raw_interface.send([QMKRemoteCommand.GET_INFO.value], True)
        # return [x for x in packet[2:6]]
        return tuple(packet[2:6])
      
    def get_keymap_key(self, layer, row, col):
        packet = self.raw_interface.send([QMKRemoteCommand.GET_KEYMAP_KEY.value, 5, 0, 0, 0, layer, row, col], True)
        # packet = self.raw_interface.send([QMKRemoteCommand.GET_KEY.value, 1, 0, 0, 0, layer, row, col], True)
        # packet = self.raw_interface.send([QMKRemoteCommand.GET_KEY.value, layer, row, col], True)
        # return [x for x in packet[2:4]]
        # key = (packet[2] << 8) + packet[3]
        key = packet[2] << 8 | packet[3]
        return key
    
    def get_keycode_for_key(self, key):
        return self.keycode_data["keycodes"][str(key)]
    