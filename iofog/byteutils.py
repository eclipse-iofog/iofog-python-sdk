#TODO: refactor code like '*256*256*256'


def int2one_bytes(val):
    b = bytearray([0])
    b[0] = val & 0xFF
    return b


def one_bytes2int(val):
    return val[0]


def int2two_bytes(val):
    b = bytearray([0, 0])   # init
    #val & 0xFF
    #val & 0xFF
    b[1] = val & 0xFF
    val >>= 8
    b[0] = val & 0xFF
    return b


def two_bytes2int(b):
    return b[0]*256 + b[1]


def int2four_bytes(val):
    b = bytearray([0, 0, 0, 0])   # init
    b[3] = val & 0xFF
    val >>= 8
    b[2] = val & 0xFF
    val >>= 8
    b[1] = val & 0xFF
    val >>= 8
    b[0] = val & 0xFF
    return b


def four_bytes2int(b):
    return b[0]*256*256*256 + b[1]*256*256 + b[2]*256 + b[3]


def long2bytes(val):
    b = bytearray([0, 0, 0, 0, 0, 0, 0, 0])   # init
    b[7] = val & 0xFF
    val >>= 8
    b[6] = val & 0xFF
    val >>= 8
    b[5] = val & 0xFF
    val >>= 8
    b[4] = val & 0xFF
    val >>= 8
    b[3] = val & 0xFF
    val >>= 8
    b[2] = val & 0xFF
    val >>= 8
    b[1] = val & 0xFF
    val >>= 8
    b[0] = val & 0xFF
    return b


def bytes2lonf(val):
    return val[0]*256*256*256*256*256*256*256 + val[1]*256*256*256*256*256*256 + val[2]*256*256*256*256*256 + val[3]*256*256*256*256 + val[4]*256*256*256 + val[5]*256*256 + val[6]*256 + val[7]


def str2bytes(val):
    return val.encode("UTF-8")


def bytes2str(val):
    return val.decode("UTF-8")


def fetch_data(head_offset, head_len,  data_offset, data):
    data_len = None
    if head_len == 1:
        data_len = one_bytes2int(data[head_offset:head_offset+head_len])
    if head_len == 2:
        data_len = two_bytes2int(data[head_offset:head_offset+head_len])
    if head_len == 4:
        data_len = four_bytes2int(data[head_offset:head_offset+head_len])
    if data_len == 0:
        return None, data_offset + data_len, head_offset + head_len
    else:
        return data[data_offset:data_offset + data_len], data_offset + data_len, head_offset + head_len








