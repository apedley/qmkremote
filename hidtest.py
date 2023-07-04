
import sys
import hid

vendor_id = 0xfefe
product_id = 0xb171

# vendor_id  = 0x3434
# product_id = 0x0260

usage_page = 0xFF60
usage      = 0x61


def get_raw_hid_interface():
    device_interfaces = hid.enumerate(vendor_id, product_id)
    raw_hid_interfaces = [i for i in device_interfaces if i['usage_page'] == usage_page and i['usage'] == usage]

    if len(raw_hid_interfaces) == 0:
        return None

    interface = hid.Device(path=raw_hid_interfaces[0]['path'])
    print(f'Connected to: {interface.manufacturer} {interface.product}')
    

    return interface
def send_raw(data):
    interface = get_raw_hid_interface()

    if interface is None:
        print("No device found")
        sys.exit(1)

    request_data = [0x00] * 33 # First byte is Report ID
    request_data[1:len(data) + 1] = data
    request_packet = bytes(request_data)

    try:
        interface.write(request_packet)

        response_packet = interface.read(32, timeout=1000)

        print("Response:")
        print(response_packet)
    finally:
        interface.close()

def send_purple():
    data = [0, 130, 5, 0, 0, 0, 211, 4, 211, 0, 67, 0, 0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0, 0, 0,   0, 0,   0, 0,  0, 0,0,   0, 0, 0];   
    send_raw([130, 5, 0, 0, 0, 211, 4, 211, 0, 67])
    
def send_reset():
    data = [0]*64
    data[1] = 129
    send_raw([129])
    
if __name__ == '__main__': 
    # send_purple()
    send_reset()