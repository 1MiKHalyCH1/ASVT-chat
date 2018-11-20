from struct import pack, unpack


def send_msg(s, msg):
    msg_len = pack("<I", len(msg))
    s.send(msg_len + msg)


def recv_msg(s):
    msg_len = unpack("<I", s.recv(4))[0]
    return s.recv(msg_len)


def addr_to_str(addr):
    return "'{}:{}'".format(*addr)


def get_user_by_addr(addr, users):
    res = [u for u, ip in users.items() if ip == addr[0]]
    return res[0] if res else None
