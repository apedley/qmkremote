
import time
import re
import sys
import hid

# vendor_id = 0xfefe
# product_id = 0xb171


# helix
# vendor_id = 0xfeed
# product_id = 0x71f2

# ximi 
vendor_id = 0xfefe
product_id = 0xb171

# # keychron

# vendor_id  = 0x3434
# product_id = 0x0260

usage_page = 0xFF60
usage      = 0x61


def get_raw_hid_interface(debug=False):
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])
    if (debug):
        print(f'Connected to: {interface.manufacturer} {interface.product}')
    

    return interface
def send_raw(data):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        sys.exit(1)

    request_data = [0x00] * 33 # First byte is Report ID
    request_data[1:len(data) + 1] = data
    print("request data:")
    print(request_data)
    request_packet = bytes(request_data)
    print(request_packet)

    try:
        interface.write(request_packet)

        response_packet = interface.read(32, timeout=1000)

        # print("Response:")
        # print(response_packet)
        return response_packet
      
    finally:
        interface.close()

def send_purple():
    data = [0, 130, 5, 0, 0, 0, 211, 4, 211, 0, 67, 0, 0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0];   
    send_raw([130, 5, 0, 0, 0, 115, 4, 115, 0, 25])
    
def send_reset():
    data = [0]*64
    data[1] = 129
    send_raw([129])

def get_layer(debug=False):
    response = send_raw([16])
    if debug:
        for i in response:
          print(f"{i:x}", end=" ")
        print()
    
    return response[2]

def poll_layer(rate=20):
    while True:
        layer = get_layer()
        print(layer)
        time.sleep(1/rate)
        
def get_info(debug=False):
    response = send_raw([17])
    if debug:
        for i in response:
          print(f"{i:x}", end=" ")
        print()
    
    return (response[2], response[3], response[4], response[5])

def get_key(layer, row, col, debug=False):
    response = send_raw([18, layer, row, col])
    if debug:
        for i in response:
          print(f"{i:x}", end=" ")
        print()
    
    return (response[2], response[3])
if __name__ == '__main__': 
    # send_purple()
    # time.sleep(4)
    # send_reset()
    # time.sleep(4)
    # get_layer()
    # poll_layer()
    
    print(get_info())
    time.sleep(1)
    
    # print(get_key(0, 2, 5))

    # time.sleep(4)
    print(get_key(0, 0, 0))
