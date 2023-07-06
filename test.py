import qmkremote
import time

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

q = qmkremote.QMKRemote(vendor_id, product_id)

# q.rgb_off()

# time.sleep(2)

# q.rgb_on()

# time.sleep(2)
# mode = q.matrix_get_mode()

# print(mode)

# # time.sleep(2) 
# layer = q.get_layer()

# print("-----")
# print(layer)


# packet = q.read_long()
# print(packet)

# info = q.get_info()
# print(info) 


# key = q.get_key(0, 0, 0)
# print(key)

# k = key[2]<<8 | key[3]
# print(k)
# key2 = q.get_key(1, 1, 1)
# print(key2)

# q.matrix_indicator_range(15, 155, 125, 4, 8)


# time.sleep(2)
# q.matrix_indicator_reset()

# time.sleep(2)

# res = q.matrix_get_mode()
# res = q.get_keymap_key(0, 1, 0)

  # for col in range(cols):
  #   for layer in range(layers):
  #     key = q.get_keymap_key(row, col, layer)
  #     print(key, end=" ")
  #   print()
  # print()
  # print()

# def print_key(keycode):
#   print(f"{keycode:x}", end=" ")
#   # print(hex(keycode))
  
# print_key()

# k = q.get_keymap_key(0, 0, 0)


(rows, cols, layers, split) = q.get_info()

for col in range(cols):
    for row in range(rows):
        key = q.get_keymap_key(0, row, col)
        print(f"{key:x}", end=" ")
    print()
  
# k = q.get_keycode_for_key("KC_DOT")
# print(k)
# print(f"{k:x}")