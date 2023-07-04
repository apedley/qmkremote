import qmkremote
import time
vendor_id = 0xfefe
product_id = 0xb171
# vendor_id = 0xfffe
# product_id = 0x0002

# vendor_id  = 0x3434
# product_id = 0x0260

# vendor_id  = 0x3265
# product_id = 0x0000

usage_page = 0xFF60
usage      = 0x61

q = qmkremote.QMKRemote(vendor_id, product_id)

# q.rgb_off()

# time.sleep(2)

# q.rgb_on()

# time.sleep(2)
mode = q.matrix_get_mode()

print(mode)

time.sleep(2)
layer = q.get_layer()

print("-----")
print(layer)