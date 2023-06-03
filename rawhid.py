import sys
import hid

def find_interfaces(vendor_id, product_id, usage_page=0xFF60, usage=0x61):
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]
    if len(raw_hid_interfaces) == 0:
        raise Exception("No device found")
        
    return raw_hid_interfaces

class RawHIDInterface:
    def __init__(self, path, debug=False):
        self.path = path
        self.interface = None
        self.debug = debug
        if self.debug:
            print(f'Init {self.path}')
        
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.interface.close()

    def send(self, data, wait_for_response=False):
        self.interface = hid.Device(path=self.path)
        if self.interface is None:
            print("No device found")
            sys.exit(1)

        request_data = [0x00] * 33 # First byte is Report ID
        request_data[1:len(data) + 1] = data
        request_packet = bytes(request_data)
        
        if self.debug:
            print(f'Request: {request_packet}')
            print(f'Data: {request_data}')
        try:
            self.interface.write(request_packet)
            
            if wait_for_response:
                response_packet = self.interface.read(32, timeout=1000)

                return response_packet
        finally:
            self.interface.close()
