def calculate_crc(data):
    crc = 0xFFFF
    polynomial = 0xA001

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= polynomial
            else:
                crc >>= 1

    return crc.to_bytes(2, byteorder='little')

# data = [1, 3, 0, 6, 0, 1, 100, 11]
# data = [1, 3, 0, 6, 0, 1, 100, 11]
[1, 3, 0, 6, 0, 1, 100, 11]
data =[1, 3, 0, 7, 0, 1, 53, 203]
crc = calculate_crc(data)
print("CRC-16-Modbus: ", crc.hex())
